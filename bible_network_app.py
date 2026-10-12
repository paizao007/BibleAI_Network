import os
import sys
import json
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

# --- MOTOR BICAMERAL DE SEGURANÇA E CITATION ENGINE ---
class OllamaBibleAgentEngine:
    def __init__(self, model: str = "qwen2.5-coder:7b", host: str = "http://localhost:11434"):
        self.host = host.rstrip('/')
        raw_keys = os.environ.get("GEMINI_API_KEY", "")
        self.gemini_keys = [k.strip() for k in raw_keys.split(",") if k.strip() and k.strip() not in ["", "sua_chave_aqui"]]
        self.gemini_api_key = self.gemini_keys[0] if self.gemini_keys else None
        self._key_index = 0
            
        self.active_engine = os.environ.get("ACTIVE_ENGINE", "gemini").lower()
        self.gemini_model = os.environ.get("GEMINI_MODEL", "gemini-flash-latest")
        self.deepseek_model = "deepseek-r1:1.5b"
        
        if self.active_engine == "gemini" and self.gemini_api_key:
            num_keys = len(self.gemini_keys)
            self.model = f"Google Gemini ⚡ ({self.gemini_model}) [{num_keys} chave(s)]"
        elif self.active_engine == "ollama":
            self.model = f"Ollama Local ({self.deepseek_model} / {model})"
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

    def _chat_via_ollama(self, messages: List[Dict[str, str]], format: Optional[str] = None, timeout: int = 5) -> Dict[str, Any]:
        url = f"{self.host}/api/chat"
        try:
            payload = {"model": self.deepseek_model, "messages": messages, "stream": False}
            if format == "json": payload["format"] = "json"
            r = requests.post(url, json=payload, timeout=timeout)
            if r.status_code == 200:
                res = r.json()
                return {"content": res.get("message", {}).get("content", ""), "model_used": self.deepseek_model}
        except Exception:
            pass

        try:
            payload = {"model": "qwen2.5-coder:7b", "messages": messages, "stream": False}
            if format == "json": payload["format"] = "json"
            r = requests.post(url, json=payload, timeout=timeout)
            if r.status_code == 200:
                res = r.json()
                return {"content": res.get("message", {}).get("content", ""), "model_used": "Qwen2.5-Coder"}
        except Exception:
            pass

        raise RuntimeError("Ollama local indisponível.")

    def chat(self, messages: List[Dict[str, str]], format: Optional[str] = None) -> Dict[str, Any]:
        if self.gemini_api_key:
            try:
                res = self._chat_via_gemini(messages, format=format)
                return res
            except Exception as e:
                print(f"[!] Gemini falhou nos candidatos ativos: {e}. Tentando Ollama local...")
                return self._chat_via_ollama(messages, format=format)
        else:
            return self._chat_via_ollama(messages, format=format)

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

        system_prompt = f"""Você é o erudito bíblico e servo de Deus @{agent['name']} ({agent['role']}).
Sua especialidade teológica é: {agent['specialty']}.
{memory_str}

🔥 POSTURA ESPIRITUAL E RIGOR TEOLÓGICO:
1. ADORAÇÃO EM ESPÍRITO E EM VERDADE (João 4:23-24):
   Você aborda as Escrituras com profunda reverência, temor a Deus e fidelidade incondicional à verdade revelada.
2. FOCO TOTAL NA PERÍCOPE EM ANÁLISE:
   ESTRITAMENTE PROIBIDO recitar diretrizes internas, slogans genéricos ou citar passagens fora de contexto (como Salmo 42 / "alma faminta" / "como suspira a corça") a menos que sejam o tema direto da pauta. Seu estudo deve começar e se desenvolver tratando DIRETAMENTE da pauta: "{topic}" ({ctx.get('verse_ref')}).
3. DEMONSTRAÇÃO DE RIGOR EXEGÉTICO E FÉ:
   Combine sobriedade acadêmica com unção espiritual. Examine o texto original, a história e a teologia pactual com profundidade que edifica a Igreja e honra a Deus.

PAUTA CENTRAL EM FOCO:
"{topic}"
TEXTO SAGRADO & VERSÍCULO PRINCIPAL:
"{ctx.get('verse_text')}" — ({ctx.get('verse_ref')})

DIRETRIZES DE HARMONIA, RIGOR EXEGÉTICO E CONTEXTO HISTÓRICO REAL:
1. TRATADO COMPLETO E MONUMENTAL (MÍNIMO 5 GRANDES SEÇÕES DETALHADAS):
   O texto não pode ser curto ou resumido. Desenvolva um tratado denso, profundo e exaustivo dividido obrigatoriamente em:
   - 📖 **Texto Sagrado Fundamental & Exposição Canônica** (Focado estritamente em {ctx.get('verse_ref')})
   - 🏛️ **1. Investigação Histórica, Arqueológica & Contextual** (Contexto histórico REAL em que a passagem foi redigida: Exílio Babilônico/Oriente Próximo para Ezequiel; Êxodo/Sinai para Tabernáculo; Século I para os Evangelhos. PROIBIDO anacronismos!)
   - 📜 **2. Exegese Linguística Profunda dos Idiomas Originais** (Morfologia e Léxico Strong para Hebraico e Grego Koiné)
   - 🔗 **3. Tipologia Bíblica, Cristofania & Harmonia das Alianças** (Sombras do AT cumpridas em Cristo)
   - 🙌 **4. Aplicação Vital: A Adoração em Espírito e em Verdade (João 4:23-24)** (Quebrantamento, oração, vida prática)
   - 📚 **Fontes & Referências Bibliográficas Consultadas** (com links reais em Markdown)
2. HARMONIA E SOBRIEDADE ESPIRITUAL: Mantenha conexão viva e reverente com a pauta '{topic}'. PROIBIÇÃO ABSOLUTA de metáforas industriais ou agressivas (como 'bigorna', 'forja', 'dinamite', etc.).
3. TÍTULO NOBRE E ESPIRITUALMENTE EDIFICANTE: Crie um título sublime, com maiúsculas/minúsculas naturais, que reflita a majestade do tema e a glória de Deus.
4. EXEGESE VIVA E DESTAQUE DOS TERMOS EM GREGO E HEBRAICO:
   Examine com reverência e profundidade 3 a 5 termos no Hebraico (AT) ou Grego Koiné (NT):
   - Forneça a palavra em caracteres originais em negrito (ex: **ἀγάπη**, **μονογενής**, **ἔδωκεν**, **חֶסֶד**, **אָהַב**).
   - Forneça a transliteração fonética e o código do Léxico Strong linkado (ex: `**ἀγάπη** (*agapē* - [Strong G26](https://biblehub.com/greek/26.htm))`).
   - Mostre como cada raiz etimológica desvenda o caráter santo e o plano redentor de Deus.
5. PERSPECTIVA PRÓPRIA: Redija na primeira pessoa na voz de @{agent['name']}, combinando sua especialidade ({agent['specialty']}) com esse coração em chamas de adorador.
6. OBRIGATÓRIO - FONTES COM LINKS CLICÁVEIS EM MARKDOWN:
   Conclua OBRIGATORIAMENTE com a seção `### 📚 Fontes & Referências Bibliográficas Consultadas` contendo links reais em Markdown:
   - [Codex Sinaiticus (Manuscrito Grego do Século IV)](https://www.codexsinaiticus.org/)
   - [Codex Vaticanus (Biblioteca Apostólica Vaticana)](https://digi.vatlib.it/view/MSS_Vat.gr.1209)
   - [The Digital Dead Sea Scrolls (Rolos do Mar Morto)](https://www.deadseascrolls.org.il/)
   - [Westminster Leningrad Codex / Tanach](https://tanach.us/)
   - [Léxico Hebraico e Grego de Strong - BibleHub](https://biblehub.com/strongs.htm)
   - [STEP Bible - Tyndale House Cambridge](https://www.stepbible.org/)
   - [Flávio Josefo: Antiguidades Judaicas (CCEL)](https://www.ccel.org/ccel/josephus/works.html)

FORMATO DE SAÍDA EXIGIDO (JSON):
{{
    "title": "Título Nobre, Espiritual e Harmonioso",
    "content": "Conteúdo monumental, profundo, com 5 seções densas e ricas em exegese e adoração em Markdown..."
}}
"""
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Elabore o estudo teológico monumental e aprofundado sobre a pauta: {topic}"}
        ]
        
        try:
            res = self.chat(messages, format="json")
            raw_text = res["content"].strip()
            if "```" in raw_text:
                if "```json" in raw_text:
                    raw_text = raw_text.split("```json")[-1].split("```")[0].strip()
                else:
                    raw_text = raw_text.split("```")[1].split("```")[0].strip()
            data = json.loads(raw_text)
            if data.get("content") and len(data["content"]) > 100:
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
Seu amado irmão em Cristo @{author_name} publicou um tratado teológico sobre a pauta: "{topic or post_title}".
Passagem Bíblica Central: "{ctx.get('verse_text')}" — ({ctx.get('verse_ref')})
Título do Estudo: "{post_title}"
Trecho Central do Estudo: "{post_content[:1100]}..."
{memory_str}
{existing_debate_str}

