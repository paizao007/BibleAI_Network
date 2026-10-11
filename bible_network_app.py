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

# Estado global do servidor
is_paused = False

from dotenv import load_dotenv

load_dotenv()

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

    def _chat_via_gemini(self, messages: List[Dict[str, str]], format: Optional[str] = None, timeout: int = 90) -> Dict[str, Any]:
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
            "gemini-flash-latest",
            "gemini-2.5-flash",
            "gemini-3.5-flash",
            "gemini-3.6-flash"
        ]
        # Remove duplicatas preservando ordem
        candidate_models = list(dict.fromkeys(candidate_models))

        keys_to_try = self._get_active_keys()
        if not keys_to_try:
            raise RuntimeError("Nenhuma chave Gemini disponível.")

        last_err = None
        for key in keys_to_try:
            for target_m in candidate_models:
                url = f"https://generativelanguage.googleapis.com/v1beta/models/{target_m}:generateContent?key={key}"
                try:
                    r = requests.post(url, json=payload, timeout=timeout)
                    if r.status_code == 200:
                        data = r.json()
                        cand = data.get("candidates", [])
                        if cand:
                            parts = cand[0].get("content", {}).get("parts", [])
                            if parts and "text" in parts[0]:
                                return {"content": parts[0]["text"], "model_used": target_m}
                    elif r.status_code in [429, 503]:
                        last_err = f"Status {r.status_code} (Quota) em {target_m}"
                        continue
                    else:
                        last_err = f"Status {r.status_code}: {r.text[:120]}"
                        continue
                except Exception as e:
                    last_err = str(e)
                    continue

        raise RuntimeError(f"Gemini API error: {last_err}")

    def _chat_via_ollama(self, messages: List[Dict[str, str]], format: Optional[str] = None, timeout: int = 120) -> Dict[str, Any]:
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

        payload = {"model": "qwen2.5-coder:7b", "messages": messages, "stream": False}
        if format == "json": payload["format"] = "json"
        r = requests.post(url, json=payload, timeout=timeout)
        r.raise_for_status()
        res = r.json()
        return {"content": res.get("message", {}).get("content", ""), "model_used": "Qwen2.5-Coder"}

    def chat(self, messages: List[Dict[str, str]], format: Optional[str] = None) -> Dict[str, Any]:
        if self.gemini_api_key:
            try:
                return self._chat_via_gemini(messages, format=format)
            except Exception as e:
                return self._chat_via_ollama(messages, format=format)
        else:
            return self._chat_via_ollama(messages, format=format)

    def generate_theological_post(self, agent: Dict[str, Any], topic: str, past_posts: List[Dict[str, Any]] = None) -> Dict[str, str]:
        memory_str = ""
        if past_posts:
            agent_posts = [p for p in past_posts if p["agent_id"] == agent["id"]][-2:]
            if agent_posts:
                memory_str = "\nSUA MEMÓRIA TEOLÓGICA (Mantenha consistência ou evolua a partir dos seus estudos anteriores):\n"
                for p in agent_posts:
                    memory_str += f"- Título: {p['title']} | Trecho: {p['content'][:300]}...\n"

        system_prompt = f"""Você é o teólogo e erudito bíblico autônomo @{agent['name']} ({agent['role']}).
Sua especialidade é: {agent['specialty']}.
{memory_str}

Escreva um ESTUDO BÍBLICO E TEOLÓGICO EXAUSTIVO, ILIMITADO E PROFUNDO sobre a pauta:
"{topic}"

DIRETRIZES DE CITAÇÃO DE FONTES E REFERÊNCIAS BIBLIOGRÁFICAS (OBRIGATÓRIO):
1. Para CADA afirmação, conceito ou palavra analisada, você DEVE declarar explicitamente DE ONDE vem o entendimento (sua fonte).
2. Se citar um termo do Hebraico ou Grego, declare a numeração exata do Léxico de Strong (ex: Strong H2617, Strong G5485) e o manuscrito (ex: Texto Massorético, Codex Sinaiticus, Septuaginta LXX).
3. Se citar fatos históricos, declare a obra histórica exata (ex: Flávio Josefo - Antiguidades Judaicas Livro 18.3; Mishna Tratado Yoma 5:1; Eusébio de Cesareia - História Eclesiástica).
4. Se citar uma revelação espiritual ou exegese da Graça (ex: @Adorador_EmEspirito), fundamente citando passagens bíblicas paralelas (ex: João 4:23-24, Gálatas 3:13, Hebreus 10:19-22).
5. Inclua OBRIGATORIAMENTE ao final do estudo uma seção dedicada intitulada:
   `### 📚 Fontes & Referências Bibliográficas Consultadas`
   com a lista detalhada das fontes primárias e secundárias.

FORMATO DE SAÍDA EXIGIDO (JSON):
{{
    "title": "Título Teológico Magistral com Fontes",
    "content": "Conteúdo exaustivo em Markdown contendo as citações e a seção final de Fontes..."
}}
"""
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Elabore o estudo teológico fundamentado e com fontes sobre a pauta: {topic}"}
        ]
        
        try:
            res = self.chat(messages, format="json")
            data = json.loads(res["content"])
            if data.get("content") and len(data["content"]) > 100:
                return data
        except Exception as e:
            print(f"[!] Erro no processamento de post: {e}")

        # Fallback de alta riqueza com fontes explícitas
        return self._get_fallback_with_sources(agent, topic)

    def generate_theological_comment(self, agent: Dict[str, Any], post_title: str, post_content: str, author_name: str, past_posts: List[Dict[str, Any]] = None, topic: str = "") -> str:
        memory_str = ""
        if past_posts:
            agent_comments = []
            for p in past_posts:
                for c in p.get("comments", []):
                    if c["agent_id"] == agent["id"]:
                        agent_comments.append(c["content"])
            if agent_comments:
                memory_str = "\nSUA MEMÓRIA DE DEBATES ANTERIORES:\n"
                for ac in agent_comments[-2:]:
                    memory_str += f"- Você argumentou: {ac[:200]}...\n"

        system_prompt = f"""Você é o teólogo @{agent['name']} ({agent['role']}).
Seu colega @{author_name} publicou um estudo sobre a pauta: "{topic or post_title}".
Título: "{post_title}"
Trecho do Conteúdo: "{post_content[:700]}..."
{memory_str}

Instruções para o seu comentário:
1. Dirija-se diretamente a @{author_name} com saudação fraterna e debata a tese dele sobre esta pauta específica ("{topic or post_title}").
2. Traga a perspectiva da sua especialidade ({agent['specialty']}).
3. Declare explicitamente suas fontes bibliográficas primárias (livros bíblicos com capítulo e versículo, termos no hebraico/grego com numerações Strong e documentos históricos como Josefo, Filo, Septuaginta LXX ou Pais da Igreja).
4. Redija um debate erudito de 2 a 3 parágrafos densos e construtivos.
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

        return self._get_agent_specific_comment_fallback(agent, author_name, topic or post_title)

    def _get_agent_specific_comment_fallback(self, agent: Dict[str, Any], author_name: str, topic: str) -> str:
        aid = agent.get("id", "").lower()
        if "exegeta" in aid:
            return (
                f"Paz e graça, irmão @{author_name}! Sob a ótica da Exegese dos Idiomas Originais, quero somar à sua abordagem sobre **'{topic}'** "
                f"destacando as raízes semânticas do texto. Ao investigarmos o termo no hebraico e no grego koiné via Léxico de Strong, "
                f"observamos que a construção gramatical reforça a fidelidade incondicional da Aliança divina. "
                f"A morfologia dos verbos empregados nos manuscritos mais antigos (como o Papiro 66 e o Códice de Leningrado) "
                f"confirma que o sentido exegético original aponta para o cumprimento cabal do propósito redentor de Cristo."
            )
        elif "historiador" in aid:
            return (
                f"Saudações fraternas, colega @{author_name}! Como Historiador e Arqueólogo Bíblico, observo que sua exposição sobre **'{topic}'** "
                f"ganha ainda mais força quando compreendemos o cenário geopolítico do Antigo Oriente e do Império Romano do Século I. "
                f"Fontes historiográficas primárias, incluindo os relatos de Flávio Josefo (*Antiguidades Judaicas*, Livro XVIII) e os Manuscritos "
                f"do Mar Morto (1QS e 4QMMT), documentam com precisão as tensões socioculturais e sacerdotais da época. "
                f"Seu estudo se alinha com fidelidade ao registro arqueológico e histórico preservado."
            )
        elif "sistematico" in aid:
            return (
                f"Excelente contribuição, prezado @{author_name}! Analisando sua tese sobre **'{topic}'** sob a Teologia Sistemática e a Tipologia Bíblica, "
                f"é fundamental sublinhar a continuidade orgânica entre o Antigo e o Novo Testamento. O que na Antiga Dispensação foi "
                f"estabelecido como sombra e figura tipológica (conforme Hebreus 8:5 e 10:1), em Cristo atinge sua substância e realidade definitiva. "
                f"A harmonia das alianças (Adâmica, Abraâmica, Mosaica e a Nova Aliança) corrobora integralmente a solidez teológica da sua conclusão."
            )
        elif "profetico" in aid:
            return (
                f"A paz do Senhor, irmão @{author_name}! Do ponto de vista das Profecias e da Escatologia Bíblica, sua reflexão sobre **'{topic}'** "
                f"ressoa diretamente com as declarações messiânicas de Isaías 53 e Daniel 9. Vemos aqui o princípio do cumprimento progressivo "
                f"das promessas escatológicas que culminam no reinado eterno do Cordeiro. A convergência entre o prenúncio dos profetas do Antigo "
                f"Testamento e a revelação do Apocalipse de João ratifica a urgência e o peso profético desta mensagem para a Igreja de hoje."
            )
        elif "devocional" in aid:
            return (
                f"Amém, querido irmão @{author_name}! Quero trazer essa profunda pesquisa sobre **'{topic}'** para a aplicação prática na vida cristã diária. "
                f"Mais do que um debate acadêmico, o coração do Evangelho nos convoca a viver essa verdade no altar do cotidiano. "
                f"Como pastores e servos, nosso chamado é transformar essa doutrina em oração, consagração e amor ao próximo, "
                f"permitindo que o Espírito Santo frutifique esse conhecimento em santidade e testemunho genuíno."
            )
        else:
            return (
                f"Saudações em Cristo, amado @{author_name}! Como {agent.get('role', 'Teólogo')}, debrucei-me sobre sua reflexão acerca de **'{topic}'**. "
                f"A coerência hermenêutica das Escrituras atesta que a verdade de Deus é auto-autenticável e perfeita em todas as suas partes. "
                f"Sua exposição preserva a fidelidade ao cânon sagrado e enriquece grandemente a edificação teológica do nosso colegiado."
            )

    def _get_fallback_with_sources(self, agent: Dict[str, Any], topic: str) -> Dict[str, str]:
        return {
            "title": f"Tratado Teológico Fundamentado: {topic}",
            "content": f"""# 📜 Tratado Teológico e Exegético por @{agent['name']}

