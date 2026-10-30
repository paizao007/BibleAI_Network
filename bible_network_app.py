import os
import sys
import json
import re
import time
import random
import requests
import threading
from datetime import datetime, timezone, timedelta
from typing import List, Dict, Any, Optional
from flask import Flask, render_template, jsonify, request

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except Exception:
        pass

def get_brazil_time_str():
    # Horário Oficial de Brasília (UTC-3)
    br_tz = timezone(timedelta(hours=-3))
    return datetime.now(br_tz).strftime('%d/%m/%Y %H:%M:%S')

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_FILE = os.path.join(BASE_DIR, "database", "bible_data.json")
WORKSPACES_DIR = os.path.join(BASE_DIR, "workspaces")
TEMPLATES_DIR = os.path.join(BASE_DIR, "templates")

os.makedirs(os.path.join(BASE_DIR, "database"), exist_ok=True)
os.makedirs(WORKSPACES_DIR, exist_ok=True)

app = Flask(__name__, template_folder=TEMPLATES_DIR)
app.config['TEMPLATES_AUTO_RELOAD'] = True

# Estado global do servidor
is_paused = False

from dotenv import load_dotenv

load_dotenv()

from theological_engine import build_monumental_treatise, build_deep_peer_debate, identify_theological_context

cycle_lock = threading.Lock()

def extract_json_from_text(raw_text: str):
    if not raw_text:
        return None
    clean = re.sub(r'<think>.*?</think>', '', raw_text, flags=re.DOTALL).strip()
    try:
        return json.loads(clean)
    except Exception:
        pass

    if '```json' in clean:
        try:
            block = clean.split('```json')[-1].split('```')[0].strip()
            return json.loads(block)
        except Exception:
            pass
    elif '```' in clean:
        try:
            block = clean.split('```')[1].split('```')[0].strip()
            return json.loads(block)
        except Exception:
            pass

    first_brace = clean.find('{')
    last_brace = clean.rfind('}')
    if first_brace != -1 and last_brace != -1 and last_brace > first_brace:
        try:
            return json.loads(clean[first_brace:last_brace+1])
        except Exception:
            pass

    return None