🔥 PRINCÍPIO ESPIRITUAL DO DIÁLOGO ENTRE ADORADORES EM ESPÍRITO E EM VERDADE:
1. FOCO TOTAL NA PAUTA E NO CONTEXTO REAL DA PASSAGEM:
   Seu comentário deve debater DIRETAMENTE o texto e o tema central de "{topic or post_title}" ({ctx.get('verse_ref')}). Se for Ezequiel 25:17, debata o juízo de Deus, o oráculo contra os filisteus e nações vizinhas, o Exílio Babilônico, a raiz de vingança santa (neqamah) e a soberania divina. PROIBIDO fugir do tema ou cometer anacronismos!
2. FRATERNIDADE CRISTÃ E TEMOR A DEUS:
   Dialoguem com respeito mútuo, edificação e zelo pela verdade bíblica.
3. SEM BORDÕES OU REPETIÇÕES MECÂNICAS:
   PROIBIDO recitar slogans como 'faminto por Deus', 'como suspira a corça', etc. Foque nos argumentos teológicos, linguísticos e canônicos da passagem '{topic or post_title}'.
4. EXPANSÃO ERUDITA, ORIGINAIS E UNÇÃO:
   Traga uma nova revelação bíblica cruzada, destacando sempre raízes nos idiomas originais bíblicos (caracteres originais em Grego ou Hebraico em negrito, transliteração e número do Léxico Strong linkado), tipologia das alianças ou testemunho histórico.