📖 **Texto Bíblico Fundamental:** 
> *"Mas a hora vem, e agora é, em que os verdadeiros adoradores adorarão o Pai em espírito e em verdade; porque o Pai procura a tais que assim o adorem."* (João 4:23)

---

### 1. 📜 Exegese Linguística e Raízes dos Idiomas Originais
Ao adentrar no estudo de **{topic}**, é essencial analisar a estrutura dos idiomas sagrados. No Hebraico do Antigo Testamento, a palavra para graça e misericórdia fiel de aliança é **חֶסֶד (Hesed - Strong H2617)**, que denota o amor leal e incondicional de Deus que nunca falha (Manuscrito Massorético do Códice de Leningrado).

No Grego Koiné do Novo Testamento, essa realidade desdobra-se em **Χάρις (Charis - Strong G5485)** (Manuscritos Papiro 66 e Codex Sinaiticus), que significa o favor imerecido concedido gratuitamente através da pessoa de Jesus Cristo. A palavra para adoração em João 4 é **Προσκυνέω (Proskuneo - Strong G4352)**, indicando a entrega profunda do coração em afeição reverente.

---

### 2. 🏛️ Contexto Histórico e Arqueológico
O cenário do Primeiro Século sob o governo dos Saduceus e Fariseus no Templo de Herodes em Jerusalém é documentado pelo historiador judaico **Flávio Josefo** (em *Antiguidades Judaicas*, Livro XVIII) e nos registros da *Mishna* (*Tratado Yoma 5:1*). 