# --- MOTOR BICAMERAL DE SEGURANÇA E CITATION ENGINE ---
class OllamaBibleAgentEngine:
    def __init__(self, host: str = "http://localhost:11434"):
        self.host = host.rstrip('/')
        raw_keys = os.environ.get("GEMINI_API_KEY", "")
        self.gemini_keys = [k.strip() for k in raw_keys.split(",") if k.strip() and k.strip() not in ["", "sua_chave_aqui"]]
        self.gemini_api_key = self.gemini_keys[0] if self.gemini_keys else None
        self._key_index = 0
            
        saved_engine = None
        saved_model = None
        try:
            if os.path.exists(DB_FILE):
                with open(DB_FILE, 'r', encoding='utf-8') as f:
                    _d = json.load(f)
                    saved_engine = _d.get("active_engine")
                    saved_model = _d.get("selected_model")
        except Exception:
            pass

        # Preferencia persistida do usuario; padrao e ollama local com gemma3:4b
        self.active_engine = (saved_engine or os.environ.get("ACTIVE_ENGINE", "ollama")).lower()
        self.gemini_model = "gemini-3-flash-preview"
        self.local_model = "gemma3:4b"

        if saved_model:
            if "gemini" in saved_model.lower():
                self.gemini_model = saved_model
            else:
                self.local_model = saved_model

        self.selected_model = self.gemini_model if self.active_engine == "gemini" else self.local_model
        self._update_model_display_name()

    def _update_model_display_name(self):
        if self.active_engine == "gemini":
            num_keys = len(self.gemini_keys)
            self.model = f"Google Gemini ⚡ ({self.gemini_model}) [{num_keys} chave(s)]"
        elif self.active_engine == "ollama":
            self.model = f"Ollama Local 🦙 ({self.local_model})"
        else:
            self.model = "Fallback de Segurança (Nenhum motor válido configurado)"

    def _get_active_keys(self) -> List[str]:
        return self.gemini_keys if self.gemini_keys else ([self.gemini_api_key] if self.gemini_api_key else [])

    def _chat_via_gemini(self, messages: List[Dict[str, str]], format: Optional[str] = None, timeout: int = 25) -> Dict[str, Any]:
        prompt_text = ""
        for m in messages:
            role = m.get("role", "user").upper()
            prompt_text += f"{role}:\n{m.get('content', '')}\n\n"

        payload = {"contents": [{"parts": [{"text": prompt_text}]}]}
        gen_config = {"temperature": 0.85, "maxOutputTokens": 8192}
        if format == "json":
            gen_config["response_mime_type"] = "application/json"
        payload["generationConfig"] = gen_config

        candidate_models = [
            self.gemini_model,
            "gemini-3.1-flash-lite",
            "gemini-flash-latest"
        ]
        # Remove duplicatas preservando ordem
        candidate_models = list(dict.fromkeys([m for m in candidate_models if m]))

        keys_to_try = self._get_active_keys()
        if not keys_to_try:
            raise RuntimeError("Nenhuma chave Gemini disponível.")

        last_err = None
        consecutive_429 = 0
        for key in keys_to_try:
            for target_m in candidate_models:
                url = f"https://generativelanguage.googleapis.com/v1beta/models/{target_m}:generateContent?key={key}"
                try:
                    r = requests.post(url, json=payload, timeout=6)
                    if r.status_code == 200:
                        data = r.json()
                        cand = data.get("candidates", [])
                        if cand:
                            parts = cand[0].get("content", {}).get("parts", [])
                            if parts and "text" in parts[0]:
                                return {"content": parts[0]["text"], "model_used": target_m}
                    elif r.status_code == 429:
                        last_err = f"Quota 429 excedida em {target_m}"
                        consecutive_429 += 1
                        if consecutive_429 >= 2:
                            # Cota do projeto esgotada: failover imediato para o motor catedrático sem travamento
                            raise RuntimeError(f"Gemini cota esgotada: {last_err}")
                        continue
                    elif r.status_code == 503:
                        last_err = f"Serviço 503 temporariamente indisponível em {target_m}"
                        continue
                    else:
                        last_err = f"Status {r.status_code} em {target_m}: {r.text[:120]}"
                        continue
                except RuntimeError:
                    raise
                except Exception as e:
                    last_err = str(e)
                    continue

        raise RuntimeError(f"Gemini API error: {last_err}")

    def _chat_via_ollama(self, messages: List[Dict[str, str]], format: Optional[str] = None, timeout: int = 400, max_tokens: Optional[int] = None) -> Dict[str, Any]:
        url = f"{self.host}/api/chat"
        # Candidatos confiaveis instalados na maquina do usuario
        models_to_try = [self.local_model, "gemma3:4b", "qwen2.5:3b"]
        models_to_try = list(dict.fromkeys([m for m in models_to_try if m]))

        # num_predict: -1 indica ao Ollama geracao 100% livre/ilimitada ate o término natural do raciocinio
        predict_tokens = max_tokens if (max_tokens is not None and max_tokens > 0) else -1

        last_err = None
        for m_name in models_to_try:
            try:
                # num_gpu: 0 garante execucao 100% estavel em CPU sem crash de driver em placas Kepler (GT 740)
                payload = {
                    "model": m_name, 
                    "messages": messages, 
                    "stream": False,
                    "options": {
                        "num_gpu": 0,
                        "num_predict": predict_tokens,
                        "temperature": 0.7
                    }
                }
                token_desc = "ILIMITADOS / LIVRES" if predict_tokens == -1 else f"{predict_tokens} tokens"
                print(f"[🦙 Ollama Local] Processando via '{m_name}' (CPU Estável, tokens={token_desc}, timeout={timeout}s)...")
                r = requests.post(url, json=payload, timeout=timeout)
                if r.status_code == 200:
                    res = r.json()
                    raw_content = res.get("message", {}).get("content", "")
                    clean_content = re.sub(r'<think>.*?</think>', '', raw_content, flags=re.DOTALL).strip()
                    return {"content": clean_content, "model_used": f"Ollama ({m_name})"}
                else:
                    last_err = f"Status {r.status_code}: {r.text[:120]}"
                    print(f"[!] Erro no modelo local '{m_name}': {last_err}")
            except Exception as e:
                last_err = str(e)
                print(f"[!] Falha no modelo local '{m_name}': {e}. Tentando proximo candidato...")
                continue

        raise RuntimeError(f"Ollama local indisponivel apos tentar modelos: {last_err}")

    def chat(self, messages: List[Dict[str, str]], format: Optional[str] = None, max_tokens: Optional[int] = None) -> Dict[str, Any]:
        if self.active_engine == "ollama":
            # 🛡️ Quando configurado como Ollama, NUNCA muda ou chama Gemini!
            return self._chat_via_ollama(messages, format=format, max_tokens=max_tokens)
        elif self.active_engine == "gemini":
            if self.gemini_api_key:
                try:
                    return self._chat_via_gemini(messages, format=format)
                except Exception as e:
                    print(f"[!] Gemini falhou nos candidatos ativos: {e}. Tentando fallback local Ollama...")
                    return self._chat_via_ollama(messages, format=format, max_tokens=max_tokens)
            else:
                print("[!] Modo Gemini selecionado sem chave API. Utilizando Ollama local...")
                return self._chat_via_ollama(messages, format=format, max_tokens=max_tokens)
        else:
            return self._chat_via_ollama(messages, format=format, max_tokens=max_tokens)

    def generate_theological_post(self, agent: Dict[str, Any], topic: str, past_posts: List[Dict[str, Any]] = None) -> Dict[str, str]:
        memory_str = ""
        if past_posts:
            # Memória pessoal dos estudos anteriores deste teólogo
            agent_posts = [p for p in past_posts if p["agent_id"] == agent["id"]][-2:]
            if agent_posts:
                memory_str += "\nSUA MEMÓRIA TEOLÓGICA ANTERIOR:\n"
                for p in agent_posts:
                    memory_str += f"- Estudo prévio seu: '{p['title']}'\n"

            # Memória coletiva do colegiado sobre a pauta lançada
            debates_on_topic = [p for p in past_posts if p.get("topic") == topic][-2:]
            if debates_on_topic:
                memory_str += f"\nDISCUSSÕES RECENTES DO COLEGIADO SOBRE A PAUTA '{topic}':\n"
                for dp in debates_on_topic:
                    memory_str += f"- @{dp['agent_name']} abordou: '{dp['title']}' com foco em: {dp['content'][:250]}...\n"

        ctx = identify_theological_context(topic)
        is_open = ctx.get("is_open_context", False)

        if is_open:
            pericope_directive = f"""2. PERÍCOPE EM FOCO E CONTEXTO REAL:
   Pauta central: "{topic}".
   INSTRUÇÃO DE BUSCA DA VERDADE CANÔNICA: A pauta é aberta. Identifique no cânon bíblico a perícope central autêntica e os textos sagrados que tratam de "{topic}".
   Examine o texto em seu ambiente autêntico no Antigo Testamento (Hebraico) ou Novo Testamento (Grego), sem citar versículos fora de contexto e sem inventar livros ou capítulos."""
            section_1_title = f"1. Texto Sagrado & Exposição Canônica sobre '{topic}'"
        else:
            pericope_directive = f"""2. PERÍCOPE EM FOCO E CONTEXTO REAL:
   Pauta central: "{topic}".
   Passagem sagrada de referência: "{ctx.get('verse_text')}" — ({ctx.get('verse_ref')}).
   Examine o texto em seu contexto histórico e literário autêntico ({ctx.get('era')}), sem misturar temas desconexos ou cometer anacronismos."""
            section_1_title = f"1. Texto Sagrado & Exposição Canônica ({ctx.get('verse_ref')})"

        system_prompt = f"""Você é o erudito bíblico e servo de Deus @{agent['name']} ({agent['role']}).
Sua especialidade teológica é: {agent['specialty']}.
{memory_str}

🔥 LIBERDADE INTELECTUAL, ERUDIÇÃO E BUSCA AUTÊNTICA DA VERDADE BÍBLICA:
1. PENSAMENTO LIVRE E FIDELIDADE ÀS ESCRITURAS:
   Pense com liberdade crítica e profunda reverência. Fuja de moldes pré-fabricados, chavões mecânicos e clichês repetitivos. Busque a verdade de Deus em todo o conselho bíblico.
{pericope_directive}
3. EXEGESE NOS IDIOMAS ORIGINAIS (GREGO KOINÉ OU HEBRAICO):
   Analise com precisão 3 a 5 termos essenciais da perícope nos originais:
   - Forneça o termo em caracteres originais em negrito (ex: **καρπός**, **ἀγάπη**, **πνεῦμα**, **חֶסֶד**, etc.).
   - Indique a transliteração e o código do Léxico Strong linkado (ex: `**ἀγάπη** (*agapē* - [Strong G26](https://biblehub.com/greek/26.htm))`).
   - Mostre como a raiz semântica esclarece a doutrina bíblica e transforma o crente.
4. VOZ E CÁTEDRA ESPECÍFICA:
   Redija na voz de @{agent['name']}, destacando as contribuições singulares da sua cátedra ({agent['specialty']}).
5. ESTRUTURA DO TRATADO (5 SEÇÕES SÓLIDAS EM MARKDOWN):
   - 📖 **{section_1_title}**
   - 🏛️ **2. Contexto Histórico, Manuscritos & Ambiente da Revelação** (Papiros, Códices, cultura da época)
   - 📜 **3. Exegese Linguística Profunda dos Idiomas Originais** (Originais grego/hebraico com Strong)
   - 🔗 **4. Harmonia Teológica, Cumprimento em Cristo & Vida Prática** (Aplicação na vida do crente)
   - 📚 **5. Fontes & Referências Manuscritas Consultadas** (com links Markdown reais para Codex Sinaiticus, STEP Bible, BibleHub, etc.)

FORMATO DE SAÍDA EXIGIDO (JSON puro):
{{
    "title": "Título Nobre, Espiritual e Erudito",
    "content": "Conteúdo monumental, profundo, com 5 seções densas e ricas em exegese e adoração em Markdown..."
}}
"""
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Elabore o estudo teológico monumental e aprofundado sobre a pauta: {topic}"}
        ]
        
        try:
            res = self.chat(messages, format="json", max_tokens=-1)
            raw_text = res["content"].strip()
            data = extract_json_from_text(raw_text)
            if data and data.get("content") and len(data["content"]) > 100:
                data["content"] = clean_theological_hallucinations(data["content"])
                if data.get("title"):
                    data["title"] = clean_theological_hallucinations(data["title"])
                print(f"[✨ IA REAL - {res.get('model_used')}] Estudo autêntico e inédito gerado para @{agent['name']} sobre '{topic}'!")
                return data
        except Exception as e:
            print(f"[!] Erro no processamento de post: {e}")

        # Fallback monumental e enciclopédico com fontes explícitas
        print(f"[🏛️ CÁTEDRA ERUDITA] Gerando tratado monumental aprofundado para @{agent['name']} sobre '{topic}'...")
        return build_monumental_treatise(agent, topic)

    def generate_theological_comment(self, agent: Dict[str, Any], post_title: str, post_content: str, author_name: str, past_posts: List[Dict[str, Any]] = None, topic: str = "", existing_comments: List[Dict[str, Any]] = None) -> str:
        memory_str = ""
        if past_posts:
            agent_comments = []
            for p in past_posts:
                for c in p.get("comments", []):
                    if c.get("agent_id") == agent["id"]:
                        agent_comments.append(c.get("content", ""))
            if agent_comments:
                memory_str = "\nSUA MEMÓRIA DE DEBATES ANTERIORES:\n"
                for ac in agent_comments[-2:]:
                    memory_str += f"- Você argumentou anteriormente: {ac[:180]}...\n"

        existing_debate_str = ""
        if existing_comments:
            existing_debate_str = "\nCONTRIBUIÇÕES DOS COLEGAS QUE JÁ PARTICIPARAM DESTE DEBATE:\n"
            for ec in existing_comments[-2:]:
                existing_debate_str += f"- @{ec['agent_name']} observou: \"{ec['content'][:250]}...\"\n"

        ctx = identify_theological_context(topic or post_title)

        system_prompt = f"""Você é o erudito bíblico e servo do Senhor @{agent['name']} ({agent['role']}).
Sua especialidade teológica é: {agent['specialty']}.
Seu estimado colega @{author_name} redigiu um tratado sobre: "{topic or post_title}".
Perícope em debate: "{ctx.get('verse_text')}" — ({ctx.get('verse_ref')})
Título do estudo: "{post_title}"
Trecho do estudo analisado:
{post_content[:1000]}...
{memory_str}
{existing_debate_str}

🔥 DIRETRIZES DE DEBATE TEOLÓGICO AUTÊNTICO (SAIR DA CAIXA E BUSCAR A VERDADE):
1. DEBATE REAL, CRÍTICO E NÃO REPETITIVO:
   Não repita o que @{author_name} ou outros colegas já disseram. Analise o argumento apresentado e traga uma PERSPECTIVA NOVA da sua própria cátedra ({agent['role']}).
2. DIALÉTICA ERUDITA E FRATERNA:
   Aponte nuances contextuais, gramaticais dos originais (grego/hebraico com Strong), testemunhos históricos patrísticos, implicações da teologia pactual ou aplicações práticas que enriqueçam o debate.
3. SEM BORDÕES OU FRASES DECORADAS:
   PROIBIDO usar clichês vazios ("amado irmão faminto", etc.). Cada parágrafo deve conter substância bíblica e teológica real.
4. EXTENSÃO E ESTILO:
   Redija de 2 a 3 parágrafos densos, eruditos, bíblicos e cheios de zelo pela verdade revelada em Cristo.
5. CONCLUSÃO OBRIGATÓRIA:
   Conclua SEMPRE todos os seus períodos e pensamentos com ponto final, sem deixar frases cortadas ou inacabadas.
"""
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Escreva seu comentário fundamentado debatendo a pauta '{topic or post_title}' com @{author_name}."}
        ]
        try:
            res = self.chat(messages, max_tokens=-1)
            comment = res["content"].strip()
            comment = re.sub(r'<think>.*?</think>', '', comment, flags=re.DOTALL).strip()
            if len(comment) > 40:
                comment = clean_theological_hallucinations(comment)
                print(f"[✨ IA REAL - {res.get('model_used')}] Comentario autentico de @{agent['name']} sobre '{topic or post_title}'!")
                return comment
        except Exception as e:
            print(f"[!] Erro gerando comentário individual de @{agent['name']}: {e}")

        print(f"[🏛️ DEBATE ENTRE PARES] Gerando réplica teológica aprofundada de @{agent['name']} sobre '{topic or post_title}'...")
        return build_deep_peer_debate(agent, author_name, topic or post_title, post_title)

    def _get_agent_specific_comment_fallback(self, agent: Dict[str, Any], author_name: str, topic: str) -> str:
        return build_deep_peer_debate(agent, author_name, topic, topic)

    def _get_fallback_with_sources(self, agent: Dict[str, Any], topic: str) -> Dict[str, str]:
        return build_monumental_treatise(agent, topic)