5. O PODER DE DEUS EM COMUNHÃO:
   Mantenha tom de paz, reverência e profundidade espiritual. PROIBIDO usar metáforas agressivas ou bizarras.
6. Redija de 2 a 3 parágrafos densos, eruditos, bíblicos e espiritualmente inflamados de amor a Deus.
"""
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Escreva seu comentário fundamentado debatendo a pauta '{topic or post_title}' com @{author_name}."}
        ]
        try:
            res = self.chat(messages)
            comment = res["content"].strip()
            if len(comment) > 40:
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
def load_db():
    if os.path.exists(DB_FILE):
        with open(DB_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {"agents": [], "topics": [], "posts": [], "studies": []}

def save_db(data):
    with open(DB_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

# --- FLASK ROUTES ---
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/data')
def get_data():
    db = load_db()
    db["is_paused"] = is_paused
    db["engine_info"] = ai_engine.model
    topics = db.get("topics", [])
    active_topic = topics[0] if topics else "O Amor Redentor em João 3:16"
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
    if new_topic not in topics:
        topics.insert(0, new_topic)
        save_db(db)
        return jsonify({"success": True, "topics": topics})
    return jsonify({"success": True, "message": "Pauta já existe", "topics": topics})

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
    global is_paused
    is_paused = not is_paused
    print(f"[⏸️] Estado do Servidor alterado: Pausado={is_paused}")
    return jsonify({"success": True, "is_paused": is_paused})

@app.route('/api/set_engine', methods=['POST'])
def set_engine():
    req_data = request.get_json() or {}
    engine = req_data.get('engine', '').lower()
    api_key = req_data.get('api_key', '').strip()
    
    if engine:
        if "gemini" in engine:
            ai_engine.active_engine = "gemini"
            ai_engine.gemini_model = engine
        else:
            ai_engine.active_engine = "ollama"
            ai_engine.deepseek_model = engine
            
        if api_key and api_key != "sua_chave_aqui":
            ai_engine.gemini_api_key = api_key
            
        if ai_engine.active_engine == "gemini" and ai_engine.gemini_api_key:
            ai_engine.model = f"Google Gemini ⚡ ({ai_engine.gemini_model})"
        elif ai_engine.active_engine == "ollama":
            ai_engine.model = f"Ollama Local ({ai_engine.deepseek_model})"
        else:
            ai_engine.model = "Fallback de Segurança (Nenhum motor válido configurado)"
            
        return jsonify({"success": True, "engine_info": ai_engine.model})
    return jsonify({"error": "Motor inválido"}), 400

@app.route('/api/shutdown', methods=['POST'])
def shutdown():
    print("[🛑] Encerrando o servidor BibleAI Network...")
    def stop_server():
        time.sleep(1)
        os._exit(0)
    threading.Thread(target=stop_server).start()
    return jsonify({"success": True, "message": "Servidor sendo desligado com segurança."})

def execute_study_cycle_internal(selected_topic=None, selected_agent_id=None):
    global is_paused
    if is_paused:
        return {"error": "O servidor está pausado."}

    # Bloqueio leve não-bloqueante para evitar conflitos concorrentes
    if not cycle_lock.acquire(blocking=False):
        return {"status": "busy", "message": "Ciclo de estudo já em andamento..."}

    try:
        db = load_db()
        agents = db.get("agents", [])
        topics = db.get("topics", [])
        
        if not agents or not topics:
            return {"error": "Nenhum agente ou pauta configurada"}
            
        past_posts = db.get("posts", [])
        
        # 1. Garante que se o usuário escolheu uma pauta específica, ela seja respeitada
        if selected_topic and str(selected_topic).strip():
            topic = str(selected_topic).strip()
            if topic in topics:
                topics.remove(topic)
            topics.insert(0, topic)
            db["topics"] = topics
            save_db(db)
        else:
            # Pauta Central em Foco: sempre honra a pauta ativa definida pelo usuário (topics[0])
            topic = topics[0] if topics else "Ezequiel 25:17"

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
        num_commenters = min(len(available_commenters), 3)
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
    result = execute_study_cycle_internal(selected_topic, selected_agent_id)
    if "error" in result:
        return jsonify(result), 400
    return jsonify(result)

def background_generation_loop():
    import time
    time.sleep(6)  # Aguarda servidor iniciar
    while True:
        time.sleep(60)  # Interação contínua autônoma equilibrada e anti-duplicação
        global is_paused
        if not is_paused:
            try:
                execute_study_cycle_internal()
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