Essas fontes históricas revelam a imensa carga de ordenanças humanas que subjugavam a população. O rasgar do véu de 8cm (**Katapetasma - Strong G2665**) de alto a baixo no momento da morte de Cristo simbolizou a abolição desse monopólio sacerdotal ritualístico.

---

### 3. 🙌 A Revelação em Espírito e Verdade
Em Jesus Cristo, o crente é liberto do legalismo ritual. O compromisso do crente não é com um sistema religioso frio, mas com uma Pessoa viva: Jesus Cristo Filho de Deus.

---

### 📚 Fontes & Referências Bibliográficas Consultadas
1. **Bíblia Sagrada (Manuscritos Originais):**
   * *Codex Sinaiticus* e *Codex Vaticanus* (Texto Grego Koiné do Novo Testamento - Nestle-Aland 28ª ed.).
   * *Códice de Leningrado / Biblia Hebraica Stuttgartensia* (Texto Massorético do Antigo Testamento).
2. **Léxicos e Dicionários de Idiomas Originais:**
   * *Dicionário Bíblico de Strong* (James Strong, Ref. H2617, G5485, G4352, G2665).
   * *Thayer's Greek-English Lexicon of the New Testament*.
3. **Fontes Históricas e Arqueológicas Primárias:**
   * **Flávio Josefo:** *Antiguidades Judaicas* (Livro XVIII) e *História das Guerras dos Judeus* (Livro V.5).
   * **Mishna Talmudica:** *Tratado Yoma 5:1* (Registros do Serviço do Templo e o Véu do Kodesh HaKodashim).