ai_engine = OllamaBibleAgentEngine()

# --- HELPER DATABASE FUNCTIONS ---
LEGACY_FIXED_TOPICS = {
    "Ezequiel 25:17",
    "O Amor Redentor em João 3:16",
    "O Sacrifício e o Amor de Deus em João 3:16",
    "A Ceia do Senhor: Memorial ou Transubstanciacao",
    "O Tabernáculo de Moisés e a Tipologia de Cristo",
    "A Palavra Graça: Hesed no Hebraico vs Charis no Grego",
    "O Véu do Templo Rasgado: O Significado Teológico e Histórico",
    "Adoração em Espírito e em Verdade (João 4:23-24): Liberdade da Lei e Intimidade com Cristo",
    "As 70 Semanas de Daniel e as Profecias Messiânicas"
}

db_rw_lock = threading.Lock()

def load_db():
    with db_rw_lock:
        if os.path.exists(DB_FILE):
            for attempt in range(3):
                try:
                    with open(DB_FILE, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        raw_topics = data.get("topics", [])
                        clean_topics = [t for t in raw_topics if t not in LEGACY_FIXED_TOPICS]
                        if len(clean_topics) != len(raw_topics):
                            data["topics"] = clean_topics
                            # Chama escrita atômica interna
                            tmp_file = DB_FILE + ".tmp"
                            with open(tmp_file, 'w', encoding='utf-8') as tf:
                                json.dump(data, tf, indent=4, ensure_ascii=False)
                            os.replace(tmp_file, DB_FILE)
                        return data
                except (json.JSONDecodeError, IOError):
                    time.sleep(0.05)
        return {"agents": [], "topics": [], "posts": [], "studies": []}

def save_db(data):
    with db_rw_lock:
        tmp_file = DB_FILE + ".tmp"
        with open(tmp_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        os.replace(tmp_file, DB_FILE)

# --- FLASK ROUTES ---
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/data')
def get_data():
    db = load_db()
    db["is_paused"] = db.get("is_paused", False)
    db["active_engine"] = ai_engine.active_engine
    db["selected_model"] = ai_engine.selected_model
    db["engine_info"] = ai_engine.model
    topics = db.get("topics", [])
    if not topics:
        last_post_topic = db.get("posts", [])[-1].get("topic") if db.get("posts") else "fim dos tempos"
        active_topic = last_post_topic or "fim dos tempos"
        topics = [active_topic]
        db["topics"] = topics
        save_db(db)
    else:
        active_topic = topics[0]

    ctx = identify_theological_context(active_topic)
    db["active_verse_text"] = ctx.get("verse_text", "")
    db["active_verse_ref"] = ctx.get("verse_ref", "")
    return jsonify(db)

@app.route('/api/topics/add', methods=['POST'])
def add_topic():
    req_data = request.get_json() or {}
    new_topic = req_data.get('topic', '').strip()
    if not new_topic:
        return jsonify({"error": "Pauta inválida"}), 400
        
    db = load_db()
    topics = db.setdefault("topics", [])
    if new_topic in topics:
        topics.remove(new_topic)
    # Insere no topo para ser fixada como pauta central ativa
    topics.insert(0, new_topic)
    save_db(db)
    return jsonify({"success": True, "topics": topics, "active_topic": new_topic})

@app.route('/api/topics/delete', methods=['POST'])
def delete_topic():
    req_data = request.get_json() or {}
    target_topic = req_data.get('topic', '').strip()
    db = load_db()
    topics = db.get("topics", [])
    if target_topic in topics:
        topics.remove(target_topic)
        db["topics"] = topics
        save_db(db)
    return jsonify({"success": True, "topics": db.get("topics", [])})

@app.route('/api/toggle_pause', methods=['POST'])
def toggle_pause():
    db = load_db()
    current_status = db.get("is_paused", False)
    new_status = not current_status
    db["is_paused"] = new_status
    save_db(db)
    print(f"[⏸️] Estado do Servidor alterado e salvo em bible_data.json: is_paused={new_status}")
    return jsonify({"success": True, "is_paused": new_status})

@app.route('/api/set_engine', methods=['POST'])
def set_engine():
    req_data = request.get_json() or {}
    engine = req_data.get('engine', '').strip()
    api_key = req_data.get('api_key', '').strip()
    
    if engine:
        db = load_db()
        if "gemini" in engine.lower():
            ai_engine.active_engine = "gemini"
            ai_engine.gemini_model = engine
            ai_engine.selected_model = engine
            ai_engine._update_model_display_name()
            db["active_engine"] = "gemini"
            db["selected_model"] = engine
        else:
            ai_engine.active_engine = "ollama"
            ai_engine.local_model = engine
            ai_engine.selected_model = engine
            ai_engine._update_model_display_name()
            db["active_engine"] = "ollama"
            db["selected_model"] = engine
            
        if api_key and api_key != "sua_chave_aqui":
            ai_engine.gemini_api_key = api_key
            ai_engine.gemini_keys = [api_key]
            
        save_db(db)
        print(f"[⚙️ Motor Atualizado & Persistido] active_engine={db['active_engine']}, selected_model={db['selected_model']}")
        return jsonify({
            "success": True, 
            "engine_info": ai_engine.model,
            "active_engine": db["active_engine"],
            "selected_model": db["selected_model"]
        })
    return jsonify({"error": "Motor invalido"}), 400

@app.route('/api/shutdown', methods=['POST'])
def shutdown():
    print("[🛑] Encerrando o servidor BibleAI Network...")
    def stop_server():
        time.sleep(1)
        os._exit(0)
    threading.Thread(target=stop_server).start()
    return jsonify({"success": True, "message": "Servidor sendo desligado com segurança."})

def execute_study_cycle_internal(selected_topic=None, selected_agent_id=None, is_manual=False):
    db = load_db()
    if not is_manual and db.get("is_paused", False):
        return {"status": "paused", "message": "O ciclo autônomo está pausado pelo usuário."}

    # Bloqueio leve não-bloqueante para evitar conflitos concorrentes
    if not cycle_lock.acquire(blocking=True if is_manual else False, timeout=25 if is_manual else -1):
        return {"status": "busy", "message": "Ciclo de estudo já em andamento..."}

    try:
        db = load_db()
        agents = db.get("agents", [])
        topics = db.get("topics", [])
        
        if not agents:
            return {"error": "Nenhum agente configurado"}
            
        past_posts = db.get("posts", [])
        
        # 1. Garante que se o usuário escolheu uma pauta específica, ela seja respeitada e fixada no topo
        if selected_topic and str(selected_topic).strip():
            topic = str(selected_topic).strip()
            if topic in topics:
                topics.remove(topic)
            topics.insert(0, topic)
            db["topics"] = topics
            save_db(db)
        elif topics:
            topic = topics[0]
        else:
            # Se não houver pauta cadastrada, recupera do último estudo gerado
            last_post_topic = past_posts[-1].get("topic") if past_posts else "fim dos tempos"
            topic = last_post_topic or "fim dos tempos"
            topics = [topic]
            db["topics"] = topics
            save_db(db)

        # Seleção de autor: rotaciona ativamente entre os 7 eruditos para que cada um traga a visão de sua cátedra
        if selected_agent_id:
            aid = str(selected_agent_id).strip().lower()
            target_agent = next((a for a in agents if a["id"].lower() == aid or a["name"].lower() == aid or aid in a["id"].lower() or aid in a["name"].lower()), None)
            author = target_agent if target_agent else random.choice(agents)
        elif past_posts:
            # Encontra teólogos que ainda não escreveram sobre esta pauta recente
            topic_authors = [p.get("agent_id") for p in past_posts[-7:] if p.get("topic") == topic and p.get("agent_id")]
            candidates = [a for a in agents if a["id"] not in topic_authors]
            if not candidates:
                recent_authors = [p.get("agent_id") for p in past_posts[-3:] if p.get("agent_id")]
                candidates = [a for a in agents if a["id"] not in recent_authors]
            author = random.choice(candidates) if candidates else random.choice(agents)
        else:
            author = random.choice(agents)
                
        print(f"[📚 CITATION ENGINE] Gerando ESTUDO COM FONTES EXPLÍCITAS por @{author['name']} sobre '{topic}'...")
        
        res = ai_engine.generate_theological_post(author, topic, past_posts)
        
        # 🛡️ VERIFICAÇÃO RIGOROSA ANTI-DUPLICAÇÃO
        new_sig = ''.join(res["content"].split())[:80]
        recent_sigs = [''.join(p.get("content", "").split())[:80] for p in past_posts[-15:] if p.get("content")]
        if new_sig in recent_sigs:
            print(f"[🛡️ ANTI-DUPLICAÇÃO] Conteúdo idêntico detectado para @{author['name']}. Alternando cátedra...")
            authors_for_topic = [p.get("agent_id") for p in past_posts if p.get("topic") == topic]
            new_candidates = [a for a in agents if a["id"] not in authors_for_topic and a["id"] != author["id"]]
            if new_candidates:
                author = random.choice(new_candidates)
                res = ai_engine.generate_theological_post(author, topic, past_posts)
        
        timestamp = get_brazil_time_str()
        post_id = f"study_{int(time.time())}"
        
        # Seleciona de 2 a 3 colegas para debaterem ativamente a pauta
        available_commenters = [a for a in agents if a["id"] != author["id"]]
        num_commenters = 1 if ai_engine.active_engine == "ollama" else min(len(available_commenters), 3)
        commenting_agents = random.sample(available_commenters, num_commenters)
        comments = []
        for c_agent in commenting_agents:
            time.sleep(1)  # Pausa respeitosa entre chamadas individuais
            c_text = ai_engine.generate_theological_comment(
                c_agent, res["title"], res["content"], author["name"], 
                past_posts, topic=topic, existing_comments=comments
            )
            comments.append({
                "agent_id": c_agent["id"],
                "agent_name": c_agent["name"],
                "content": c_text,
                "timestamp": timestamp
            })
            
        new_post = {
            "id": post_id,
            "agent_id": author["id"],
            "agent_name": author["name"],
            "avatar": author["avatar"],
            "specialty": author["specialty"],
            "topic": topic,
            "title": res["title"],
            "content": res["content"],
            "timestamp": timestamp,
            "comments": comments
        }
        
        db.setdefault("posts", []).append(new_post)
        save_db(db)
        
        agent_ws = os.path.join(WORKSPACES_DIR, author["name"])
        os.makedirs(agent_ws, exist_ok=True)
        study_file = os.path.join(agent_ws, f"{post_id}.md")
        
        with open(study_file, 'w', encoding='utf-8') as f:
            f.write(f"# 📜 {res['title']}\n\n")
            f.write(f"**Autor:** @{author['name']} ({author['role']})\n")
            f.write(f"**Data:** {timestamp}\n")
            f.write(f"**Pauta:** {topic}\n\n")
            f.write(f"{res['content']}\n\n")
            f.write("## 💬 Debates & Contribuições dos Colegas Teólogos\n\n")
            for c in comments:
                f.write(f"### @{c['agent_name']}:\n{c['content']}\n\n")
                
        return {"success": True, "post": new_post}
    finally:
        cycle_lock.release()

@app.route('/api/run_cycle', methods=['POST'])
def run_cycle():
    req_data = request.get_json() if request.is_json else {}
    selected_topic = req_data.get("topic") if req_data else None
    selected_agent_id = req_data.get("agent_id") if req_data else None
    result = execute_study_cycle_internal(selected_topic, selected_agent_id, is_manual=True)
    if "error" in result:
        return jsonify(result), 400
    return jsonify(result)

def background_generation_loop():
    import time
    time.sleep(6)  # Aguarda servidor iniciar
    while True:
        # Quando rodando em Ollama Local, dar intervalo de 120s para respiro de CPU/GPU
        # Quando em Gemini nuvem, 60s
        loop_interval = 180 if ai_engine.active_engine == "ollama" else 60
        time.sleep(loop_interval)  # Interação contínua autônoma equilibrada e anti-duplicação
        try:
            db = load_db()
            if not db.get("is_paused", False):
                execute_study_cycle_internal(is_manual=False)
            else:
                print("[⏸️ Loop Autônomo] Em repouso (pesquisas autônomas pausadas pelo usuário).")
        except Exception as e:
            print(f"[Loop Autônomo] Interação: {e}")

threading.Thread(target=background_generation_loop, daemon=True).start()

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5005))
    print("=" * 65)
    print(" 📜 BibleAI Network v6.0 — Citation & Sources Engine Ativo")
    print(f" 🌐 Painel do Usuário: http://localhost:{port}")
    print("=" * 65)
    app.run(host='0.0.0.0', port=port, debug=False)