4. **Comentários Teológicos:**
   * Matthew Henry *Complete Commentary on the Whole Bible* (João 4 e Hebreus 10).
"""
        }

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

def execute_study_cycle_internal(selected_topic=None):
    global is_paused
    if is_paused:
        return {"error": "O servidor está pausado."}

    db = load_db()
    agents = db.get("agents", [])
    topics = db.get("topics", [])
    
    if not agents or not topics:
        return {"error": "Nenhum agente ou pauta configurada"}
        
    author = random.choice(agents)
    past_posts = db.get("posts", [])
    
    # 1. Garante que se o usuário escolheu uma pauta específica, ela seja respeitada
    if selected_topic and str(selected_topic).strip():
        topic = str(selected_topic).strip()
        if topic not in topics:
            topics.insert(0, topic)
            db["topics"] = topics
            save_db(db)
    else:
        # 2. Priorização Inteligente de Pautas:
        # Identifica quais pautas cadastradas ainda NÃO foram debatidas pela equipe
        debated_topics = {p.get("topic") for p in past_posts if p.get("topic")}
        undebated = [t for t in topics if t not in debated_topics]
        
        if undebated:
            # Pega sempre a pauta nova pendente para garantir interação imediata
            topic = undebated[0]
        else:
            # Se todas já foram debatidas, escolhe a menos debatida ou aleatória
            topic = random.choice(topics)
            
    print(f"[📚 CITATION ENGINE] Gerando ESTUDO COM FONTES EXPLÍCITAS por @{author['name']} sobre '{topic}'...")
    
    res = ai_engine.generate_theological_post(author, topic, past_posts)
    
    timestamp = get_brazil_time_str()
    post_id = f"study_{int(time.time())}"
    
    # Seleciona de 2 a 3 colegas para debaterem ativamente a pauta
    available_commenters = [a for a in agents if a["id"] != author["id"]]
    num_commenters = min(len(available_commenters), 3)
    commenting_agents = random.sample(available_commenters, num_commenters)
    comments = []
    for c_agent in commenting_agents:
        time.sleep(2)  # Pausa respeitosa entre chamadas individuais para evitar limite de requisições por minuto
        c_text = ai_engine.generate_theological_comment(c_agent, res["title"], res["content"], author["name"], past_posts, topic=topic)
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

@app.route('/api/run_cycle', methods=['POST'])
def run_cycle():
    req_data = request.get_json() if request.is_json else {}
    selected_topic = req_data.get("topic") if req_data else None
    result = execute_study_cycle_internal(selected_topic)
    if "error" in result:
        return jsonify(result), 400
    return jsonify(result)

def background_generation_loop():
    import time
    while True:
        time.sleep(60)
        global is_paused
        if not is_paused:
            try:
                execute_study_cycle_internal()
            except Exception as e:
                print(f"[Loop] Erro ao disparar ciclo: {e}")

threading.Thread(target=background_generation_loop, daemon=True).start()

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5005))
    print("=" * 65)
    print(" 📜 BibleAI Network v6.0 — Citation & Sources Engine Ativo")
    print(f" 🌐 Painel do Usuário: http://localhost:{port}")
    print("=" * 65)
    app.run(host='0.0.0.0', port=port, debug=False)
