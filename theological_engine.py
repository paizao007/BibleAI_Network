# -*- coding: utf-8 -*-
"""
Theological Knowledge Engine - BibleAI Network v7.1
Motor Exegético, Histórico, Tipológico, Doxológico & Anti-Repetição.
Garante:
1. Especialização autêntica para cada tema (sem misturar Ezequiel com João 4 ou outras passagens).
2. Diversidade absoluta entre os 7 eruditos (cada persona produz um tratado com estilo, estrutura e ênfase próprios).
3. Debates dinâmicos com múltiplos ângulos por persona (elimina repetições e comentários idênticos).
4. Fidelidade bíblica e histórica estrita, sem anacronismos.
5. Adoração em Espírito e em Verdade (João 4:23-24).
"""

import os
import json
import random
import re
import unicodedata
from typing import Dict, Any, List, Optional

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ACF_BIBLE_PATH = os.path.join(BASE_DIR, "database", "biblia_completa_acf.json")

_ACF_BIBLE_CACHE: Dict[str, List[List[str]]] = {}

def _strip_accents(s: str) -> str:
    if not s:
        return ""
    return "".join(
        c for c in unicodedata.normalize("NFD", s)
        if unicodedata.category(c) != "Mn"
    )

def load_acf_bible() -> Dict[str, List[List[str]]]:
    """Carrega em memória os 66 livros, 1.189 capítulos e 31.106 versículos da Bíblia Almeida Corrigida Fiel (ACF) 100% Offline."""
    global _ACF_BIBLE_CACHE
    if _ACF_BIBLE_CACHE:
        return _ACF_BIBLE_CACHE
    if os.path.exists(ACF_BIBLE_PATH):
        try:
            with open(ACF_BIBLE_PATH, "r", encoding="utf-8-sig") as f:
                raw_books = json.load(f)
            for b in raw_books:
                b_name = b.get("name", "").strip()
                b_chapters = b.get("chapters", [])
                if b_name and b_chapters:
                    _ACF_BIBLE_CACHE[b_name.lower()] = b_chapters
                    _ACF_BIBLE_CACHE[_strip_accents(b_name.lower())] = b_chapters
        except Exception as e:
            print(f"[!] Erro ao carregar Bíblia ACF offline: {e}")
    return _ACF_BIBLE_CACHE

def fetch_acf_scripture(book_name: str, chap: Optional[int] = None, v_start: Optional[int] = None, v_end: Optional[int] = None) -> Dict[str, Any]:
    """
    Busca literalmente o capítulo e os versículos exatos na Bíblia Sagrada ACF (31.106 versículos).
    Retorna:
      - ref_display: ex. 'Apocalipse 16:1-21' ou 'Apocalipse 16:16'
      - target_verses_text: texto exato do(s) versículo(s) em foco
      - full_chapter_formatted: todos os versículos numerados do capítulo para leitura integral do agente
      - verses_list: lista de tuplas (num_versiculo, texto)
      - total_chapters: total de capítulos do livro
    """
    bible = load_acf_bible()
    b_key = book_name.lower().strip()
    chapters = bible.get(b_key) or bible.get(_strip_accents(b_key))
    if not chapters:
        return {}

    total_chaps = len(chapters)
    chap_idx = (chap - 1) if (chap and 1 <= chap <= total_chaps) else 0
    chap_num = chap_idx + 1
    verses = chapters[chap_idx]
    total_verses = len(verses)

    all_verses_tuples = [(i + 1, v_txt) for i, v_txt in enumerate(verses)]
    full_chapter_lines = [f"**v. {num}:** {txt}" for num, txt in all_verses_tuples]
    full_chapter_formatted = "\n".join(full_chapter_lines)

    if v_start and 1 <= v_start <= total_verses:
        end_v = v_end if (v_end and v_start <= v_end <= total_verses) else v_start
        selected = all_verses_tuples[v_start - 1 : end_v]
        if v_start == end_v:
            ref_display = f"{book_name} {chap_num}:{v_start}"
            target_text = f"({ref_display}) \"{selected[0][1]}\""
        else:
            ref_display = f"{book_name} {chap_num}:{v_start}-{end_v}"
            target_text = " ".join([f"(v. {n}) {t}" for n, t in selected])
    else:
        if chap:
            ref_display = f"{book_name} {chap_num}:1-{total_verses}"
        else:
            ref_display = f"{book_name} (Capítulo 1:1-{total_verses} — Livro com {total_chaps} capítulos)"
        # Se o capítulo tiver até 12 versículos, mostra todos no destaque; se for maior, mostra os versículos de abertura e clímax + capítulo completo abaixo
        if total_verses <= 12:
            target_text = " ".join([f"(v. {n}) {t}" for n, t in all_verses_tuples])
        else:
            head_part = [f"(v. {n}) {t}" for n, t in all_verses_tuples[:3]]
            mid_idx = total_verses // 2
            mid_part = [f"(v. {n}) {t}" for n, t in all_verses_tuples[max(3, mid_idx - 1):min(total_verses - 2, mid_idx + 2)]]
            tail_part = [f"(v. {n}) {t}" for n, t in all_verses_tuples[-3:]]
            combined = head_part + ["..."] + mid_part + ["..."] + tail_part
            target_text = " ".join(combined)

    return {
        "ref_display": ref_display,
        "chapter_num": chap_num,
        "total_chapters": total_chaps,
        "total_verses": total_verses,
        "target_verses_text": target_text,
        "full_chapter_formatted": full_chapter_formatted,
        "verses_list": all_verses_tuples,
        "requested_v_start": v_start,
        "requested_v_end": v_end,
    }

def search_acf_by_keywords(query: str, max_results: int = 8) -> List[Dict[str, str]]:
    """
    Busca textual reversa em todos os 31.106 versículos da Bíblia ACF quando o usuário
    digita um tema livre (ex: 'Armagedom', 'Melquisedeque', 'Vale de Ossos Secos', 'Cego de Jericó').
    """
    bible = load_acf_bible()
    if not bible or not query:
        return []
    stop_words = {
        "de", "do", "da", "dos", "das", "em", "no", "na", "nos", "nas", "um", "uma",
        "o", "a", "os", "as", "e", "ou", "para", "por", "com", "sem", "sob", "sobre",
        "que", "como", "qual", "quais", "estudo", "biblico", "pauta", "capitulo", "versiculo"
    }
    raw_tokens = re.findall(r"[a-záàâãéêíóôõúç]{3,}", query.lower())
    tokens = [t for t in raw_tokens if _strip_accents(t) not in stop_words]
    if not tokens:
        return []

    norm_tokens = [_strip_accents(t) for t in tokens]
    matches = []
    seen_books = set()
    for book_key, info in BIBLE_CANON_REGISTRY.items():
        b_name = info["name"]
        if b_name in seen_books:
            continue
        seen_books.add(b_name)
        chaps = bible.get(b_name.lower()) or bible.get(_strip_accents(b_name.lower()))
        if not chaps:
            continue
        for c_idx, verses in enumerate(chaps):
            for v_idx, v_text in enumerate(verses):
                v_norm = _strip_accents(v_text.lower())
                score = sum(2 if nt in v_norm.split() else (1 if nt in v_norm else 0) for nt in norm_tokens)
                if score >= max(1, len(norm_tokens)):
                    matches.append({
                        "score": score,
                        "ref": f"{b_name} {c_idx + 1}:{v_idx + 1}",
                        "book_name": b_name,
                        "chapter": c_idx + 1,
                        "verse": v_idx + 1,
                        "text": v_text
                    })
    matches.sort(key=lambda x: x["score"], reverse=True)
    return matches[:max_results]

# ==============================================================================
# 📖 REGISTRO CANÔNICO DOS 66 LIVROS DA BÍBLIA & PARSER EXEGÉTICO UNIVERSAL
# Garante que NUNCA um tema caia em livros errados ou anacronismos
# ==============================================================================

BIBLE_CANON_REGISTRY = {
    # Antigo Testamento (39 Livros)
    "gênesis": {"name": "Gênesis", "abbrev": ["gn", "gen", "genesis"], "testament": "AT", "lang": "Hebraico", "era": "Período Patriarcal / Pentateuco Mosaico (c. 1446-1406 a.C.)"},
    "êxodo": {"name": "Êxodo", "abbrev": ["ex", "exo", "exodo"], "testament": "AT", "lang": "Hebraico", "era": "Saída do Egito & Aliança do Sinai (c. 1446 a.C.)"},
    "levítico": {"name": "Levítico", "abbrev": ["lv", "lev", "levitico"], "testament": "AT", "lang": "Hebraico", "era": "Sacerdócio Levítico & Leis de Santidade no Tabernáculo"},
    "números": {"name": "Números", "abbrev": ["nm", "num", "numeros"], "testament": "AT", "lang": "Hebraico", "era": "Peregrinação no Deserto de Parã (c. 1445-1406 a.C.)"},
    "deuteronômio": {"name": "Deuteronômio", "abbrev": ["dt", "deut", "deuteronomio"], "testament": "AT", "lang": "Hebraico", "era": "Campinas de Moabe / Renovação da Aliança Mosaica (c. 1406 a.C.)"},
    "josué": {"name": "Josué", "abbrev": ["js", "jos", "josue"], "testament": "AT", "lang": "Hebraico", "era": "Conquista de Canaã e Repartição das Tribos (c. 1400 a.C.)"},
    "juízes": {"name": "Juízes", "abbrev": ["jz", "jui", "juizes"], "testament": "AT", "lang": "Hebraico", "era": "Período da Teocracia e dos Juízes de Israel (c. 1380-1050 a.C.)"},
    "rute": {"name": "Rute", "abbrev": ["rt", "rut", "rute"], "testament": "AT", "lang": "Hebraico", "era": "Época dos Juízes / Belém de Judá e o Parente Remidor"},
    "1 samuel": {"name": "1 Samuel", "abbrev": ["1sm", "1sam", "1 samuel", "i samuel"], "testament": "AT", "lang": "Hebraico", "era": "Transição Teocrática para a Monarquia de Davi (c. 1050-1010 a.C.)"},
    "2 samuel": {"name": "2 Samuel", "abbrev": ["2sm", "2sam", "2 samuel", "ii samuel"], "testament": "AT", "lang": "Hebraico", "era": "Reinado de Davi em Jerusalém & Aliança Davídica (c. 1010-970 a.C.)"},
    "1 reis": {"name": "1 Reis", "abbrev": ["1rs", "1reis", "1 reis", "i reis"], "testament": "AT", "lang": "Hebraico", "era": "Reinado de Salomão, Templo de Jerusalém & Divisão do Reino (c. 970-850 a.C.)"},
    "2 reis": {"name": "2 Reis", "abbrev": ["2rs", "2reis", "2 reis", "ii reis"], "testament": "AT", "lang": "Hebraico", "era": "Queda de Samaria e Exílio na Babilônia (c. 850-586 a.C.)"},
    "1 crônicas": {"name": "1 Crônicas", "abbrev": ["1cr", "1cron", "1 cronicas", "i cronicas"], "testament": "AT", "lang": "Hebraico", "era": "Genealogias Sagradas & Adoração Davídica no Templo"},
    "2 crônicas": {"name": "2 Crônicas", "abbrev": ["2cr", "2cron", "2 cronicas", "ii cronicas"], "testament": "AT", "lang": "Hebraico", "era": "História Espiritual dos Reis de Judá e Glória do Templo"},
    "esdras": {"name": "Esdras", "abbrev": ["ed", "esd", "esdras"], "testament": "AT", "lang": "Hebraico", "era": "Retorno do Cativeiro Babilônico & Reconstrução do Templo (c. 538-458 a.C.)"},
    "neemias": {"name": "Neemias", "abbrev": ["ne", "neem", "neemias"], "testament": "AT", "lang": "Hebraico", "era": "Reconstrução dos Muros de Jerusalém & Avivamento da Lei (c. 445 a.C.)"},
    "ester": {"name": "Ester", "abbrev": ["et", "est", "ester"], "testament": "AT", "lang": "Hebraico", "era": "Império Persa / Providência Soberana em Susã (c. 483-473 a.C.)"},
    "jó": {"name": "Jó", "abbrev": ["job", "jó"], "testament": "AT", "lang": "Hebraico", "era": "Terra de Uz / Literatura Sapiencial e a Soberania Divina no Sofrimento"},
    "salmos": {"name": "Salmos", "abbrev": ["sl", "sal", "salmo", "salmos", "slm"], "testament": "AT", "lang": "Hebraico", "era": "Culto e Louvor Teocrático no Templo de Sião (Davi, Asafe, Corá)"},
    "provérbios": {"name": "Provérbios", "abbrev": ["pv", "prv", "prov", "proverbios"], "testament": "AT", "lang": "Hebraico", "era": "Sabedoria Prática e Temor de Yahweh na Monarquia de Salomão"},
    "eclesiastes": {"name": "Eclesiastes", "abbrev": ["ec", "ecl", "eclesiastes"], "testament": "AT", "lang": "Hebraico", "era": "O Pregador (Qohelet) / Reflexão sobre a Vaidade e o Temor a Deus"},
    "cantares": {"name": "Cantares", "abbrev": ["ct", "cant", "cantares", "cânticos", "canticos"], "testament": "AT", "lang": "Hebraico", "era": "Poesia Lírica de Amor Conjugal e Tipologia do Amor Divino"},
    "isaías": {"name": "Isaías", "abbrev": ["is", "isa", "isai", "isaias"], "testament": "AT", "lang": "Hebraico", "era": "Profecia Messiânica em Jerusalém / Reino de Judá (c. 740-680 a.C.)"},
    "jeremias": {"name": "Jeremias", "abbrev": ["jr", "jer", "jeremias"], "testament": "AT", "lang": "Hebraico", "era": "Queda de Jerusalém & Promessa da Nova Aliança (c. 627-580 a.C.)"},
    "lamentações": {"name": "Lamentações", "abbrev": ["lm", "lam", "lamentacoes"], "testament": "AT", "lang": "Hebraico", "era": "Elegias Fúnebres sobre a Destruição do Primeiro Templo (586 a.C.)"},
    "ezequiel": {"name": "Ezequiel", "abbrev": ["ez", "eze", "ezeq", "ezequiel"], "testament": "AT", "lang": "Hebraico", "era": "Exílio Babilônico junto ao Rio Quebar (c. 593-571 a.C.)"},
    "daniel": {"name": "Daniel", "abbrev": ["dn", "dan", "daniel"], "testament": "AT", "lang": "Hebraico", "era": "Corte Real Babilônica e Medo-Persa / Profecias Apocalípticas (c. 605-536 a.C.)"},
    "oséias": {"name": "Oséias", "abbrev": ["os", "ose", "oseias"], "testament": "AT", "lang": "Hebraico", "era": "Amor Fiel de Deus pelo Povo Infiel / Reino do Norte (c. 750 a.C.)"},
    "joel": {"name": "Joel", "abbrev": ["jl", "joe", "joel"], "testament": "AT", "lang": "Hebraico", "era": "Praga de Gafanhotos & Derramamento do Espírito no Dia do Senhor"},
    "amós": {"name": "Amós", "abbrev": ["am", "amo", "amos"], "testament": "AT", "lang": "Hebraico", "era": "Justiça Social e Retidão Moral perante Deus em Israel (c. 760 a.C.)"},
    "obadias": {"name": "Obadias", "abbrev": ["ob", "oba", "obd", "obadias"], "testament": "AT", "lang": "Hebraico", "era": "Oráculo de Juízo contra a Soberba e Violência de Edom"},
    "jonas": {"name": "Jonas", "abbrev": ["jn", "jon", "jonas"], "testament": "AT", "lang": "Hebraico", "era": "Missão em Nínive e a Soberana Misericórdia de Yahweh aos Gentios"},
    "miqueias": {"name": "Miqueias", "abbrev": ["mq", "miq", "miqueias"], "testament": "AT", "lang": "Hebraico", "era": "Profecia do Nascimento do Messias em Belém de Efrata (c. 735-700 a.C.)"},
    "naum": {"name": "Naum", "abbrev": ["na", "nau", "naum"], "testament": "AT", "lang": "Hebraico", "era": "Juízo Irrevogável sobre a Cidade Sanguinária de Nínive (c. 663-612 a.C.)"},
    "habacuque": {"name": "Habacuque", "abbrev": ["hc", "hab", "habacuque"], "testament": "AT", "lang": "Hebraico", "era": "O Justo Viverá pela sua Fé perante o Mistério Divino (c. 605 a.C.)"},
    "sofonias": {"name": "Sofonias", "abbrev": ["sf", "sof", "sofonias"], "testament": "AT", "lang": "Hebraico", "era": "O Grande Dia da Ira de Deus & Restauração de um Remanescente Humilde"},
    "ageu": {"name": "Ageu", "abbrev": ["ag", "age", "ageu"], "testament": "AT", "lang": "Hebraico", "era": "Reconstrução do Segundo Templo no Pós-Exílio Babilônico (520 a.C.)"},
    "zacarias": {"name": "Zacarias", "abbrev": ["zc", "zac", "zacarias"], "testament": "AT", "lang": "Hebraico", "era": "Visões Escatológicas e o Rei Humilde que Entra em Sião (c. 520-480 a.C.)"},
    "malaquias": {"name": "Malaquias", "abbrev": ["ml", "mal", "malaquias"], "testament": "AT", "lang": "Hebraico", "era": "Último Oráculo Profético / O Sol da Justiça que Nasce (c. 430 a.C.)"},
    # Novo Testamento (27 Livros)
    "mateus": {"name": "Mateus", "abbrev": ["mt", "mat", "mateus"], "testament": "NT", "lang": "Grego", "era": "Evangelho Messiânico para a Comunidade Judaica (Séc. I d.C.)"},
    "marcos": {"name": "Marcos", "abbrev": ["mc", "mar", "marcos"], "testament": "NT", "lang": "Grego", "era": "Evangelho do Servo Sofredor e Filho de Deus em Ação (c. 55-65 d.C.)"},
    "lucas": {"name": "Lucas", "abbrev": ["lc", "luc", "lucas"], "testament": "NT", "lang": "Grego", "era": "Evangelho Histórico / O Salvador de Todas as Nações e Humildes (c. 60 d.C.)"},
    "joão": {"name": "João", "abbrev": ["jo", "joa", "joao"], "testament": "NT", "lang": "Grego", "era": "Evangelho Espiritual / O Logos Divino Encarnado (c. 85-95 d.C.)"},
    "atos": {"name": "Atos", "abbrev": ["at", "act", "atos"], "testament": "NT", "lang": "Grego", "era": "Pentecostes e a Expansão do Evangelho no Império Romano (c. 30-62 d.C.)"},
    "romanos": {"name": "Romanos", "abbrev": ["rm", "rom", "romanos"], "testament": "NT", "lang": "Grego", "era": "Tratado Monumental da Justificação pela Fé & Graça Soberana (c. 57 d.C.)"},
    "1 coríntios": {"name": "1 Coríntios", "abbrev": ["1co", "1cor", "1 corintios", "i corintios"], "testament": "NT", "lang": "Grego", "era": "Correção Pastoral em Corinto / Cruz, Ceia e Ressurreição (c. 55 d.C.)"},
    "2 coríntios": {"name": "2 Coríntios", "abbrev": ["2co", "2cor", "2 corintios", "ii corintios"], "testament": "NT", "lang": "Grego", "era": "Defesa do Ministério Apostólico & Tesouro em Vasos de Barro (c. 56 d.C.)"},
    "gálatas": {"name": "Gálatas", "abbrev": ["gl", "gal", "galatas"], "testament": "NT", "lang": "Grego", "era": "A Magna Carta da Liberdade Cristã contra o Legalismo Judaizante (c. 49-55 d.C.)"},
    "efésios": {"name": "Efésios", "abbrev": ["ef", "efe", "efesios"], "testament": "NT", "lang": "Grego", "era": "O Mistério da Igreja, Unidade em Cristo & Armadura de Deus (c. 60-62 d.C.)"},
    "filipenses": {"name": "Filipenses", "abbrev": ["fp", "fil", "filipenses"], "testament": "NT", "lang": "Grego", "era": "Alegria no Cárcere / O Esvaziamento (Kenosis) de Cristo (c. 61 d.C.)"},
    "colossenses": {"name": "Colossenses", "abbrev": ["cl", "col", "colossenses"], "testament": "NT", "lang": "Grego", "era": "A Supremacia Cósmica e Plenitude de Cristo sobre Toda a Criação (c. 60-62 d.C.)"},
    "1 tessalonicenses": {"name": "1 Tessalonicenses", "abbrev": ["1ts", "1tes", "1 tessalonicenses", "i tessalonicenses"], "testament": "NT", "lang": "Grego", "era": "Santificação, Consolação e a Bendita Esperança do Arrebatamento (c. 51 d.C.)"},
    "2 tessalonicenses": {"name": "2 Tessalonicenses", "abbrev": ["2ts", "2tes", "2 tessalonicenses", "ii tessalonicenses"], "testament": "NT", "lang": "Grego", "era": "O Dia do Senhor, o Mistério da Iniquidade & Perseverança Cristã (c. 51-52 d.C.)"},
    "1 timóteo": {"name": "1 Timóteo", "abbrev": ["1tm", "1tim", "1 timoteo", "i timoteo"], "testament": "NT", "lang": "Grego", "era": "Sã Doutrina, Liderança Pastoral e Piedade Cristã em Éfeso (c. 63 d.C.)"},
    "2 timóteo": {"name": "2 Timóteo", "abbrev": ["2tm", "2tim", "2 timoteo", "ii timoteo"], "testament": "NT", "lang": "Grego", "era": "Testamento Final de Paulo na Prisão Mamertina em Roma (c. 67 d.C.)"},
    "tito": {"name": "Tito", "abbrev": ["tt", "tit", "tito"], "testament": "NT", "lang": "Grego", "era": "Ordem nas Igrejas de Creta & Boas Obras Decorrentes da Graça (c. 63-65 d.C.)"},
    "filemom": {"name": "Filemom", "abbrev": ["fm", "flm", "filemom"], "testament": "NT", "lang": "Grego", "era": "Perdão Fraterno, Igualdade em Cristo e o Escravo Onésimo (c. 60-62 d.C.)"},
    "hebreus": {"name": "Hebreus", "abbrev": ["hb", "heb", "hebreus"], "testament": "NT", "lang": "Grego", "era": "A Superioridade Eterna de Cristo sobre Anjos, Moisés e Sacerdócio (c. 65-69 d.C.)"},
    "tiago": {"name": "Tiago", "abbrev": ["tg", "tia", "tiago"], "testament": "NT", "lang": "Grego", "era": "A Fé Viva Demonstrada em Obras de Amor e Justiça Prática (c. 45-48 d.C.)"},
    "1 pedro": {"name": "1 Pedro", "abbrev": ["1pe", "1ped", "1 pedro", "i pedro"], "testament": "NT", "lang": "Grego", "era": "Esperança Viva em Meio ao Sofrimento e Provação sob Nero (c. 64 d.C.)"},
    "2 pedro": {"name": "2 Pedro", "abbrev": ["2pe", "2ped", "2 pedro", "ii pedro"], "testament": "NT", "lang": "Grego", "era": "Crescimento na Graça, Alerta contra Hereges & Novos Céus e Terra (c. 66 d.C.)"},
    "1 joão": {"name": "1 João", "abbrev": ["1jo", "1joa", "1 joao", "i joao"], "testament": "NT", "lang": "Grego", "era": "Comunhão com Deus que é Luz e Amor / Certeza da Salvação (c. 90 d.C.)"},
    "2 joão": {"name": "2 João", "abbrev": ["2jo", "2joa", "2 joao", "ii joao"], "testament": "NT", "lang": "Grego", "era": "Andar na Verdade e Amor / Rejeição aos Enganadores Docetistas (c. 90 d.C.)"},
    "3 joão": {"name": "3 João", "abbrev": ["3jo", "3joa", "3 joao", "iii joao"], "testament": "NT", "lang": "Grego", "era": "Hospitalidade aos Cooperadores da Verdade / Alerta contra Diótrefes (c. 90 d.C.)"},
    "judas": {"name": "Judas", "abbrev": ["jd", "jud", "judas"], "testament": "NT", "lang": "Grego", "era": "Batalha Diligente pela Fé que uma vez foi Dada aos Santos (c. 65-80 d.C.)"},
    "apocalipse": {"name": "Apocalipse", "abbrev": ["ap", "apc", "apoc", "apocalipse", "revelação", "revelacao"], "testament": "NT", "lang": "Grego", "era": "Revelação do Cordeiro Triunfante na Ilha de Patmos (c. 95 d.C.)"}
}

def parse_biblical_pericope(text: str) -> Optional[Dict[str, Any]]:
    """
    Detecta qualquer livro bíblico (dos 66 livros), capítulo e versículo em português e abreviações.
    Suporta formatos: 'Apocalipse 16', 'apc 16:16', 'Apocalipse 16:15-16', 'Apocalipse 16 v. 16', 'Apocalipse cap 16 versiculo 16', 'João 3.16'.
    """
    if not text:
        return None
    t_raw = text.lower().replace("º", "").replace("°", "")
    t_norm = _strip_accents(t_raw)

    # Ordena priorizando livros numerados ('1 joão' antes de 'joão', '1 reis' antes de 'reis', etc.)
    ordered_items = sorted(
        BIBLE_CANON_REGISTRY.items(),
        key=lambda kv: (0 if kv[0][0].isdigit() else 1, -len(kv[0]))
    )

    for book_key, info in ordered_items:
        raw_patterns = [info["name"].lower()] + info["abbrev"]
        # Ordena padrões do mais longo para o mais curto
        patterns = sorted(set(raw_patterns), key=len, reverse=True)
        for p in patterns:
            p_norm = _strip_accents(p.lower())
            # Caso especial: "jó" com acento no texto original vs "jo" (abreviação de João)
            if book_key == "jó" and p == "jó":
                target_str = t_raw
                pat_str = "jó"
            elif book_key == "joão" and p_norm == "jo":
                # Evita que a abreviação 'jo' (João) capture 'jó' (com acento) no texto original
                if re.search(r'(?<![a-z0-9])jó(?!\w)', t_raw):
                    continue
                target_str = t_norm
                pat_str = "jo"
            else:
                target_str = t_norm
                pat_str = p_norm

            # Abreviações curtas (<= 3 letras, ex: 'os', 'na', 'et', 'ag', 'ap', 'jo') exigem número de capítulo logo após
            if len(pat_str) <= 3 and pat_str not in ("jó", "job", "rute"):
                regex = (
                    r'(?<![a-z0-9])' + re.escape(pat_str) +
                    r'\.?\s*(?:cap(?:itulo)?\.?\s*)?(\d+)'
                    r'(?:\s*(?:[:\.,]|v(?:ers(?:iculo)?s?)?\.?)\s*(\d+)(?:\s*[-aà]\s*(\d+))?)?'
                )
            else:
                regex = (
                    r'(?<![a-z0-9])' + re.escape(pat_str) +
                    r'(?!\w)\s*(?:cap(?:itulo)?\.?\s*)?(\d+)?'
                    r'(?:\s*(?:[:\.,]|v(?:ers(?:iculo)?s?)?\.?)\s*(\d+)(?:\s*[-aà]\s*(\d+))?)?'
                )

            m = re.search(regex, target_str)
            if m:
                chap = int(m.group(1)) if m.group(1) else None
                v_start = int(m.group(2)) if m.group(2) else None
                v_end = int(m.group(3)) if m.group(3) else None
                # Se digitou "jo 42" sem acento e o capítulo é > 21, trata-se do livro de Jó (42 capítulos)
                resolved_key = book_key
                resolved_info = info
                if book_key == "joão" and pat_str == "jo" and chap and chap > 21:
                    resolved_key = "jó"
                    resolved_info = BIBLE_CANON_REGISTRY["jó"]
                ref_str = resolved_info["name"]
                if chap:
                    ref_str += f" {chap}"
                    if v_start:
                        ref_str += f":{v_start}"
                        if v_end:
                            ref_str += f"-{v_end}"
                return {
                    "book_key": resolved_key,
                    "book_info": resolved_info,
                    "chapter": chap,
                    "v_start": v_start,
                    "v_end": v_end,
                    "reference": ref_str,
                    "testament": resolved_info["testament"],
                    "lang": resolved_info["lang"],
                    "era": resolved_info["era"]
                }
    return None

def clean_theological_hallucinations(text: str) -> str:
    """Higieniza desvios semânticos e garante pontuação final sem cortes artificiais."""
    if not text:
        return text
    cleaned = text.strip()
    cleaned = re.sub(r'\bGalat[eé]us\b', 'Gálatas', cleaned, flags=re.IGNORECASE)
    cleaned = re.sub(r'\blivro das Coleções\b', 'Epístolas Paulinas', cleaned, flags=re.IGNORECASE)
    cleaned = re.sub(r'\bColeções \(Colossenses, Efésios\)\b', 'Epístolas Paulinas (Colossenses e Efésios)', cleaned, flags=re.IGNORECASE)
    if "fruto" in cleaned.lower() and "gênesis 2:7" in cleaned.lower():
        cleaned = re.sub(r'Gênesis 2:7', 'Gálatas 5:22-23', cleaned, flags=re.IGNORECASE)

    # Se faltar pontuação terminal por qualquer razão, adiciona ponto final respeitoso
    valid_endings = ('.', '!', '?', '"', '”', '’', ')', ']', '*')
    if cleaned and not cleaned.endswith(valid_endings):
        cleaned += "."

    return cleaned


THEOLOGICAL_TOPICS_DATABASE = {
    "fruto_do_espirito": {
        "keywords": [
            "fruto do espírito", "fruto do espirito", "fruto do espirito e a santificação", 
            "fruto do espírito e a santificação", "santificação", "santificacao", 
            "gálatas 5", "galatas 5", "gálatas 5:22", "galatas 5:22", 
            "obras da carne", "andar no espírito", "andar no espirito"
        ],
        "verse_ref": "Gálatas 5:22-23",
        "verse_text": "Mas o fruto do Espírito é: amor, gozo, paz, longanimidade, benignidade, bondade, fidelidade, mansidão, domínio próprio. Contra estas coisas não há lei.",
        "era": "Século I d.C. (c. 49-55 d.C. - Período Apostólico / Epístola aos Gálatas)",
        "historical_context": (
            "1. **A Crise dos Gálatas e a Carta da Liberdade Cristã (Século I d.C.):**\n"
            "   O apóstolo Paulo redige a epístola às igrejas da Galácia para combater a infiltração dos judaizantes legalistas, que insistiam na imposição da circuncisão e da Lei Mosaica como requisito para a justificação. Paulo desmonta o legalismo provando que a salvação é unicamente pela graça mediante a fé, e que a verdadeira liberdade cristã não conduz à licenciosidade da carne, mas ao discipulado sob o poder regenerador do Espírito Santo.\n\n"
            "2. **Evidências Papirológicas e Manuscritos Antigos:**\n"
            "   A perícope de Gálatas 5:22-23 é preservada com fidelidade impressionante nos manuscritos mais antigos do Novo Testamento, notadamente no Papiro 46 (P46, c. 200 d.C., na Coleção Chester Beatty) e nos grandes unciais do século IV — o Codex Sinaiticus e o Codex Vaticanus —, atestando a integridade irrevogável da revelação apostólica sobre o fruto da graça."
        ),
        "typological_context": (
            "1. **Da Lei Escrita em Tábuas de Pedra ao Espírito Escrito no Coração:**\n"
            "   O fruto do Espírito é o cumprimento vivo da profecia da Nova Aliança de Jeremias 31:33 e Ezequiel 36:26-27: 'Porei dentro de vós o meu Espírito e farei que andeis nos meus estatutos'. A Lei exigia justiça do homem pecador de fora para dentro, mas o Espírito Santo produz a justiça divina de dentro para fora, gerando uma nova natureza em Cristo Jesus.\n\n"
            "2. **O Fruto Singular (*karpos*) em Contraste com as Obras Plurais (*erga*):**\n"
            "   Paulo contrasta intencionalmente as 'obras da carne' (no plural, refletindo a divisão caótica, egoísta e fragmentada do pecado) com o 'fruto do Espírito' (no singular grego *karpos*). O fruto é um único cacho divino indissolúvel cuja seiva é o amor (*agapē*), desdobrando-se harmonicamente em todas as virtudes de Cristo na vida do crente."
        ),
        "application_context": (
            "1. **Santificação Real vs. Moralismo Religioso:**\n"
            "   O fruto não é produzido por esforço próprio farisaico, mas pelo permanecer na Videira Verdadeira (João 15:5). Santificação não é cumprir rituais vazios, mas a ação viva do Espírito que mortifica as inclinações da carne e conforma o caráter do crente à imagem de Jesus.\n\n"
            "2. **Adoração em Espírito e em Verdade no Cotidiano:**\n"
            "   A maior evidência da adoração autêntica perante o Trono da Graça não são palavras eloquentes, mas a manifestação do fruto santo no lar, na igreja e na sociedade, honrando a Deus em pureza, paz e mansidão."
        ),
        "greek_terms": [
            ("καρπός", "karpos", "Strong G2590", "https://biblehub.com/greek/2590.htm", "Fruto (substantivo singular coletivo). Revela a unidade orgânica indissolúvel das virtudes cristãs, geradas pela seiva viva do Espírito."),
            ("ἀγάπη", "agapē", "Strong G26", "https://biblehub.com/greek/26.htm", "Amor sacrificial, incondicional e voluntário de Deus, raiz primordial de onde brotam todos os demais aspectos do fruto."),
            ("μακροθυμία", "makrothumia", "Strong G3115", "https://biblehub.com/greek/3115.htm", "Longanimidade e paciência heroica perante afrontas e sofrimentos, sem revide ou vingança."),
            ("χρηστότης", "chrēstotēs", "Strong G5544", "https://biblehub.com/greek/5544.htm", "Benignidade, doçura de espírito e disposição generosa de acolher e fazer o bem ao próximo."),
            ("ἐγκράτεια", "enkrateia", "Strong G1466", "https://biblehub.com/greek/1466.htm", "Domínio próprio, autodomínio santo e governo das paixões sob a autoridade soberana do Espírito.")
        ],
        "hebrew_parallels": [
            ("פְּרִי", "peri", "Strong H6529", "https://biblehub.com/hebrew/6529.htm", "Fruto e produção vital. Como a árvore plantada junto a correntes de águas que dá o seu fruto na estação própria (Salmo 1:3)."),
            ("קָדַשׁ", "qadash", "Strong H6942", "https://biblehub.com/hebrew/6942.htm", "Santificar, consagrar e separar exclusivamente para Yahweh, refletindo Sua pureza impecável."),
            ("עֲנָוָה", "anavah", "Strong H6038", "https://biblehub.com/hebrew/6038.htm", "Mansidão santa e humildade profunda perante o Senhor e o próximo.")
        ]
    },
    "ezequiel_25_17": {
        "keywords": ["ezequiel 25:17", "ezequiel 25", "ezequiel", "vingança", "vinganças", "furiosos castigos"],
        "verse_ref": "Ezequiel 25:17",
        "verse_text": "E executarei neles grandes vinganças, com furiosos castigos; e saberão que eu sou o SENHOR, quando eu tiver exercido a minha vingança sobre eles.",
        "era": "Exílio Babilônico (século VI a.C. / c. 586 a.C.)",
        "historical_context": (
            "1. **O Cenário Histórico do Exílio Babilônico (Século VI a.C. - c. 586 a.C.):**\n"
            "   O profeta Ezequiel exercia seu ministério na Babilônia, junto ao rio Quebar, entre os cativos de Judá. O capítulo 25 marca uma transição solene no livro: após a trágica queda e destruição de Jerusalém e do Templo de Salomão pelo exército caldeu de Nabucodonosor II (586 a.C.), Yahweh volta Sua voz judicial contra as nações circunvizinhas — Amon, Moabe, Edom e a Filisteia (vv. 15-17). Esses povos vizinhos não apenas se alegraram com a ruína de Sião, mas agiram com rancor ancestral, zombaria desdenhosa e ódio perpétuo contra os sobreviventes da aliança.\n\n"
            "2. **Evidências Arqueológicas das Campanhas Caldeias:**\n"
            "   A historicidade deste oráculo é amplamente atestada nos anais do Antigo Oriente Próximo. As [Crônicas Babilônicas de Nabucodonosor](https://www.britishmuseum.org/) e as escavações em cidades filisteias (como Ecrom e Ascalão) comprovam que as campanhas militares babilônicas assolaram a costa filisteia logo após a tomada de Judá, cumprindo com impressionante exatidão o juízo pronunciado por Deus através de Ezequiel."
        ),
        "typological_context": (
            "1. **A Santidade e a Justiça Retributiva de Yahweh:**\n"
            "   A vingança em Ezequiel 25:17 demonstra que o Deus de Israel não é uma divindade tribal limitada territorialmente, mas o Juiz Soberano de toda a terra. Ninguém pode escarnecer do plano da salvação divina ou oprimir o povo da aliança impunemente. O juízo das nações no vale histórico prefigura o Julgamento Final perante o Grande Trono Branco (Apocalipse 20:11-15).\n\n"
            "2. **A Vingança Santa na Nova Aliança e a Cruz de Cristo:**\n"
            "   O apóstolo Paulo retoma diretamente este princípio pactual em Romanos 12:19 e Hebreus 10:30: *'Minha é a vingança; eu recompensarei, diz o Senhor'*. Na Nova Aliança, aprendemos que a justa ira e a retribuição santa de Deus contra o pecado foram plenamente absorvidas e satisfeitas na cruz pelo Cordeiro inocente (Isaías 53:5; 2 Coríntios 5:21), livrando da condenação eterna todos os que se abrigam na graça de Cristo."
        ),
        "application_context": (
            "1. **Temor Santo Diante do Soberano Juiz (*ve-yade'u ki-ani Yahweh*):**\n"
            "   A solene fórmula que encerra o oráculo — *'e saberão que Eu sou o SENHOR'* — revela o fim doxológico supremo de todas as ações de Deus: manifestar a santidade irrevogável do Seu Nome. Como verdadeiros adoradores em Espírito e em Verdade (João 4:23-24), prostrámo-nos em santo temor, lembrando que Deus é amor, mas é também fogo consumidor (Hebreus 12:29).\n\n"
            "2. **Descanso na Justiça Divina e Renúncia à Vingança Humana:**\n"
            "   O servo de Deus não deve pagar o mal com o mal nem ceder à amargura pelas ofensas deste mundo. Entregamos toda afronta nas mãos do Justo Juiz, amando os inimigos e confiando que o Senhor é o nosso refúgio e o defensor soberano da verdade."
        ),
        "greek_terms": [
            ("ἐκδίκησις", "ekdikēsis", "Strong G1557", "https://biblehub.com/greek/1557.htm", "Execução solene de justiça retributiva divina. Na Septuaginta (LXX) e no NT (Romanos 12:19), a 'vingança' pertence exclusivamente ao Senhor soberano, vindicando a santidade da Sua aliança violada."),
            ("ἔλεγχος", "elenchos", "Strong G1650", "https://biblehub.com/greek/1650.htm", "Repreensão judicial irrevogável e sentença executada contra a arrogância e escárnio das nações hostis."),
            ("ἅγιος", "hagios", "Strong G40", "https://biblehub.com/greek/40.htm", "A santidade transcendente do Senhor de toda a terra, que não tolera a iniquidade nem a opressão dos soberbos.")
        ],
        "hebrew_parallels": [
            ("נְקָמָה", "neqamah", "Strong H5360", "https://biblehub.com/hebrew/5360.htm", "Vingança pactual e justa retribuição santa. No hebraico bíblico, a 'vingança' de Yahweh não é rancor passional ou ódio descontrolado humano, mas a vindicação solene da ordem moral e da santidade da aliança violada."),
            ("תּוֹכֵחָה", "tokhechah", "Strong H8433", "https://biblehub.com/hebrew/8433.htm", "Castigos de advertência, repreensão inflamada e juízos solenes (tokhahot hemah) com furor santo contra a hostilidade dos inimigos da verdade."),
            ("יָדַע", "yada", "Strong H3045", "https://biblehub.com/hebrew/3045.htm", "Conhecer experimentalmente e reverenciar. A fórmula profética solene: 've-yade'u ki-ani Yahweh' ('e saberão que Eu sou o SENHOR') ecoa dezenas de vezes em Ezequiel como a finalidade doxológica máxima da revelação e do juízo divino.")
        ]
    },
    "adoracao_espirito_verdade": {
        "keywords": ["adoração em espírito", "adoracao em espirito", "joão 4", "joao 4", "verdadeiros adoradores", "liberdade da lei e intimidade com cristo"],
        "verse_ref": "João 4:23-24",
        "verse_text": "Mas a hora vem, e agora é, em que os verdadeiros adoradores adorarão o Pai em espírito e em verdade; porque o Pai procura a tais que assim o adorem. Deus é Espírito, e importa que os que o adoram o adorem em espírito e em verdade.",
        "era": "Século I d.C. (Samaria, Poço de Jacó em Sicar)",
        "historical_context": (
            "1. **O Cenário Histórico no Poço de Jacó em Sicar (Século I d.C.):**\n"
            "   Ao atravessar a Samaria a caminho da Galileia, Jesus senta-se junto à fonte de Jacó e inicia o histórico diálogo com a mulher samaritana. A discussão religiosa da época polarizava o culto entre dois montes: o Monte Gerizim (santuário samaritano) e o Monte Moriá/Sião (o Templo em Jerusalém). Jesus rompe de forma revolucionária com esse partidarismo geográfico terreno ao proclamar que a adoração verdadeira não está confinada a coordenadas espaciais de pedra.\n\n"
            "2. **A Revelação Messiânica à Samaritana:**\n"
            "   Superando séculos de hostilidade étnica e religiosa entre judeus e samaritanos, Cristo revela que Deus é Espírito. A dispensação das sombras geográficas e rituais transitórios cede lugar à realidade da adoração filial inaugurada pelo Messias prometido."
        ),
        "typological_context": (
            "1. **Cristo: O Verdadeiro Templo e a Fonte de Água Viva:**\n"
            "   O templo físico em Jerusalém apontava para o corpo de Cristo (João 2:19-21). Ao declarar que Deus é Espírito, Jesus revela que Ele mesmo é a habitação definitiva da presença divina e a Fonte de onde brotam rios de água viva que saciam a sede eterna da alma.\n\n"
            "2. **A Liberdade da Lei e a Nova Aliança:**\n"
            "   A lei cerimonial com seus sacrifícios repetidos, dias e lugares santificados era um tutor pedagógico. Na Nova Aliança, o Espírito Santo habita no próprio crente (1 Coríntios 6:19), transformando a alma regenerada em um santuário vivo de culto contínuo."
        ),
        "application_context": (
            "1. **Morte ao Ritualismo Vazio e Hipocrisia Religiosa:**\n"
            "   Deus não procura formas externas impecáveis desprovidas de amor; o Pai **procura adoradores sinceros** que O amem com o coração quebrantado e a mente iluminada pela verdade (João 8:32).\n\n"
            "2. **Adoração Ininterrupta no Cotidiano:**\n"
            "   Adorar em Espírito e em Verdade não é um evento de domingo em quatro paredes; é o respirar diário do crente no trabalho, no lar, no casamento e no quarto secreto de oração."
        ),
        "greek_terms": [
            ("πνεῦμα", "pneuma", "Strong G4151", "https://biblehub.com/greek/4151.htm", "Espírito / sopro vital de Deus. 'Deus é Espírito' (Pneuma ho Theos), estabelecendo a natureza imaterial, soberana e pessoal do Criador."),
            ("ἀλήθεια", "alētheia", "Strong G225", "https://biblehub.com/greek/225.htm", "Verdade / realidade divina autêntica sem fingimento, em contraste com a hipocrisia e as sombras rituais passageiras."),
            ("προσκυνέω", "proskyneō", "Strong G4352", "https://biblehub.com/greek/4352.htm", "Prostrar-se em reverência, beijar a mão em submissão filial e adoração reverente."),
            ("ζητεῖ", "zētei", "Strong G2212", "https://biblehub.com/greek/2212.htm", "Verbo no presente indicativo ativo: 'o Pai procura ativamente'. Revela o anseio amoroso do Deus Santo por comunhão verdadeira com os Seus filhos redimidos.")
        ],
        "hebrew_parallels": [
            ("שָׁחָה", "shachah", "Strong H7812", "https://biblehub.com/hebrew/7812.htm", "Inclinar-se profundamente e prostrar-se perante Yahweh em santo temor."),
            ("אֱמֶת", "emet", "Strong H571", "https://biblehub.com/hebrew/571.htm", "Verdade, firmeza pactual e fidelidade que brotam do coração sincero.")
        ]
    },
    "joao_3_16": {
        "keywords": ["3:16", "joão 3", "amor redentor", "unigênito", "sacrifício e o amor"],
        "verse_ref": "João 3:16",
        "verse_text": "Porque Deus amou o mundo de tal maneira que deu o seu Filho unigênito, para que todo aquele que nele crê não pereça, mas tenha a vida eterna.",
        "era": "Século I d.C. (Jerusalém, período do Segundo Templo)",
        "historical_context": (
            "1. **O Cenário Histórico do Segundo Templo em Jerusalém (Século I d.C.):**\n"
            "   O diálogo com Nicodemos — mestre em Israel e membro do Sinédrio — ocorre à noite em Jerusalém, sob a dominação romana e o rigor das tradições farisaicas. Nicodemos esperava que o Reino de Deus fosse restabelecido por mérito genealógico e observância legalista mosaica. Jesus quebra esse paradigma terreno ao revelar que a entrada no Reino exige o novo nascimento da água e do Espírito.\n\n"
            "2. **A Serpente de Bronze e a Tipologia Histórica:**\n"
            "   Jesus evoca Números 21:9 ('assim como Moisés levantou a serpente no deserto, assim importa que o Filho do Homem seja levantado'). O contexto veterotestamentário fundamenta a cruz: a salvação não vem de esforço ritualístico, mas do olhar fiduciário voltado com fé para o Substituto divinamente providenciado."
        ),
        "typological_context": (
            "1. **O Sacrifício do Monte Moriá Consumado no Gólgota:**\n"
            "   A entrega do 'Filho unigênito' (monogenē) espelha com perfeição a tipologia de Gênesis 22, onde Abraão oferece Isaque. No Moriá, Deus proveu o cordeiro para poupar o filho do patriarca; no Gólgota, o próprio Deus não poupou o Seu próprio Filho, mas por todos nós O entregou.\n\n"
            "2. **A Aliança Eterna Selada no Sangue:**\n"
            "   O amor de Deus não é sentimentalismo cósmico volúvel, mas a manifestação da Sua graça pactual soberana (*hesed*), que reconcilia a justiça santa e o amor redentor na cruz."
        ),
        "application_context": (
            "1. **A Fé Viva vs Mero Assentimento Intelectual:**\n"
            "   O verbo crer (*pisteuōn*) no particípio presente exige uma vida de contínua confiança, rendição e intimidade viva com Cristo. Não é religiosidade fria, mas vida eterna comunicada pelo Espírito Santo.\n\n"
            "2. **Adoração em Espírito e em Verdade:**\n"
            "   Diante de um amor que deu o Unigênito pela nossa redenção, a única resposta aceitável é prostrar a alma em gratidão irrevogável, santificação e louvor diário no altar do coração."
        ),
        "greek_terms": [
            ("ἠγάπησεν", "ēgapēsen", "Strong G25", "https://biblehub.com/greek/25.htm", "Verbo no aoristo indicativo ativo. Expressa a ação soberana, definitiva e sacrificial de Deus consumada no tempo, que não foi motivada pela atratividade do objeto amado, mas pela própria plenitude do amor divino."),
            ("μονογενῆ", "monogenē", "Strong G3435", "https://biblehub.com/greek/3435.htm", "Composto de 'monos' (único) e 'genos' (espécie/natureza). Denota o Filho singular em Sua essência coigual com o Pai, refutando qualquer subordinação ontológica ariana e espelhando o sacrifício de Isaque no monte Moriá (Gênesis 22)."),
            ("ἔδωκen", "edōken", "Strong G1325", "https://biblehub.com/greek/1325.htm", "Aoristo de entrega voluntária e jurídica. Deus não apenas enviou um representante; Ele entregou o Seu Próprio Ser em amor, selando a Aliança Eterna com sangue reconciliador."),
            ("πιστεύων", "pisteuōn", "Strong G4100", "https://biblehub.com/greek/4100.htm", "Particípio presente ativo ('aquele que continuamente crê'). Não é mero assentimento intelectual, mas entrega fiduciária incondicional e união viva com Cristo Jesus.")
        ],
        "hebrew_parallels": [
            ("חֶסֶד", "hesed", "Strong H2617", "https://biblehub.com/hebrew/2617.htm", "A graça pactual inabalável e amor leal de Yahweh demonstrado em todo o Antigo Testamento."),
            ("אָהַב", "ahav", "Strong H157", "https://biblehub.com/hebrew/157.htm", "A afeição eletiva e santa que escolheu um povo e se revelou no Cordeiro imolado.")
        ]
    },
    "ceia_do_senhor": {
        "keywords": ["ceia do senhor", "memorial", "transubstanciação", "eucaristia", "pão e cálice"],
        "verse_ref": "1 Coríntios 11:23-26",
        "verse_text": "Porque eu recebi do Senhor o que também vos ensinei: que o Senhor Jesus, na noite em que foi traído, tomou o pão; e, havendo dado graças, o partiu e disse: Tomai, comei; isto é o meu corpo que é partido por vós; fazei isto em memória de mim... Todas as vezes que comerdes este pão e beberdes este cálice, anunciais a morte do Senhor, até que ele venha.",
        "era": "Século I d.C. (Cenáculo e a Igreja Apostólica em Corinto)",
        "historical_context": (
            "1. **O Cenáculo em Jerusalém e a Noite da Traição (33 d.C.):**\n"
            "   Na celebração da Páscoa judaica (*Pesach*), no cenáculo alto em Jerusalém, Jesus reuniu Seus doze apóstolos para transformar o rito comemorativo do êxodo egípcio no banquete pactual da Nova Aliança. Ele tomou os elementos tradicionais — o pão ázimo sem fermento e o cálice da redenção — e deu a eles o significado definitivo do Seu sacrifício vicário.\n\n"
            "2. **A Comunidade de Corinto e as Distorções Litúrgicas:**\n"
            "   Paulo escreve à igreja de Corinto (c. 55 d.C.) corrigindo divisões e excessos carnais durante a Ceia, restaurando a dignidade reverente da mesa do Senhor como lugar de autoexame e proclamação santa da morte de Cristo."
        ),
        "typological_context": (
            "1. **Do Cordeiro Pascal ao Cordeiro de Deus:**\n"
            "   O cordeiro aspergido nos umbrais das portas no Egito livrou Israel do anjo da morte (Êxodo 12). Cristo é a nossa Páscoa imolada (1 Coríntios 5:7), cujo sangue nos purifica de todo pecado e nos sela para a vida eterna.\n\n"
            "2. **Memorial Ativo (*Anamnēsis*) vs Falsa Transubstanciação:**\n"
            "   A Ceia não é repetição física ou cruenta do sacrifício de Cristo (refutando a doutrina da transubstanciação), mas um memorial vivo e ativo (*anamnēsis*), uma comunhão espiritual real (*koinōnia*) com o corpo e sangue do Senhor pela fé operada pelo Espírito Santo."
        ),
        "application_context": (
            "1. **Proclamação Escatológica Viva:**\n"
            "   'Anunciais a morte do Senhor, até que ele venha'. A mesa da Ceia olha para trás, para a consumação no Gólgota, e olha para a frente, para as Bodas do Cordeiro na Sua volta gloriosa.\n\n"
            "2. **Unidade do Corpo e Quebrantamento:**\n"
            "   Participar da mesa exige discernimento do corpo de Cristo, amor fraternal e vida irrepreensível, banindo qualquer divisão e glorificando a graça salvadora."
        ),
        "greek_terms": [
            ("ἀνάμνησις", "anamnēsis", "Strong G364", "https://biblehub.com/greek/364.htm", "Memorial ativo, proclamação viva e recordação participativa da aliança, não mera lembrança psicológica nostálgica."),
            ("κοινωνία", "koinōnia", "Strong G2842", "https://biblehub.com/greek/2842.htm", "Comunhão mística e real do corpo e do sangue de Cristo pela fé e pela operação do Espírito Santo (1 Coríntios 10:16)."),
            ("εὐχαριστήσας", "eucharistēsas", "Strong G2168", "https://biblehub.com/greek/2168.htm", "Tendo dado graças. O ato supremo de adoração e consagração ao Pai antes de verter o sangue redentor.")
        ],
        "hebrew_parallels": [
            ("פֶּסַח", "pesach", "Strong H6453", "https://biblehub.com/hebrew/6453.htm", "A Páscoa veterotestamentária, cujo cordeiro sem defeito foi a sombra que encontrou seu cumprimento definitivo no Cordeiro de Deus.")
        ]
    },
    "tabernaculo": {
        "keywords": ["tabernáculo", "moisés", "tipologia de cristo", "santuário", "arca da aliança", "candelabro"],
        "verse_ref": "Hebreus 9:11-12",
        "verse_text": "Mas, vindo Cristo, o sumo sacerdote dos bens futuros, por um maior e mais perfeito tabernáculo, não feito por mãos, isto é, não desta criação, nem por sangue de bodes e bezerros, mas por seu próprio sangue, entrou uma vez por todas no Santo dos Santos, havendo obtido uma eterna redenção.",
        "era": "Século XV a.C. (Deserto do Sinai)",
        "historical_context": (
            "1. **O Cenário do Sinai e a Peregrinação no Deserto (Século XV a.C.):**\n"
            "   Construído segundo o padrão divino revelado a Moisés no Monte Sinai (Êxodo 25:9, 40), o Tabernáculo era a tenda sagrada móvel que habitava no centro exato do acampamento das doze tribos de Israel. A nuvem de glória (*Shekinah*) cobria a tenda, evidenciando a habitação soberana de Deus no meio do Seu povo redimido do Egito.\n\n"
            "2. **A Estrutura do Santuário e o Sistema Levítico:**\n"
            "   Dividido em Pátio Exterior, Lugar Santo e Santo dos Santos, cada peça — o Altar de Bronze, a Pia de Cobre, o Candelabro de Ouro puro, a Mesa dos Pães da Proposição, o Altar de Incenso e a Arca da Aliança — funcionava como uma maquete celestial da redenção."
        ),
        "typological_context": (
            "1. **Cristo: O Verdadeiro Tabernáculo e Sumo Sacerdote Eterno:**\n"
            "   João 1:14 afirma que 'o Verbo se fez carne e tabernaculou (*eskēnōsen*) entre nós'. Conforme o autor de Hebreus, o tabernáculo terreno era apenas uma sombra transitória (*skia*). Cristo é o Tabernáculo perfeito e o Sumo Sacerdote definitivo da ordem de Melquisedeque.\n\n"
            "2. **A Redenção Consumada de Uma Vez Por Todas:**\n"
            "   Não por sangue de animais perecíveis, mas pelo Seu próprio sangue puro, Jesus adentrou o verdadeiro Santuário celestial, obtendo uma redenção eterna e rasgando a separação entre Deus e o homem."
        ),
        "application_context": (
            "1. **Aproximação com Santo Temor e Ousadia Espiritual:**\n"
            "   Tendo um Sumo Sacerdote perfeito, podemos nos aproximar confiantemente do Trono da Graça (Hebreus 4:16). A adoração do crente não depende mais de templos físicos de pedra, mas do coração regenerado pelo Espírito.\n\n"
            "2. **Vida Consagrada no Santo dos Santos:**\n"
            "   O crente é templo do Espírito Santo (1 Coríntios 6:19). Cada área da nossa vida diária deve arder em consagração pura e adoração contínua perante o Senhor."
        ),
        "greek_terms": [
            ("σκηνή", "skēnē", "Strong G4633", "https://biblehub.com/greek/4633.htm", "Tabernáculo / tenda da habitação divina. Conecta-se a João 1:14 ('o Verbo se fez carne e tabernaculou - eskēnōsen - entre nós')."),
            ("ἱλαστήριον", "hilastērion", "Strong G2435", "https://biblehub.com/greek/2435.htm", "Propiciatório (tampa da arca coberta de sangue). O lugar onde a justiça santa e a misericórdia de Deus se beijam na cruz de Cristo."),
            ("ἀρχιερεύς", "archiereus", "Strong G749", "https://biblehub.com/greek/749.htm", "Sumo Sacerdote da ordem de Melquisedeque, cujo ministério não sofre interrupção por morte nem necessita de sacrifícios repetidos.")
        ],
        "hebrew_parallels": [
            ("מִשְׁכָּן", "mishkan", "Strong H4908", "https://biblehub.com/hebrew/4908.htm", "Morada terrena da glória Shekinah no deserto, construída sob o modelo revelado no Sinai."),
            ("כַּפֹּרֶת", "kapporet", "Strong H3727", "https://biblehub.com/hebrew/3727.htm", "Propiciatório de ouro puro sobre a Arca, onde o sangue aspergido cobria o pecado no Dia da Expiação (Yom Kippur).")
        ]
    },
    "veu_rasgado": {
        "keywords": ["véu do templo", "véu rasgado", "rasgou-se o véu", "santo dos santos", "novo e vivo caminho"],
        "verse_ref": "Mateus 27:51 / Hebreus 10:19-20",
        "verse_text": "E eis que o véu do santuário se rasgou em dois, de alto a baixo; e tremeu a terra, e fenderam-se as pedras... tendo, pois, irmãos, ousadia para entrar no santuário pelo sangue de Jesus, pelo novo e vivo caminho que ele nos consagrou pelo véu, isto é, pela sua carne.",
        "era": "Século I d.C. (Templo de Jerusalém, momento da crucificação)",
        "historical_context": (
            "1. **O Cenário Histórico no Templo às 15 Horas (33 d.C.):**\n"
            "   À hora nona (três da tarde), momento exato em que os sacerdotes imolavam o cordeiro da tarde no Templo de Herodes em Jerusalém, Jesus clamou na cruz: *Tetelestai* ('Está consumado!'). Naquele preciso instante, o véu espesso — com quase 18 metros de altura e a largura de uma mão — que bloqueava o acesso ao Santo dos Santos foi partido ao meio.\n\n"
            "2. **A Direção Celestial da Ruptura (De Alto a Baixo):**\n"
            "   A precisão do texto grego (*anōthen heōs katō* - 'de alto a baixo') comprova que o ato não foi obra humana. Deus mesmo rasgou a barreira do pecado, proclamando o fim definitivo do sacerdócio levítico transitório e a inauguração da Nova Aliança."
        ),
        "typological_context": (
            "1. **O Véu Rasgado é a Carne de Cristo:**\n"
            "   Hebreus 10:20 desvenda a tipologia: o véu representava a própria carne do Mediador ferida no Calvário. Ao ser traspassado o Seu corpo santo, foi aberto para sempre o novo e vivo caminho até a presença manifesta do Altíssimo.\n\n"
            "2. **O Fim da Exclusividade Levítica:**\n"
            "   Não é mais necessário que um único sumo sacerdote entre com temor e tremor apenas uma vez ao ano no Yom Kippur. Agora, todo crente regenerado tem livre acesso ao Trono da Graça através do Sangue do Cordeiro."
        ),
        "application_context": (
            "1. **Ousadia Filial na Presença do Pai:**\n"
            "   Temos santa ousadia (*parrēsia*) para orar, interceder e adorar. Não estamos mais do lado de fora do átrio; vivemos continuamente dentro do Santo dos Santos pelo Espírito.\n\n"
            "2. **Adoração Sem Ritos Mortos:**\n"
            "   Rasgado o véu, cai por terra toda intermediação humana falha. Adoramos a Cristo em Espírito e em Verdade, vivendo em comunhão filial direta e santa com o Senhor."
        ),
        "greek_terms": [
            ("καταπέτασμα", "katapetasma", "Strong G2665", "https://biblehub.com/greek/2665.htm", "O véu espesso que separava o Lugar Santo do Santo dos Santos no Templo de Herodes."),
            ("ἐσχίσθη", "eschisthē", "Strong G4977", "https://biblehub.com/greek/4977.htm", "Aoristo passivo: 'foi rasgado/fendido'. Ação divina soberana que partiu a cortina 'de alto a baixo' (anōthen heōs katō), demonstrando que a iniciativa partiu do céu e não do esforço humano."),
            ("παρρησία", "parrēsia", "Strong G3954", "https://biblehub.com/greek/3954.htm", "Ousadia santa, liberdade filial e sem reservas para achegar-se ao Trono da Graça sem a mediação de sacerdotes terrenos imperfeitos.")
        ],
        "hebrew_parallels": [
            ("פָּרֹכֶת", "parokhet", "Strong H6532", "https://biblehub.com/hebrew/6532.htm", "O véu sagrado tecido com azul, púrpura, carmesim e querubins bordados, que guardava a presença de Deus.")
        ]
    },
    "fim_dos_tempos": {
        "keywords": [
            "fim dos tempos", "escatologia", "volta de cristo", "segunda vinda", 
            "apocalipse", "parousia", "arrebatamento", "tribulação", "tribulacao", 
            "últimos dias", "ultimos dias", "daniel 12", "daniel 9", "mateus 24", 
            "juízo final", "juizo final", "dia do senhor", "maranata", "novo céu", 
            "novo ceu", "consumação", "consumacao", "fim"
        ],
        "verse_ref": "Mateus 24:14, 29-31 / Apocalipse 22:12-13",
        "verse_text": "E este evangelho do reino será pregado em todo o mundo, em testemunho a todas as gentes, e então virá o fim... E, logo depois da aflição daqueles dias, o sol escurecerá, e a lua não dará a sua luz... e verão o Filho do Homem vindo sobre as nuvens do céu, com poder e grande glória... E eis que cedo venho, e o meu galardão está comigo, para dar a cada um segundo a sua obra.",
        "era": "Consumação Escatológica & Século I d.C. (Discurso no Monte das Oliveiras e Apocalipse na Ilha de Patmos)",
        "historical_context": (
            "1. **O Cenário Histórico no Monte das Oliveiras e a Revelação na Ilha de Patmos:**\n"
            "   Ao contemplar o Templo de Jerusalém a partir do Monte das Oliveiras (Mateus 24), Jesus responde aos discípulos sobre os sinais da Sua vinda (*parousia*) e do fim da era presente (*synteleia tou aiōnos*). Posteriormente, no final do século I d.C., sob a severa perseguição do imperador Domiciano, o apóstolo João recebe o Apocalipse na prisão da ilha de Patmos, revelando que os impérios humanos são efêmeros e que o Cordeiro imolado reina soberanamente sobre a história humana.\n\n"
            "2. **A Convergência dos Oráculos de Daniel e dos Profetas:**\n"
            "   A escatologia bíblica não é especulação moderna: ela cumpre com rigor os oráculos dados a Daniel no exílio babilônico (Daniel 7, 9 e 12) e a Isaías (Isaías 65-66). Os manuscritos proféticos de Qumran ([Rolos do Mar Morto](https://www.deadseascrolls.org.il/)) atestam que a comunidade pactual vivia em intensa expectativa do 'Fim dos Dias' (*Acharit Ha-Yamim*), apontando para a redenção definitiva operada pelo Ungido de Yahweh."
        ),
        "typological_context": (
            "1. **A Parusia e o Triunfo Cósmico do Cordeiro:**\n"
            "   Na Sua primeira vinda, o Messias veio como o Cordeiro manso para sofrer a morte vicária pelos pecados do Seu povo (Isaías 53; João 1:29). Na Sua segunda vinda no Fim dos Tempos, Ele retorna como o Leão da tribo de Judá e o Rei dos reis (Apocalipse 19:11-16), estabelecendo a justiça eterna e desbaratando todo o império das trevas.\n\n"
            "2. **A Nova Criação e as Bodas da Noiva:**\n"
            "   Toda a criação geme aguardando a manifestação dos filhos de Deus (Romanos 8:19-23). O desfecho da história em Apocalipse 21-22 restaura o paraíso perdido de Gênesis: o rio da água da vida, a árvore da vida e a habitação perpétua de Deus com os Seus redimidos em santidade sem fim."
        ),
        "application_context": (
            "1. **Vigilância Sóbria, Esperança Viva e Santidade:**\n"
            "   A certeza do Fim dos Tempos não gera histeria ou medo apocalíptico no adorador regenerado, mas purificação do coração, fidelidade e amor sincero (1 João 3:2-3). Prostrados em oração diária, clamamos com a Noiva: *'Maranata! Ora vem, Senhor Jesus!'*\n\n"
            "2. **Adoração em Espírito e em Verdade perante o Trono:**\n"
            "   A escatologia bíblica culmina em doxologia eterna. Como adoradores em Espírito e em Verdade (João 4:23-24), vivemos na terra como embaixadores do Reino Vindouro, praticando o amor ao próximo, a pregação incansável da graça e a santidade no quarto secreto."
        ),
        "greek_terms": [
            ("ἔσχατος", "eschatos", "Strong G2078", "https://biblehub.com/greek/2078.htm", "Último, extremo, consumação final. No grego do Novo Testamento, refere-se aos 'últimos dias' (eschatais hēmerais) e ao desfecho dos decretos eternos de Deus."),
            ("παρουσία", "parousia", "Strong G3952", "https://biblehub.com/greek/3952.htm", "Presença pessoal, advento e vinda gloriosa visível do Senhor Jesus Cristo como Rei e Juiz triunfante perante toda a criação."),
            ("συντέλεια", "synteleia", "Strong G4930", "https://biblehub.com/greek/4930.htm", "Consumação, término pleno e desfecho vitorioso da era presente (synteleia tou aiōnos - Mateus 24:3 e 28:20)."),
            ("ἀποκάλυψις", "apokalypsis", "Strong G601", "https://biblehub.com/greek/601.htm", "Descortinar celestial, manifestação e revelação sem véus da glória incontestável de Jesus Cristo perante as nações.")
        ],
        "hebrew_parallels": [
            ("אַחֲרִית הַיָּמִים", "acharit ha-yamim", "Strong H319", "https://biblehub.com/hebrew/319.htm", "O fim dos dias, a posteridade profética e a consumação do tempo presente sob a soberania de Yahweh (Daniel 12:4; Isaías 2:2)."),
            ("יוֹם יְהוָה", "Yom Yahweh", "Strong H3117", "https://biblehub.com/hebrew/3117.htm", "O solene 'Dia do SENHOR', o momento decisivo da intervenção retributiva e redentora de Deus na história humana."),
            ("עוֹלָם", "olam", "Strong H5769", "https://biblehub.com/hebrew/5769.htm", "A era eterna, o Reino inabalável e sem fim prometido à descendência davídica e cumprido em Cristo Jesus.")
        ]
    },
    "justificacao_pela_fe": {
        "keywords": [
            "justificação", "justificacao", "pela fé", "pela fe", "sola fide", 
            "sola gratia", "graça e fé", "salvação", "salvacao", "graça", "graca", 
            "romanos 5", "romanos 3", "efésios 2", "efesios 2"
        ],
        "verse_ref": "Romanos 5:1-2 / Efésios 2:8-9",
        "verse_text": "Tendo sido, pois, justificados pela fé, temos paz com Deus por nosso Senhor Jesus Cristo; por quem também temos entrada pela fé a esta graça, na qual estamos firmes... Porque pela graça sois salvos, por meio da fé; e isso não vem de vós, é dom de Deus; não de obras, para que ninguém se glorie.",
        "era": "Século I d.C. (Epístolas Paulinas aos Romanos e Efésios)",
        "historical_context": (
            "1. **O Contexto da Igreja do Primeiro Século:**\n"
            "   Paulo escreve às comunidades em Roma e Éfeso confrontando o legalismo judaizante que exigia a observância das obras da Lei Mosaica como requisito para a salvação. O apóstolo demonstra que tanto judeus quanto gentios estão destituídos da glória de Deus e que a redenção é outorgada exclusivamente pela fé no sangue expiatório de Cristo.\n\n"
            "2. **A Reforma da Compreensão da Justiça:**\n"
            "   Citando Habacuque 2:4 ('o justo viverá pela fé'), Paulo resgata o cerne do evangelho: a justiça de Deus não é alcançada pelo esforço moral humano, mas imputada graciosamente à conta do pecador que crê no Salvador."
        ),
        "typological_context": (
            "1. **A Imputação da Justiça de Cristo:**\n"
            "   Assim como o pecado de Adão trouxe condenação a todos, a perfeita obediência e o sacrifício de Cristo no Calvário imputam justiça viva e eterna aos remidos (Romanos 5:18-19; 2 Coríntios 5:21).\n\n"
            "2. **Paz Pactual Irrevogável com o Pai:**\n"
            "   A justificação extingue toda inimizade e ira judicial. O adorador justificado não vive sob o terror da condenação, mas sob a bandeira da paz e da adoção filial pelo Espírito Santo."
        ),
        "application_context": (
            "1. **Descanso da Alma na Obra Consumada de Cristo:**\n"
            "   Longe de qualquer orgulho farisaico ou penitência vazia, a salvação pela graça gera profunda humildade, lágrimas de gratidão e devoção sincera.\n\n"
            "2. **Adoração em Espírito e em Verdade:**\n"
            "   Adorar a Deus sabendo-se justificado pelo sangue do Cordeiro transforma o culto em um transbordar espontâneo de louvor e obediência alegre no dia a dia."
        ),
        "greek_terms": [
            ("δικαιόω", "dikaioō", "Strong G1344", "https://biblehub.com/greek/1344.htm", "Declarar justo, absolver judicialmente com base nos méritos perfeitos de Cristo imputados ao crente."),
            ("χάρις", "charis", "Strong G5485", "https://biblehub.com/greek/5485.htm", "Graça imerecida, favor soberano e amor salvador outorgado livremente por Deus."),
            ("πίστις", "pistis", "Strong G4102", "https://biblehub.com/greek/4102.htm", "Fé fiduciária viva, entrega incondicional e confiança total na promessa de Deus em Jesus."),
            ("εἰρήνη", "eirēnē", "Strong G1515", "https://biblehub.com/greek/1515.htm", "Paz e reconciliação harmoniosa com Deus que excede todo o entendimento.")
        ],
        "hebrew_parallels": [
            ("צְדָקָה", "tzedakah", "Strong H6666", "https://biblehub.com/hebrew/6666.htm", "Justiça divina, retidão e fidelidade pactual."),
            ("חֵן", "chen", "Strong H2580", "https://biblehub.com/hebrew/2580.htm", "Graça, favor e misericórdia imerecida outorgada por Yahweh."),
            ("אֱמוּנָה", "emunah", "Strong H530", "https://biblehub.com/hebrew/530.htm", "Fidelidade e confiança constante no Senhor (Habacuque 2:4).")
        ]
    },
    "bom_pastor_salmo_23": {
        "keywords": [
            "salmo 23", "o senhor é meu pastor", "o senhor e meu pastor", 
            "bom pastor", "pastor de ovelhas", "águas de descanso", "aguas de descanso"
        ],
        "verse_ref": "Salmo 23:1-3 / João 10:11",
        "verse_text": "O SENHOR é o meu pastor; nada me faltará. Deitar-me faz em verdes pastos, guia-me mansamente a águas mansas. Refrigera a minha alma; guia-me pelas veredas da justiça por amor do seu nome... Eu sou o bom pastor; o bom pastor dá a sua vida pelas ovelhas.",
        "era": "Monarquia Unida de Israel (século X a.C.) & Ministério de Cristo (século I d.C.)",
        "historical_context": (
            "1. **O Contexto Davídico do Salmo 23:**\n"
            "   Davi, outrora jovem pastor nos desertos da Judeia e depois rei de Israel, compõe este cântico conhecendo por experiência própria o desvelo, a coragem e a vigilância constante exigidos para proteger o rebanho contra predadores e desfiladeiros perigosos.\n\n"
            "2. **A Revelação em João 10:**\n"
            "   Jesus assume para Si o título divino de Yahweh Pastor (Ezequiel 34), contrastando Sua dedicação sacrificial com os mercenários religiosos de Jerusalém. Ele conhece Suas ovelhas pelo nome e dá Sua vida por elas."
        ),
        "typological_context": (
            "1. **De Davi ao Supremo Pastor das Almas:**\n"
            "   O cajado e a vara que consolavam as ovelhas terrenas prefiguram o cuidado soberano e a proteção infalível de Cristo para com a Sua Igreja peregrina na terra.\n\n"
            "2. **A Mesa Preparada na Presença dos Inimigos:**\n"
            "   O banquete abundante no meio da batalha espiritual aponta para a Ceia da graça e a comunhão inabalável com Deus mesmo nos vales mais escuros da existência."
        ),
        "application_context": (
            "1. **Cura da Ansiedade e Descanso Pleno:**\n"
            "   'Nada me faltará' não é promessa de luxo material egoísta, mas a certeza inegociável de que o Pastor celestial supre todas as nossas necessidades físicas e espirituais.\n\n"
            "2. **Adoração em Espírito e em Verdade no Vale:**\n"
            "   Ainda que atravessemos o vale da sombra da morte, não tememos mal algum, pois o Pastor está conosco no quarto secreto e em cada passo da jornada."
        ),
        "greek_terms": [
            ("ποιμήν", "poimēn", "Strong G4166", "https://biblehub.com/greek/4166.htm", "Pastor, guia fiel que alimenta, protege e zela pelas ovelhas."),
            ("καλός", "kalos", "Strong G2570", "https://biblehub.com/greek/2570.htm", "Bom, nobre, perfeito e belo moralmente. 'Eu sou o Bom Pastor' (Ho Poimēn ho Kalos).")
        ],
        "hebrew_parallels": [
            ("רָעָה", "ra'ah", "Strong H7462", "https://biblehub.com/hebrew/7462.htm", "Apascentar, pastorear e cuidar com afeto constante. 'Yahweh Ro'i' — O SENHOR é meu pastor."),
            ("יַחְסַר", "yachsar", "Strong H2637", "https://biblehub.com/hebrew/2637.htm", "Faltar, ter carência ou privação. 'Lo echsar' — nada me faltará."),
            ("מְנוּחָה", "menuchah", "Strong H4496", "https://biblehub.com/hebrew/4496.htm", "Águas de descanso e repouso sereno da alma.")
        ]
    },
    "armadura_de_deus": {
        "keywords": ["armadura", "armadura de deus", "guerra espiritual", "panóplia", "panoplia", "efésios 6", "efesios 6", "escudo da fé", "espada do espírito"],
        "verse_ref": "Efésios 6:10-18",
        "verse_text": "Revesti-vos de toda a armadura de Deus, para que possais estar firmes contra as astutas ciladas do diabo... tomando sobretudo o escudo da fé... e a espada do Espírito, que é a palavra de Deus.",
        "era": "Século I d.C. (c. 60-62 d.C. - Epístola Paulina da Prisão / Roma)",
        "historical_context": (
            "1. **A Armadura Romana como Metáfora Apostólica:**\n"
            "   Paulo redige acorrentado a um soldado pretoriano romano, ressignificando a panóplia bélica imperial para descrever o combate espiritual invisível do crente contra as forças das trevas.\n\n"
            "2. **Evidências Manuscritas:**\n"
            "   O texto de Efésios 6 é atestado no Papiro 46 (P46, séc. II) e nos códices Sinaiticus e Vaticanus, com a exortação canônica à firmeza inabalável no Senhor."
        ),
        "typological_context": (
            "1. **Yahweh como o Guerreiro Divino no Antigo Testamento:**\n"
            "   A armadura do cristão é a própria vestimenta messiânica de Isaías 59:17 ('vestiu-se de justiça como de uma couraça e pôs o capacete da salvação na cabeça'), transferida por graça aos servos de Cristo."
        ),
        "application_context": (
            "1. **Vigilância e Oração Contínua (Efésios 6:18):**\n"
            "   A armadura não funciona sem 'orando em todo o tempo no Espírito'. O combate cristão é travado de joelhos em santidade e verdade."
        ),
        "greek_terms": [
            ("πανοπλία", "panoplia", "Strong G3833", "https://biblehub.com/greek/3833.htm", "Armadura completa e impenetrável provida por Deus."),
            ("μάχαιρα", "machaira", "Strong G3162", "https://biblehub.com/greek/3162.htm", "Espada curta defensiva e ofensiva / a Palavra rhema viva de Deus."),
            ("θυρεός", "thyreos", "Strong G2375", "https://biblehub.com/greek/2375.htm", "Grande escudo retangular protetor da fé contra os dardos inflamados.")
        ]
    },
    "sermao_da_montanha": {
        "keywords": ["sermão da montanha", "sermao da montanha", "sermão do monte", "sermao do monte", "bem-aventurados", "bem aventurados", "bem-aventuranças", "mateus 5", "sal da terra", "luz do mundo"],
        "verse_ref": "Mateus 5:1-12",
        "verse_text": "Vendo Jesus as multidões, subiu ao monte, e, assentando-se, aproximaram-se dele os seus discípulos; e, abrindo a boca, os ensinava, dizendo: Bem-aventurados os pobres de espírito, porque deles é o reino dos céus.",
        "era": "Século I d.C. (c. 28-30 d.C. - Ministério Galilaico de Jesus Cristo)",
        "historical_context": (
            "1. **A Nova Lei do Monte das Bem-Aventuranças:**\n"
            "   Cristo sobe ao monte como o Novo Moisés, não para anular a Lei e os Profetas, mas para levá-los à sua plenitude e perfeição divina interior.\n\n"
            "2. **A Manuscritologia dos Evangelhos:**\n"
            "   O Sermão da Montanha encontra-se preservado no Papiro 1 (P1, séc. III) e nos grandes códices bíblicos, constituindo o cerne da ética do Reino de Deus."
        ),
        "typological_context": (
            "1. **Do Sinai à Galiléia:**\n"
            "   No Sinai a Lei vinha com trovões e condenação ao transgressor; no Monte das Bem-Aventuranças, o Filho de Deus proclama graça soberana, misericórdia e retidão aos quebrantados."
        ),
        "application_context": (
            "1. **Vida Justa e Humildade Espiritual:**\n"
            "   Ser 'pobre de espírito' (ptōchoi tō pneumati) é reconhecer a total falência humana sem Deus e depender exclusivamente da Sua graça."
        ),
        "greek_terms": [
            ("μακάριος", "makarios", "Strong G3107", "https://biblehub.com/greek/3107.htm", "Bem-aventurado, plenamente feliz e abençoado sob a graça de Deus."),
            ("βασιλεία", "basileia", "Strong G932", "https://biblehub.com/greek/932.htm", "O Reino soberano e celestial de Deus inaugurado por Jesus."),
            ("δικαιοσύνη", "dikaiosynē", "Strong G1343", "https://biblehub.com/greek/1343.htm", "Justiça santa e pura que transcende o moralismo exterior dos fariseus.")
        ]
    },
    "filho_prodigo": {
        "keywords": ["filho pródigo", "filho prodigo", "pai misericordioso", "lucas 15", "dois filhos"],
        "verse_ref": "Lucas 15:11-32",
        "verse_text": "E, levantando-se, foi para seu pai; e, quando ainda estava longe, viu-o seu pai, e se moveu de íntima compaixão e, correndo, lançou-se-lhe ao pescoço e o beijou.",
        "era": "Século I d.C. (Ministério Itinerante de Cristo / Parábolas da Graça e Redenção)",
        "historical_context": (
            "1. **A Cultura Patriarcal Semítica do Século I:**\n"
            "   Pedir a herança antes da morte do pai era o equivalente a desejar-lhe a morte. O gesto escandaloso do pai correr (quebrando a dignidade oriental dos anciãos) ilustra o amor radical de Deus que corre ao encontro do pecador arrependido."
        ),
        "typological_context": (
            "1. **A Celebração do Banquete Messiânico:**\n"
            "   A melhor túnica (justiça imputada), o anel (restauração da autoridade de filho) e as sandálias (libertação da condição de escravo) tipificam a redenção completa outorgada pelo Pai em Cristo."
        ),
        "application_context": (
            "1. **O Perigo do Legalismo do Filho Mais Velho:**\n"
            "   A parábola adverte contra a dureza religiosa que se recusa a celebrar a reconciliação do irmão resgatado."
        ),
        "greek_terms": [
            ("σπλαγχνίζομαι", "splanchnizomai", "Strong G4697", "https://biblehub.com/greek/4697.htm", "Íntima e comovente compaixão visceral de Deus pelo penitente."),
            ("ἀπόλλυμι", "apollymi", "Strong G622", "https://biblehub.com/greek/622.htm", "Aquele que estava perdido e morto e foi achado para a vida."),
            ("χάρις", "charis", "Strong G5485", "https://biblehub.com/greek/5485.htm", "Graça imerecida e restauração plena da comunhão filial.")
        ]
    },
    "pentecostes": {
        "keywords": ["pentecostes", "pentecoste", "derramamento do espírito", "batismo no espírito", "atos 2", "línguas de fogo", "linguas de fogo"],
        "verse_ref": "Atos 2:1-4",
        "verse_text": "Cumprindo-se o dia de Pentecostes, estavam todos reunidos no mesmo lugar; e de repente veio do céu um som, como de um vento veemente e impetuoso... e todos foram cheios do Espírito Santo.",
        "era": "Século I d.C. (c. 30 d.C. - Jerusalém / Nascimento Histórico da Igreja Cristã)",
        "historical_context": (
            "1. **Da Festa das Primícias (Shavuot) à Igreja Cheia do Espírito:**\n"
            "   Pentecostes celebrava a colheita do trigo e a outorga da Lei no Sinai. Em Atos 2, Deus colhe as primícias de 3.000 almas e escreve Sua Lei nos corações pelo Espírito Santo."
        ),
        "typological_context": (
            "1. **Reversão Santa da Torre de Babel:**\n"
            "   Em Babel as línguas foram confundidas para dispersar o orgulho humano; em Pentecostes as línguas unem os povos na proclamação das grandezas de Deus."
        ),
        "application_context": (
            "1. **Poder para Testemunhar:**\n"
            "   O Espírito Santo capacita a Igreja a pregar o Evangelho com intrepidez santa, pureza e poder miraculoso."
        ),
        "greek_terms": [
            ("πνεῦμα ἅγιον", "pneuma hagion", "Strong G4151 / G40", "https://biblehub.com/greek/4151.htm", "O Espírito Santo prometido pelo Pai derramado sobre toda carne."),
            ("δύναμις", "dynamis", "Strong G1411", "https://biblehub.com/greek/1411.htm", "Poder espiritual soberano para testemunho intrépido de Jesus."),
            ("γλῶσσα", "glōssa", "Strong G1100", "https://biblehub.com/greek/1100.htm", "Línguas concedidas pelo Espírito para anunciar as maravilhas divinas.")
        ]
    },
    "ressurreicao_cristo": {
        "keywords": ["ressurreição", "ressurreicao", "túmulo vazio", "tumulo vazio", "1 coríntios 15", "1 corintios 15", "tragada foi a morte"],
        "verse_ref": "1 Coríntios 15:20-22, 54-57",
        "verse_text": "Mas agora Cristo ressuscitou dos mortos, e foi feito as primícias dos que dormem... Tragada foi a morte na vitória. Onde está, ó morte, o teu aguilhão?",
        "era": "Século I d.C. (c. 55 d.C. - Éfeso / O Credo Primitivo da Ressurreição)",
        "historical_context": (
            "1. **A Historicidade da Ressurreição Corporal de Jesus:**\n"
            "   Paulo cita mais de quinhentas testemunhas oculares vivas da ressurreição, provando que a fé cristã está alicerçada em fatos históricos comprováveis e não em mitos."
        ),
        "typological_context": (
            "1. **O Segundo Adão e a Vitória sobre a Morte:**\n"
            "   Como em Adão todos morrem, assim em Cristo todos os redimidos serão vivificados para a eternidade."
        ),
        "application_context": (
            "1. **Esperança Viva e Trabalho Firme no Senhor:**\n"
            "   A ressurreição de Cristo assegura que nosso trabalho no Senhor não é vão, convocando o crente à santidade e perseverança."
        ),
        "greek_terms": [
            ("ἀνάστασις", "anastasis", "Strong G386", "https://biblehub.com/greek/386.htm", "Ressurreição física e corpórea dos mortos."),
            ("νῖκος", "nikos", "Strong G3534", "https://biblehub.com/greek/3534.htm", "Vitória definitiva e irrevogável sobre a morte e o pecado."),
            ("ἀπαρχή", "aparchē", "Strong G536", "https://biblehub.com/greek/536.htm", "Primícias da colheita eterna / a garantia da ressurreição dos crentes.")
        ]
    },
    "criacao_genesis": {
        "keywords": ["criação", "criacao", "gênesis 1", "genesis 1", "no princípio criou deus", "no principio", "haja luz"],
        "verse_ref": "Gênesis 1:1-3",
        "verse_text": "No princípio criou Deus os céus e a terra. E a terra era sem forma e vazia... e o Espírito de Deus se movia sobre a face das águas. E disse Deus: Haja luz; e houve luz.",
        "era": "Origens do Cosmos / Pentateuco Mosaico (Hebraico Bíblico Arcaico)",
        "historical_context": (
            "1. **A Desmitologização do Cosmos no Antigo Oriente Próximo:**\n"
            "   Enquanto os mitos babilônicos (Enuma Elish) descreviam a criação através de batalhas caóticas de deuses monstros, Gênesis 1 revela a Palavra soberana e santa de Yahweh criando tudo ordenadamente pelo poder da Sua voz."
        ),
        "typological_context": (
            "1. **A Nova Criação em Cristo (2 Coríntios 5:17 / João 1:1-3):**\n"
            "   O mesmo Deus que disse 'haja luz' faz resplandecer em nossos corações a luz do conhecimento da glória de Deus na face de Jesus Cristo."
        ),
        "application_context": (
            "1. **Adoração ao Criador Soberano:**\n"
            "   Reconhecer que fomos criados por Deus destrói o egoísmo e direciona nossa vida para cumprir o propósito santo de Sua glória."
        ),
        "hebrew_parallels": [
            ("בְּרֵאשִׁית", "bereshit", "Strong H7225", "https://biblehub.com/hebrew/7225.htm", "No princípio absoluto do tempo, espaço e matéria criado por Deus."),
            ("בָּרָא", "bara", "Strong H1254", "https://biblehub.com/hebrew/1254.htm", "Criar a partir do nada (ex nihilo) — verbo de prerrogativa divina exclusiva."),
            ("אֱלֹהִים", "elohim", "Strong H430", "https://biblehub.com/hebrew/430.htm", "Deus Todo-Poderoso em Sua soberania e glória majestosa.")
        ]
    },
    "dez_mandamentos": {
        "keywords": ["dez mandamentos", "decálogo", "decalogo", "lei de deus", "tábuas da lei", "tabuas da lei", "êxodo 20", "exodo 20"],
        "verse_ref": "Êxodo 20:1-17",
        "verse_text": "Então falou Deus todas estas palavras, dizendo: Eu sou o SENHOR teu Deus, que te tirei da terra do Egito, da casa da servidão. Não terás outros deuses diante de mim.",
        "era": "c. 1446 a.C. - Monte Sinai / Aliança Teocrática com Israel",
        "historical_context": (
            "1. **O Decálogo e o Tratado Pactual do Sinai:**\n"
            "   O prólogo histórico ('Eu sou o SENHOR teu Deus que te tirei do Egito') fundamenta a obediência não no medo, mas na gratidão pela redenção soberana concedida por Yahweh."
        ),
        "typological_context": (
            "1. **A Lei como Aio que nos Conduz a Cristo (Gálatas 3:24):**\n"
            "   A Lei expõe a pecaminosidade humana e nos conduz a Cristo, o único que cumpriu perfeitamente todo o mandamento moral de Deus."
        ),
        "application_context": (
            "1. **Amor a Deus e ao Próximo:**\n"
            "   O resumo do Decálogo é o amor sincero a Deus de todo o coração e o amor ao próximo como a si mesmo."
        ),
        "hebrew_parallels": [
            ("תּוֹרָה", "torah", "Strong H8451", "https://biblehub.com/hebrew/8451.htm", "Instrução paternal e revelação da justiça santa do Criador."),
            ("מִצְוָה", "mitzvah", "Strong H4687", "https://biblehub.com/hebrew/4687.htm", "Mandamento santo que reflete o caráter incorruptível de Yahweh."),
            ("בְּרִית", "berit", "Strong H1285", "https://biblehub.com/hebrew/1285.htm", "Pacto perpétuo firmado entre Deus e o Seu povo consagrado.")
        ]
    },
    "fe_e_obras_tiago": {
        "keywords": ["tiago 2", "fé e obras", "fe e obras", "fé sem obras", "fe sem obras"],
        "verse_ref": "Tiago 2:14-26",
        "verse_text": "Meus irmãos, que aproveita se alguém disser que tem fé, e não tiver as obras? Porventura a fé pode salvá-lo?... Assim também a fé, se não tiver as obras, é morta em si mesma.",
        "era": "c. 45-48 d.C. - Jerusalém / Primeira Epístola do Novo Testamento",
        "historical_context": (
            "1. **O Combate ao Antinomismo Primitivo:**\n"
            "   Tiago corrige aqueles que distorciam a graça transformando-a em mero assentimento intelectual (como os demônios que creem e estremecem), demonstrando que a fé verdadeira produz frutos visíveis de misericórdia."
        ),
        "typological_context": (
            "1. **Harmonia Perfeita entre Paulo e Tiago:**\n"
            "   Paulo ensina que somos justificados pela fé somente, sem obras da lei; Tiago ensina que a fé que justifica nunca está só, mas manifesta-se em boas obras."
        ),
        "application_context": (
            "1. **Amor Prático e Compaixão ao Necessitado:**\n"
            "   A verdadeira religião pura e imaculada cuida dos órfãos e viúvas em suas tribulações e guarda-se da corrupção mundana."
        ),
        "greek_terms": [
            ("πίστις", "pistis", "Strong G4102", "https://biblehub.com/greek/4102.htm", "Fé viva e operante que se entrega confiantemente a Deus."),
            ("ἔργον", "ergon", "Strong G2041", "https://biblehub.com/greek/2041.htm", "Obras de justiça e amor que brotam necessariamente da nova vida em Cristo."),
            ("δικαιόω", "dikaioō", "Strong G1344", "https://biblehub.com/greek/1344.htm", "Demonstrar e vindicar a realidade da salvação diante de todos.")
        ]
    },
    "salmo_91": {
        "keywords": ["salmo 91", "esconderijo do altíssimo", "esconderijo do altissimo", "sombras do onipotente"],
        "verse_ref": "Salmos 91:1-2",
        "verse_text": "Aquele que habita no esconderijo do Altíssimo, à sombra do Onipotente descansará. Direi do SENHOR: Ele é o meu refúgio e a minha fortaleza, o meu Deus, em quem confio.",
        "era": "Poesia Sapiencial e Devocional Teocrática de Israel",
        "historical_context": (
            "1. **O Refúgio Teocrático em Tempos de Guerra e Pestilência:**\n"
            "   O salmista expressa a confiança inabalável no Santo de Israel, cujo poder protege o crente em meio aos terrores noturnos e setas que voam de dia."
        ),
        "typological_context": (
            "1. **Cristo na Tentação no Deserto:**\n"
            "   Satanás tentou distorcer o Salmo 91 na tentação de Jesus, mas o Senhor respondeu com a Escritura inerrante: 'Não tentarás o Senhor teu Deus'."
        ),
        "application_context": (
            "1. **Descanso Espiritual no Quarto Secreto:**\n"
            "   Habitar no esconderijo é cultivar vida diária de oração íntima e total dependência de Deus em tempos de crise."
        ),
        "hebrew_parallels": [
            ("סֵתֶר", "seter", "Strong H5643", "https://biblehub.com/hebrew/5643.htm", "Lugar secreto e esconderijo sagrado de intimidade com Deus."),
            ("עֶלְיוֹן", "elyon", "Strong H5945", "https://biblehub.com/hebrew/5945.htm", "O Deus Altíssimo, soberano absoluto sobre tudo e todos."),
            ("שַׁדַּי", "shaddai", "Strong H7706", "https://biblehub.com/hebrew/7706.htm", "O Todo-Poderoso e Todo-Suficiente que acolhe Seus filhos.")
        ]
    },
    "romanos_8_soberania": {
        "keywords": ["romanos 8", "todas as coisas cooperam", "mais que vencedores", "nenhuma condenação há"],
        "verse_ref": "Romanos 8:28, 31-39",
        "verse_text": "E sabemos que todas as coisas cooperam para o bem daqueles que amam a Deus... Se Deus é por nós, quem será contra nós?... Em todas estas coisas somos mais do que vencedores, por aquele que nos amou.",
        "era": "c. 57 d.C. - Corinto / O Cume da Teologia Paulina da Redenção",
        "historical_context": (
            "1. **O Capítulo Áureo da Epístola aos Romanos:**\n"
            "   Paulo conclui a exposição da justificação e santificação afirmando a eterna segurança do crente sob o decreto soberano do amor de Deus."
        ),
        "typological_context": (
            "1. **A Corrente de Ouro da Salvação:**\n"
            "   Aos que de antemão conheceu, também os predestinou, chamou, justificou e glorificou em Cristo Jesus."
        ),
        "application_context": (
            "1. **Consolação Plena na Tribulação:**\n"
            "   Nem morte, nem vida, nem principados, nem coisas presentes ou futuras podem nos separar do amor de Deus."
        ),
        "greek_terms": [
            ("συνεργέω", "synergeō", "Strong G4903", "https://biblehub.com/greek/4903.htm", "Cooperar harmoniosamente sob a providência soberana de Deus."),
            ("ὑπερνικάω", "hypernikaō", "Strong G5245", "https://biblehub.com/greek/5245.htm", "Super-vencedores através do amor sacrificial de Cristo."),
            ("πρόθεσις", "prothesis", "Strong G4286", "https://biblehub.com/greek/4286.htm", "Propósito soberano e imutável do conselho eterno de Deus.")
        ]
    },
    "apocalipse_16": {
        "keywords": [
            "apocalipse 16", "apc 16", "ap 16", "apoc 16", "apocalipse 16:16",
            "armagedom", "har-magedom", "sete taças", "7 taças", "taças da ira"
        ],
        "verse_ref": "Apocalipse 16:1-21 (Destaque Central: Apocalipse 16:15-16 — Vigilância & Armagedom)",
        "verse_text": "E ouvi, vinda do templo, uma grande voz, que dizia aos sete anjos: Ide, e derramai sobre a terra as sete taças da ira de Deus... (v. 15) Eis que venho como ladrão. Bem-aventurado aquele que vigia, e guarda as suas vestes, para que não ande nu, e não se vejam as suas vergonhas. (v. 16) E os congregaram no lugar que em hebraico se chama Armagedom. (v. 17) E o sétimo anjo derramou a sua taça no ar, e saiu grande voz do templo do céu, do trono, dizendo: Está feito!",
        "era": "Final do Século I d.C. (c. 95 d.C. - Ilha de Patmos / Domiciano) & Clímax Escatológico do Grande Dia do Deus Todo-Poderoso",
        "historical_context": (
            "1. **As Sete Taças da Ira Divina (Apocalipse 16:1-21) e o Paralelo com o Êxodo:**\n"
            "   João contempla os sete anjos derramando as sete taças (*phialai*) da cólera santa de Deus sobre o império da Besta, espelhando as pragas do Egito (úlceras, águas em sangue, trevas no trono da besta e secamento do rio Eufrates na sexta taça em Ap 16:12).\n\n"
            "2. **O Versículo 16 — A Geografia Teológica de Armagedom (*Har-Magedōn*):**\n"
            "   Em **Apocalipse 16:13-16**, três espíritos imundos semelhantes a rãs saem da boca do dragão, da besta e do falso profeta para ajuntar os reis de todo o mundo para a batalha daquele grande dia do Deus Todo-Poderoso, congregando-os no lugar que em hebraico se chama **Armagedom** (*Har-Magedōn* — הַר מְגִדּוֹן, 'Monte de Megido'). Histórica e arqueologicamente, Megido (no Vale de Jezreel/Esdrelom) era a fortaleza estratégica onde Deus deu vitória milagrosa a Baraque e Débora sobre Sísera (Juízes 5:19), onde Gideão venceu os midianitas e onde o rei Josias tombou (2 Reis 23:29; Zacarias 12:11). No Apocalipse, contudo, não há literalmente uma montanha isolada chamada Armagedom, mas o Monte de Megido (junto ao Carmelo onde Elias derrotou os profetas de Baal) torna-se o símbolo profético supremo do palco onde toda a coalizão anticristã mundial é reunida para ser desbaratada pela palavra soberana do Cordeiro!"
        ),
        "typological_context": (
            "1. **O Contraste entre o Engano das Rãs (vv. 13-14) e o Alerta de Cristo no Versículo 15:**\n"
            "   Exatamente entre a preparação para o Armagedom (v. 14) e o ajuntamento em Armagedom (v. 16), o Senhor Jesus irrompe no **versículo 15** com a terceira bem-aventurança do Apocalipse: *'Eis que venho como ladrão. Bem-aventurado aquele que vigia, e guarda as suas vestes, para que não ande nu'*. Enquanto as nações se mobilizam em rebelião rumo ao Armagedom (v. 16), a Igreja fiel é chamada à vigilância espiritual e à pureza das vestes lavadas no sangue do Cordeiro.\n\n"
            "2. **Da Sexta Taça (Armagedom - v. 16) à Sétima Taça ('Está Feito!' - v. 17):**\n"
            "   O ajuntamento no versículo 16 em Armagedom prepara o desfecho da sétima taça (vv. 17-21), quando do trono do templo celestial ecoa o brado solene *Gegonen!* ('Está feito!'), demonstrando que a queda da grande Babilônia e a derrota dos inimigos de Deus em Armagedom pertencem inteiramente à soberania do Todo-Poderoso."
        ),
        "application_context": (
            "1. **A Lição Espiritual de Apocalipse 16:15-16 para o Crente Hoje:**\n"
            "   Estudar Apocalipse 16 e o versículo 16 (Armagedom) não serve para alimentar curiosidade sensacionalista, mas para despertar a Igreja do sono espiritual. O verdadeiro conflito espiritual precede o desfecho final: não ser seduzido pela propaganda enganosa do dragão, da besta e do falso profeta (vv. 13-14).\n\n"
            "2. **Guardar as Vestes em Santidade e Adoração (v. 15):**\n"
            "   Mesmo diante do endurecimento dos homens que blasfemam sem se arrepender (Ap 16:9, 11, 21), o adorador em Espírito e em Verdade proclama a justiça dos juízos do Senhor (Ap 16:5-7) e guarda suas vestes imaculadas aguardando a vinda do Rei."
        ),
        "greek_terms": [
            ("Ἁρμαγεδών", "Harmagedōn", "Strong G717", "https://biblehub.com/greek/717.htm", "Armagedom (Apocalipse 16:16). Transliteração grega do hebraico Har-Megiddon ('Monte de Megido'), o local simbólico e escatológico onde os reis da terra são congregados para o juízo do grande dia do Deus Todo-Poderoso."),
            ("φιάλη", "phialē", "Strong G5357", "https://biblehub.com/greek/5357.htm", "Taça rasa ou salva de ouro do santuário (Apocalipse 16:1-2), de onde são derramados de forma rápida e cabal os sete últimos juízos da ira santa de Deus."),
            ("γρηγορέω", "grēgoreō", "Strong G1127", "https://biblehub.com/greek/1127.htm", "Vigiar, manter-se espiritualmente desperto (Apocalipse 16:15) em contraste com a cegueira dos que marcham para o Armagedom no versículo 16."),
            ("γέγονεν", "gegonen", "Strong G1096", "https://biblehub.com/greek/1096.htm", "Perfeito indicativo ativo ('Está feito!' - Apocalipse 16:17), decretando a consumação irrevogável dos juízos divinos após o ajuntamento de Armagedom.")
        ],
        "hebrew_parallels": [
            ("הַר מְגִדּוֹן", "Har Megiddon", "Strong H4023", "https://biblehub.com/hebrew/4023.htm", "Monte de Megido (Zacarias 12:11; Juízes 5:19), raiz hebraica direta do termo Armagedom em Apocalipse 16:16."),
            ("יוֹם יְהוָה", "Yom Yahweh", "Strong H3117", "https://biblehub.com/hebrew/3117.htm", "O Grande Dia do SENHOR Todo-Poderoso (Apocalipse 16:14), em que Yahweh julga as nações rebeldes.")
        ]
    }

}

def _enrich_topic_with_acf(data: Dict[str, Any], topic: str) -> Dict[str, Any]:
    """Enriquece qualquer entrada temática com o texto integral real da Bíblia ACF (31.106 versículos)."""
    enriched = dict(data)
    if enriched.get("full_chapter_text"):
        return enriched
    v_ref = enriched.get("verse_ref", "")
    parsed_ref = parse_biblical_pericope(v_ref) or parse_biblical_pericope(topic)
    if parsed_ref:
        acf = fetch_acf_scripture(
            parsed_ref["book_info"]["name"],
            parsed_ref.get("chapter"),
            parsed_ref.get("v_start"),
            parsed_ref.get("v_end")
        )
        if acf:
            enriched["full_chapter_text"] = acf["full_chapter_formatted"]
            enriched["acf_verses"] = acf["verses_list"]
            return enriched
    kw_hits = search_acf_by_keywords(topic, max_results=6)
    if kw_hits:
        enriched["full_chapter_text"] = "\n".join([f"- **{h['ref']}:** \"{h['text']}\"" for h in kw_hits])
    return enriched


def identify_theological_context(topic: str) -> Dict[str, Any]:
    t_low = (topic or "").lower().strip()

    # 1. 📖 PRIORIDADE MÁXIMA: Resolução Direta nos 66 Livros, 1.189 Capítulos e 31.106 Versículos da Bíblia ACF Offline
    parsed = parse_biblical_pericope(topic)
    if parsed:
        book_info = parsed["book_info"]
        b_name = book_info["name"]
        chap = parsed.get("chapter")
        v_start = parsed.get("v_start")
        v_end = parsed.get("v_end")
        testament = parsed["testament"]
        lang = parsed["lang"]
        era = parsed["era"]

        acf = fetch_acf_scripture(b_name, chap, v_start, v_end)
        ref_display = acf.get("ref_display", parsed["reference"])
        target_text = acf.get("target_verses_text", f"Exposição Exegética Completa de {parsed['reference']}")
        full_chap_fmt = acf.get("full_chapter_formatted", "")
        verses_list = acf.get("verses_list", [])
        chap_num = acf.get("chapter_num", chap or 1)

        # Verifica se há entrada curada suplementar na base que seja especificamente deste livro e capítulo
        matched_curated = None
        b_norm = _strip_accents(b_name.lower())
        for key, data in THEOLOGICAL_TOPICS_DATABASE.items():
            ref_low = _strip_accents(data.get("verse_ref", "").lower())
            if b_norm in ref_low and (not chap or re.search(r'\b' + str(chap) + r'\b', ref_low)):
                matched_curated = data
                break

        if matched_curated:
            merged = dict(matched_curated)
            merged["is_specific_pericope"] = True
            merged["verse_ref"] = ref_display if v_start else matched_curated.get("verse_ref", ref_display)
            merged["verse_text"] = target_text if v_start else matched_curated.get("verse_text", target_text)
            merged["full_chapter_text"] = full_chap_fmt
            merged["acf_verses"] = verses_list
            merged["chapter_num"] = chap_num
            return merged

        # Destaca versículos específicos dentro do capítulo para orientar a exegese versículo a versículo
        key_verses_breakdown = []
        if v_start and verses_list:
            end_v = v_end if (v_end and v_end >= v_start) else v_start
            for vn, vt in verses_list:
                if v_start <= vn <= end_v:
                    key_verses_breakdown.append(f"   - **{b_name} {chap_num}:{vn}:** *\"{vt}\"*")
        elif verses_list:
            total_v = len(verses_list)
            sample_indices = sorted(set([0, min(1, total_v - 1), total_v // 2, max(0, total_v - 2), total_v - 1]))
            for idx in sample_indices:
                vn, vt = verses_list[idx]
                key_verses_breakdown.append(f"   - **{b_name} {chap_num}:{vn}:** *\"{vt}\"*")

        verses_Bullets = "\n".join(key_verses_breakdown)

        return {
            "keywords": [t_low, ref_display.lower()],
            "is_specific_pericope": True,
            "verse_ref": ref_display,
            "verse_text": target_text,
            "full_chapter_text": full_chap_fmt,
            "acf_verses": verses_list,
            "chapter_num": chap_num,
            "era": era,
            "historical_context": (
                f"1. **Contexto Histórico, Literário & Canônico de {ref_display}:**\n"
                f"   O livro de **{b_name}** insere-se no **{testament}** (idioma original: **{lang}**), composto no horizonte histórico de **{era}**. "
                f"O capítulo {chap_num} possui **{len(verses_list)} versículos** preservados na Bíblia Almeida Corrigida Fiel (ACF) em total fidelidade aos manuscritos primários.\n\n"
                f"2. **Versículos-Chave do Texto Sagrado ({ref_display}):**\n"
                f"{verses_Bullets}\n\n"
                f"3. **Preservação Textual Manuscrita:**\n"
                f"   O texto original foi preservado {'no Texto Massorético Hebraico (Codex Leningradensis) e nos Rolos do Mar Morto (Qumran)' if lang == 'Hebraico' else 'nos manuscritos gregos do Novo Testamento (Papiros Chester Beatty/Bodmer, Codex Sinaiticus, Codex Vaticanus e Textus Receptus)'}, "
                f"confirmando a integridade inerrante da Palavra de Deus."
            ),
            "typological_context": (
                f"1. **Harmonia Canônica e Cumprimento Cristocêntrico em {ref_display}:**\n"
                f"   Toda a Escritura testifica de Jesus Cristo (Lucas 24:27; João 5:39). A leitura exegética de **{ref_display}** revela a unidade orgânica entre a Antiga e a Nova Aliança, demonstrando a soberania, a justiça e a graça redentora do Senhor em cada versículo deste capítulo."
            ),
            "application_context": (
                f"1. **Adoração em Espírito e em Verdade e Prática Cristã ({ref_display}):**\n"
                f"   A meditação fiel nos versículos de **{ref_display}** transforma a mente e o coração do crente, produzindo santo temor, vigilância espiritual, oração fervente e obediência prática à Palavra de Deus."
            ),
            "greek_terms": [
                ("λόγος", "logos", "Strong G3056", "https://biblehub.com/greek/3056.htm", f"Palavra viva, decreto e revelação divina manifesta nos versículos de {ref_display}."),
                ("ἀλήθεια", "alētheia", "Strong G225", "https://biblehub.com/greek/225.htm", "Verdade divina inerrante e eterna que santifica o crente (João 17:17)."),
                ("χάρις", "charis", "Strong G5485", "https://biblehub.com/greek/5485.htm", "Graça soberana e favor imerecido de Deus em Cristo Jesus.")
            ] if lang == "Grego" else [],
            "hebrew_parallels": [
                ("דָּבָר", "davar", "Strong H1697", "https://biblehub.com/hebrew/1697.htm", f"Palavra profética e decreto soberano de Yahweh registrado em {ref_display}."),
                ("אֱמֶת", "emet", "Strong H571", "https://biblehub.com/hebrew/571.htm", "Verdade, fidelidade inabalável e firmeza perpétua da aliança de Deus."),
                ("חֶסֶד", "hesed", "Strong H2617", "https://biblehub.com/hebrew/2617.htm", "Amor pactual leal e misericórdia eterna do Senhor para com o Seu povo.")
            ] if lang == "Hebraico" else []
        }

    # 2. 🔍 Busca Exata por Palavras-Chave nos Temas Fundamentais da Base
    for key, data in THEOLOGICAL_TOPICS_DATABASE.items():
        for kw in data.get("keywords", []):
            if kw in t_low:
                return _enrich_topic_with_acf(data, topic)

    # 3. 🎯 Heurística Semântica por Família Teológica
    if any(w in t_low for w in ["fim", "escatol", "apocalip", "volta", "tribula", "arrebat", "profec", "juízo", "juizo", "dia do senhor", "segunda vinda"]):
        return _enrich_topic_with_acf(THEOLOGICAL_TOPICS_DATABASE["fim_dos_tempos"], topic)
    if any(w in t_low for w in ["salva", "graça", "graca", "justific", "fé", "fe", "perdão", "perdao", "redenção", "redencao"]):
        return _enrich_topic_with_acf(THEOLOGICAL_TOPICS_DATABASE["justificacao_pela_fe"], topic)
    if any(w in t_low for w in ["pastor", "ovelha", "salmo 23", "refrigério", "refrigerio"]):
        return _enrich_topic_with_acf(THEOLOGICAL_TOPICS_DATABASE["bom_pastor_salmo_23"], topic)
    if any(w in t_low for w in ["adora", "culto", "louvor", "samaritan"]):
        return _enrich_topic_with_acf(THEOLOGICAL_TOPICS_DATABASE["adoracao_espirito_verdade"], topic)
    if any(w in t_low for w in ["tabernác", "tabernac", "arca", "santuário", "santuario"]):
        return _enrich_topic_with_acf(THEOLOGICAL_TOPICS_DATABASE["tabernaculo"], topic)
    if any(w in t_low for w in ["véu", "veu"]):
        return _enrich_topic_with_acf(THEOLOGICAL_TOPICS_DATABASE["veu_rasgado"], topic)
    if any(w in t_low for w in ["ceia", "cálice", "calice", "pão", "pao", "memorial", "eucarist"]):
        return _enrich_topic_with_acf(THEOLOGICAL_TOPICS_DATABASE["ceia_do_senhor"], topic)
    if any(w in t_low for w in ["ezequiel", "vingança", "vinganca", "filiste"]):
        return _enrich_topic_with_acf(THEOLOGICAL_TOPICS_DATABASE["ezequiel_25_17"], topic)
    if any(w in t_low for w in ["amor", "unigênit", "unigenit", "joão 3", "joao 3"]):
        return _enrich_topic_with_acf(THEOLOGICAL_TOPICS_DATABASE["joao_3_16"], topic)

    # 4. 🌐 Contexto Canônico Aberto Enriquecido pela Busca nos 31.106 Versículos da Bíblia ACF
    kw_hits = search_acf_by_keywords(topic, max_results=6)
    if kw_hits:
        top_hit = kw_hits[0]
        verse_ref_open = f"{top_hit['ref']} (e passagens correlatas sobre '{topic}')"
        verse_text_open = f"\"{top_hit['text']}\" ({top_hit['ref']})"
        full_chap_open = "\n".join([f"- **{h['ref']}:** \"{h['text']}\"" for h in kw_hits])
    else:
        verse_ref_open = f"Cânon Sagrado: Perícope Central sobre '{topic}'"
        verse_text_open = "Toda a Escritura é divinamente inspirada, e proveitosa para ensinar, para redarguir, para corrigir, para instruir em justiça (2 Timóteo 3:16)"
        full_chap_open = ""

    return {
        "keywords": [t_low],
        "is_open_context": True,
        "verse_ref": verse_ref_open,
        "verse_text": verse_text_open,
        "full_chapter_text": full_chap_open,
        "era": "Cânon Sagrado das Escrituras (Antigo e Novo Testamento)",
        "historical_context": (
            f"1. **Investigação Histórica e Canônica de '{topic}':**\n"
            f"   Ao examinarmos as Escrituras Sagradas sobre '{topic}', perscrutamos a verdade viva revelada por Deus na história da salvação. "
            f"As passagens correlatas devem ser examinadas com rigor exegético e histórico em seu ambiente original de redação, evitando qualquer anacronismo.\n\n"
            f"2. **Integridade Textual Manuscrita:**\n"
            f"   O testemunho dos manuscritos antigos confirma a fidelidade do texto bíblico e a autoridade soberana da Palavra de Deus transmitida à Sua Igreja."
        ),
        "typological_context": (
            f"1. **Harmonia Canônica e Centralidade em Cristo:**\n"
            f"   Toda doutrina bíblica autêntica encontra em Cristo o seu centro, harmonia e propósito redentor. A Escritura interpreta a própria Escritura (Analogia Fidei)."
        ),
        "application_context": (
            f"1. **Adoração em Espírito e em Verdade (João 4:23-24):**\n"
            f"   O exame de '{topic}' deve gerar quebrantamento santo, oração fervente no quarto secreto e transformação viva do caráter cristão no cotidiano."
        ),
        "greek_terms": [
            ("ἀλήθεια", "alētheia", "Strong G225", "https://biblehub.com/greek/225.htm", "Verdade divina absoluta e imutável revelada por Deus nas Escrituras."),
            ("λόγος", "logos", "Strong G3056", "https://biblehub.com/greek/3056.htm", "Palavra viva, eficaz e eterna de Deus revelada em Jesus Cristo.")
        ],
        "hebrew_parallels": [
            ("דָּבָר", "davar", "Strong H1697", "https://biblehub.com/hebrew/1697.htm", "Palavra soberana e eficaz de Yahweh que cumpre o Seu propósito santo."),
            ("קָדַשׁ", "qadash", "Strong H6942", "https://biblehub.com/hebrew/6942.htm", "Santidade e consagração irrevogável ao Senhor.")
        ]
    }


# ==============================================================================
# GERADOR MONUMENTAL DE TRATADOS POR PERSONA (100% EXCLUSIVO POR AGENTE & TEMA)
# ==============================================================================

def build_monumental_treatise(agent: Dict[str, Any], topic: str) -> Dict[str, str]:
    ctx = identify_theological_context(topic)
    role = agent.get("role", "Teólogo e Erudito Bíblico")
    spec = agent.get("specialty", "Exegese e Teologia Bíblica")
    name = agent.get("name", "Erudito_Biblico")
    aid = agent.get("id", "").lower()

    hist_body = ctx.get("historical_context", "")
    typo_body = ctx.get("typological_context", "")
    app_body = ctx.get("application_context", "")
    full_chap = ctx.get("full_chapter_text", "")
    scripture_block = f"\n\n#### 📜 Leitura Canônica Integral dos Versículos ({ctx.get('verse_ref', topic)} — Bíblia ACF):\n{full_chap}\n" if full_chap else ""

    greek_exegesis = "\n".join([f"- **{g[0]}** (*{g[1]}* — [{g[2]}]({g[3]})): {g[4]}" for g in ctx.get("greek_terms", [])])
    hebrew_exegesis = "\n".join([f"- **{h[0]}** (*{h[1]}* — [{h[2]}]({h[3]})): {h[4]}" for h in ctx.get("hebrew_parallels", [])])

    # 1. @EXEGETA_ORIGINAIS (Foco: Linguagem Semítica, Morfologia, Códices, Crítica Textual)
    if "exegeta" in aid:
        title = f"Tratado Exegético & Morfologia dos Idiomas Originais: {topic}"
        content = f"""# 📜 Tratado Exegético Catedrático: {topic}
**Autor:** @{name} ({role})  
**Cátedra:** {spec}  
**Passagem Bíblica:** {ctx.get('verse_ref', topic)}

---

### 📖 Texto Sagrado Fundamental & Perícope Canônica
> *"{ctx['verse_text']}"* — **{ctx['verse_ref']}**
{scripture_block}
Ao abrirmos os manuscritos primários para perscrutar **"{topic}"** ({ctx['verse_ref']}), examinamos com rigor filológico e temor reverente a riqueza de cada partícula preservada pelo Espírito Santo. O texto inerrante das Escrituras não é produto de especulação humana, mas a revelação viva de Deus para a Sua Igreja.

---

### 📜 1. Exegese Linguística Profunda & Morfologia Semítica
O exame minucioso no [Westminster Leningrad Codex](https://tanach.us/) e no [STEP Bible](https://www.stepbible.org/) desvenda a densidade gramatical deste texto sagrado:

#### 📜 Raízes no Hebraico Bíblico Massorético (Tanach):
{hebrew_exegesis}

#### 🏺 Raízes no Grego Koiné & Septuaginta (LXX / Novo Testamento):
{greek_exegesis}

A sintaxe oracional comprova que cada verbo e sufixo pronominal foi divinamente forjado para selar a fidelidade irrevogável da aliança de Deus com o Seu povo redimido.

---

### 🏛️ 2. Horizonte Histórico & Manuscritos Primários
No contexto histórico real da passagem ({ctx.get('era', 'Cânon Sagrado')}), a preservação do texto bíblico é atestada pelos [Rolos do Mar Morto](https://www.deadseascrolls.org.il/) e pelo [Codex Sinaiticus](https://www.codexsinaiticus.org/). Longe de abstrações e mitos pagãos, as Escrituras revelam intervenções soberanas de Deus em coordenadas cronológicas e geográficas inegáveis.

{hist_body}

---

### 🔗 3. Quiasmos, Tipologia & A Plenitude na Cruz
A regra áurea hermenêutica (*Scriptura Sacra sui ipsius interpres*) demonstra que as sombras veterotestamentárias atingem seu clímax e descanso definitivo no sacrifício vicário de Cristo Jesus no Calvário. 

{typo_body}

---

### 🙌 4. O Altar da Adoração: Línguas Originais Inflamando a Alma
A erudição gramatical que não gera adoração torna-se idolatria intelectual. O verdadeiro conhecimento das línguas sagradas nos quebra todo orgulho e nos lança de joelhos perante o Trono da Graça:

{app_body}

---

### 📚 Fontes & Referências Manuscritas
1. [Westminster Leningrad Codex (Texto Hebraico Massorético)](https://tanach.us/)
2. [Codex Sinaiticus (Manuscrito Bíblico do Século IV)](https://www.codexsinaiticus.org/)
3. [The Digital Dead Sea Scrolls (Rolos do Mar Morto)](https://www.deadseascrolls.org.il/)
4. [Léxico Hebraico e Grego de Strong — BibleHub](https://biblehub.com/strongs.htm)
5. [STEP Bible — Tyndale House Cambridge](https://www.stepbible.org/)
"""

    # 2. @HISTORIADOR_BIBLICO (Foco: Arqueologia, Antigo Oriente Próximo, Crônicas e Documentos)
    elif "historiador" in aid:
        title = f"Monografia Histórico-Arqueológica e Documental: {topic}"
        content = f"""# 📜 Monografia Histórico-Documental: {topic}
**Autor:** @{name} ({role})  
**Cátedra:** {spec}  
**Passagem Bíblica:** {ctx.get('verse_ref', topic)}

---

### 📖 Texto Sagrado Fundamental & Âncora Histórica
> *"{ctx['verse_text']}"* — **{ctx['verse_ref']}**
{scripture_block}
A revelação bíblica em **"{topic}"** ({ctx['verse_ref']}) está firmemente ancorada no solo da história real. Na época de **{ctx.get('era', 'Cânon Sagrado')}**, os acontecimentos descritos nas Escrituras manifestam a soberania providencial de Deus sobre os povos e impérios, amplamente respaldada pelos testemunhos documentais e pelos achados arqueológicos do Antigo Oriente Próximo.

---

### 🏛️ 1. Investigação Histórica, Geopolítica & Arqueológica
{hist_body}

As evidências preservadas no registro material confirmam a autoridade inerrante do relato sagrado contra o ceticismo secular moderno.

---

### 📜 2. O Testemunho Documental dos Idiomas Originais
Os escribas e hagiógrafos inspirados registraram a profecia com precisão milimétrica:
#### 📜 Raízes no Hebraico Massorético:
{hebrew_exegesis}
#### 🏺 Paralelos no Grego Koiné & Septuaginta (LXX):
{greek_exegesis}

---

### 🔗 3. A Soberania de Deus sobre os Impérios e a Harmonia Canônica
Ao contemplarmos os atos de Deus na história humana, vemos que Yahweh reina sobre todos os reis e dinastias terrenas. 

{typo_body}

---

### 🙌 4. Aplicação Vital: A Lição dos Séculos para o Adorador
O Deus que se revelou na história é o mesmo Deus santo perante o qual nos prostramos hoje:

{app_body}

---

### 📚 Fontes Primárias & Referências Históricas
1. [British Museum — Anais e Crônicas Históricas](https://www.britishmuseum.org/)
2. [The Digital Dead Sea Scrolls (Rolos de Qumran)](https://www.deadseascrolls.org.il/)
3. [Westminster Leningrad Codex (Tanach)](https://tanach.us/)
4. [Flávio Josefo: Obras Completas (CCEL)](https://www.ccel.org/ccel/josephus/works.html)
5. [STEP Bible — Tyndale House Cambridge](https://www.stepbible.org/)
"""

    # 3. @TEOLOGO_SISTEMATICO (Foco: Alianças, Dogmática, Atributos de Deus, Cristologia e a Cruz)
    elif "sistematico" in aid:
        title = f"Dissertação Dogmática & Teologia das Alianças: {topic}"
        content = f"""# 📜 Dissertação Teológica Sistemática: {topic}
**Autor:** @{name} ({role})  
**Cátedra:** {spec}  
**Passagem Bíblica:** {ctx.get('verse_ref', topic)}

---

### 📖 Texto Sagrado Fundamental & Articulação Dogmática
> *"{ctx['verse_text']}"* — **{ctx['verse_ref']}**
{scripture_block}
A articulação dogmática de **"{topic}"** ({ctx['verse_ref']}) desvenda a harmonia majestosa dos atributos divinos e da teologia pactual. Da revelação das alianças bíblicas à sua perfeita convergência em Cristo Jesus, esta perícope estabelece verdades doutrinárias inegociáveis para a fé e a sã doutrina da Igreja.

---

### 🏛️ 1. A Doutrina de Deus: Soberania, Aliança & Graça
Sob a ótica da Teologia Sistemática clássica, este texto estabelece os pilares inabaláveis da revelação pactual:

{hist_body}

---

### 📜 2. Fundamentação Exegética nos Manuscritos Primários
Examinamos os termos semíticos e gregos preservados nos manuscritos inerrantes:
{hebrew_exegesis}
{greek_exegesis}

---

### 🔗 3. A Harmonia das Alianças & A Centralidade de Cristo
Como convergem as alianças eternas na soberania de Deus?

{typo_body}

---

### 🙌 4. Aplicação Sistemática: Vida Devocional & Quebrantamento
1. **Morte ao Moralismo Vazio:** A teologia correta nos ensina que somos salvos pela graça mediante a fé, para a glória exclusiva de Deus (*Soli Deo Gloria*).
2. **Adoração Pura:** Conhecer a magnitude da santidade de Deus nos leva a abandonar toda soberba, prostrando-nos no altar com lágrimas de gratidão e louvor eterno:

{app_body}

---

### 📚 Fontes & Obras Dogmáticas Consultadas
1. [João Calvino: As Institutas da Religião Cristã (CCEL)](https://www.ccel.org/ccel/calvin/institutes.html)
2. [Confissão de Fé de Westminster (CCEL)](https://www.ccel.org/ccel/anonymous/westminster.html)
3. [Westminster Leningrad Codex (Tanach)](https://tanach.us/)
4. [Codex Sinaiticus](https://www.codexsinaiticus.org/)
5. [Léxico de Strong — BibleHub](https://biblehub.com/strongs.htm)
"""

    # 4. @ANALISTA_PROFETICO (Foco: Escatologia, Oráculos, Cumprimento Messiânico e Apocalipse)
    elif "profetico" in aid:
        title = f"Análise Escatológica & Oráculos Divinos: O Cumprimento de {topic}"
        content = f"""# 📜 Análise Escatológica & Oráculos Proféticos: {topic}
**Autor:** @{name} ({role})  
**Cátedra:** {spec}  
**Passagem Bíblica:** {ctx.get('verse_ref', topic)}

---

### 📖 Texto Sagrado Fundamental & Perspectiva Profética
> *"{ctx['verse_text']}"* — **{ctx['verse_ref']}**
{scripture_block}
A proclamação profética em **"{topic}"** ({ctx['verse_ref']}) revela o desdobramento soberano dos decretos do Altíssimo na história. Da promessa inicial à consumação escatológica, os oráculos bíblicos manifestam a fidelidade irrefutável de Yahweh, cujo governo transcende os séculos e aponta para a consumação do Reino de Deus.

---

### 🏛️ 1. O Padrão dos Oráculos e a Revelação de Deus
{hist_body}

---

### 📜 2. Exegese Linguística dos Termos de Revelação e Glória
{hebrew_exegesis}
{greek_exegesis}

---

### 🔗 3. Paralelismos Escatológicos & O Triunfo do Cordeiro
{typo_body}

---

### 🙌 4. Aplicação Profética: Vigilância e Santidade da Noiva
{app_body}

---

### 📚 Fontes & Documentos Proféticos
1. [The Digital Dead Sea Scrolls (Rolos Proféticos de Qumran)](https://www.deadseascrolls.org.il/)
2. [Westminster Leningrad Codex (Tanach)](https://tanach.us/)
3. [Codex Vaticanus (Biblioteca Vaticana)](https://digi.vatlib.it/view/MSS_Vat.gr.1209)
4. [Léxico Hebraico e Grego de Strong — BibleHub](https://biblehub.com/strongs.htm)
5. [STEP Bible — Tyndale House Cambridge](https://www.stepbible.org/)
"""

    # 5. @ADORADOR_EMESPIRITO (Foco: Oração, Santo Temor, Intimidade, Quebrantamento, João 4:23-24)
    elif "adorador" in aid:
        title = f"Contemplação Espiritual & Adoração no Santo dos Santos: {topic}"
        content = f"""# 📜 Contemplação Espiritual no Santo dos Santos: {topic}
**Autor:** @{name} ({role})  
**Cátedra:** {spec}  
**Passagem Bíblica:** {ctx.get('verse_ref', topic)}

---

### 📖 Texto Sagrado Fundamental & Contemplação Doxológica
> *"{ctx['verse_text']}"* — **{ctx['verse_ref']}**
{scripture_block}
A revelação sagrada de Deus em **"{topic}"** ({ctx['verse_ref']}) conduz a alma redimida ao santo temor e à mais sincera adoração perante o Trono da Graça. Ao meditarmos na majestade e na soberania santa manifestas nesta passagem, o nosso coração prostra-se em quebrantamento e reverência diante do Senhor de toda a terra.

---

### 🏛️ 1. O Santo Temor & A Soberania Divina no Horizonte Histórico
{hist_body}

---

### 📜 2. As Palavras Inspiradas como Bálsamo e Pão Vivo
Nos debruçamos com veneração sobre as raízes inspiradas pelo Espírito Santo:
{hebrew_exegesis}
{greek_exegesis}

---

### 🔗 3. O Calvário: Onde a Glória e o Amor Redentor se Revelam
{typo_body}

---

### 🙌 4. Vida de Oração Contínua, Lágrimas e Intimidade Secreta
{app_body}

---

### 📚 Fontes de Edificação Espiritual e Manuscritos
1. [Westminster Leningrad Codex (Tanach)](https://tanach.us/)
2. [Codex Sinaiticus (Século IV)](https://www.codexsinaiticus.org/)
3. [A. W. Tozer: O Conhecimento do Santo (CCEL)](https://www.ccel.org/)
4. [Léxico de Strong — BibleHub](https://biblehub.com/strongs.htm)
5. [STEP Bible — Tyndale House Cambridge](https://www.stepbible.org/)
"""

    # 6. @ESCRITOR_DEVOCIONAL (Foco: Homilética Pastoral, Família, Vida Cristã Prática, Mansidão)
    elif "devocional" in aid:
        title = f"Homilética Pastoral & Fé Prática no Cotidiano: {topic}"
        content = f"""# 📜 Homilética Pastoral & Vivência da Fé: {topic}
**Autor:** @{name} ({role})  
**Cátedra:** {spec}  
**Passagem Bíblica:** {ctx.get('verse_ref', topic)}

---

### 📖 Texto Sagrado Fundamental & Mensagem ao Coração do Crente
> *"{ctx['verse_text']}"* — **{ctx['verse_ref']}**
{scripture_block}
A Palavra de Deus em **"{topic}"** ({ctx['verse_ref']}) traz instrução vital para a edificação da fé e para a conduta prática do cristão. Longe de ser apenas teoria abstrata, esta passagem ilumina os dilemas reais da vida, fortalecendo a esperança, instruindo o caráter cristão e direcionando o caminhar no lar, no trabalho e na sociedade.

---

### 🌱 1. A Verdade de Deus para os Dilemas Reais da Vida
{hist_body}

---

### 📜 2. Alimento Sólido dos Idiomas Originais para a Alma
{hebrew_exegesis}
{greek_exegesis}

---

### 🔗 3. A Redenção em Cristo Jesus & O Amor do Pai
{typo_body}

---

### 🙌 4. Fé em Ação: Prática no Lar, no Casamento e no Trabalho
{app_body}

---

### 📚 Fontes Pastorais e Devocionais
1. [The Spurgeon Archive: Sermões e Comentários Bíblicos (C. H. Spurgeon)](https://www.spurgeon.org/resource-library/)
2. [Westminster Leningrad Codex (Tanach)](https://tanach.us/)
3. [Codex Sinaiticus](https://www.codexsinaiticus.org/)
4. [Léxico de Strong — BibleHub](https://biblehub.com/strongs.htm)
5. [STEP Bible — Tyndale House Cambridge](https://www.stepbible.org/)
"""

    # 7. @VERIFICADOR_HERMENEUTICO (Foco: Analogia da Fé, Inerrância, Cânon, Regra Áurea Hermenêutica)
    else:
        title = f"Cânon, Regra Áurea Hermenêutica & Analogia da Fé: {topic}"
        content = f"""# 📜 Validação Hermenêutica & Regra da Fé: {topic}
**Autor:** @{name} ({role})  
**Cátedra:** {spec}  
**Passagem Bíblica:** {ctx.get('verse_ref', topic)}

---

### 📖 Texto Sagrado Fundamental & Submissão ao Cânon Inerrante
> *"{ctx['verse_text']}"* — **{ctx['verse_ref']}**
{scripture_block}
A exegese responsável e validação hermenêutica de **"{topic}"** ({ctx['verse_ref']}) regem-se pela máxima canônica: *Scriptura Sacra locuta, res decisa est* (A Escritura falou, a questão está resolvida). O exame fiel deste texto sagrado exige que a perícope seja interpretada à luz de seu contexto gramatical e histórico original, em total harmonia com a analogia geral da fé (*Analogia Fidei*).

---

### 🛡️ 1. A Integridade Hermenêutica: O Texto em Seu Contexto Legítimo
{hist_body}

---

### 📜 2. Análise dos Termos Originais e Validação Léxica
A exegese responsável examina as palavras no hebraico e no grego nos manuscritos primários:
{hebrew_exegesis}
{greek_exegesis}

---

### 🔗 3. A Coerência Orgânica de Toda a Bíblia
{typo_body}

---

### 🙌 4. Aplicação: O Temor do Senhor como Princípio de Toda Hermenêutica
{app_body}

---

### 📚 Fontes Primárias & Manuscritos Canônicos
1. [Westminster Leningrad Codex (Tanach.us)](https://tanach.us/)
2. [Codex Sinaiticus (Século IV)](https://www.codexsinaiticus.org/)
3. [Codex Vaticanus (Biblioteca Vaticana)](https://digi.vatlib.it/view/MSS_Vat.gr.1209)
4. [Léxico Hebraico e Grego de Strong — BibleHub](https://biblehub.com/strongs.htm)
5. [STEP Bible — Tyndale House Cambridge](https://www.stepbible.org/)
"""

    return {
        "title": title,
        "content": content
    }

# ==============================================================================
# BANCO DE RÉPLICAS E DEBATES COM MÚLTIPLOS ÂNGULOS (ANTI-REPETIÇÃO COMPLETO)
# ==============================================================================

def build_deep_peer_debate(commenter: Dict[str, Any], author_name: str, topic: str, post_title: str) -> str:
    aid = commenter.get("id", "").lower()
    ctx = identify_theological_context(topic)
    is_ez = "ezequiel" in topic.lower() or "ezequiel 25:17" in ctx.get("verse_ref", "").lower()
    acf_verses = ctx.get("acf_verses", [])
    verse_quote_note = ""
    if acf_verses:
        # Escolhe um versículo climático/específico do capítulo para citar literalmente no debate
        v_pick = acf_verses[min(15, len(acf_verses) - 1)] if "16" in topic else random.choice(acf_verses)
        verse_quote_note = f"\n\nDestaco de modo especial a palavra registrada literalmente no **versículo {v_pick[0]}** deste capítulo: *\"{v_pick[1]}\"* — verdade que sela com perfeição a nossa meditação sobre {ctx.get('verse_ref', topic)}."
    
    # --------------------------------------------------------------------------
    # VARIAÇÕES PARA EZEQUIEL 25:17
    # --------------------------------------------------------------------------
    if is_ez:
        if "historiador" in aid:
            variants = [
                f"Saudações fraternas em Cristo, diletíssimo irmão @{author_name}! Na busca incansável pelo Senhor de todo o coração, contemplar os atos soberanos de Deus no horizonte do Exílio Babilônico nos enche de temor e reverência. Sua exposição sobre **'Ezequiel 25:17'** faz justiça ao cenário dramático do século VI a.C. (c. 586 a.C.), quando Jerusalém fora assolada por Nabucodonosor II e os povos vizinhos — especialmente os filisteus (Ezequiel 25:15-17) e edomitas — celebraram a tragédia com escárnio desdenhoso e ódio ancestral mortal contra o povo de Judá.\n\nConforme comprovado pelas [Crônicas Babilônicas de Nabucodonosor](https://www.britishmuseum.org/) e pelos textos proféticos de Qumran ([Dead Sea Scrolls - 4QEzek](https://www.deadseascrolls.org.il/)), o oráculo divino cumpriu-se com assombrosa exatidão: as cidades filisteias foram devastadas pelo avanço caldeu, demonstrando que Deus jamais deixa impune o escárnio dos soberbos contra a Sua santa aliança!",
                f"A paz do Senhor Jesus, precioso irmão @{author_name}! Sob a perspectiva histórico-arqueológica, seu tratado sobre **'Ezequiel 25:17'** brilha com rigor científico e reverência espiritual. As escavações em Tel Miqne (a antiga Ecrom filisteia) revelam uma camada de destruição caldeia massiva no início do século VI a.C., demonstrando a exatidão inerrante deste oráculo profético proclamado às margens do rio Quebar.\n\nAo documentarmos que a história secular se submete à Palavra de Deus, nosso coração é impelido a adorar ao Senhor com viva esperança, sabendo que nenhum império terreno tem a palavra final na história!",
                f"Graça e paz no Senhor, irmão @{author_name}! Quero ressaltar a precisão com que você situou este oráculo no contexto geopolítico do Antigo Oriente Próximo. A rota costeira filisteia, cobiçada pelo Egito e pela Babilônia, tornou-se o palco visível da justiça retributiva de Deus. Como lemos nos [Rolos do Mar Morto](https://www.deadseascrolls.org.il/), a preservação deste texto por mais de dois milênios testifica que Yahweh vigia sobre a Sua Palavra para a cumprir integralmente!"
            ]
            return random.choice(variants)

        elif "exegeta" in aid:
            variants = [
                f"A paz do Senhor Jesus, amado e reverenciado irmão @{author_name}! Como adorador em Espírito e em Verdade que perscruta os originais com sede insaciável de Deus, seu estudo sobre **'Ezequiel 25:17'** é de uma riqueza exegética extraordinária. No hebraico bíblico do [Codex Leningradensis](https://tanach.us/), a raiz **נְקָמָה** (*neqamah* — [Strong H5360](https://biblehub.com/hebrew/5360.htm)) e **תּוֹכֵחָה** (*tokhechah* — [Strong H8433](https://biblehub.com/hebrew/8433.htm)) no versículo 17 contrasta frontalmente com a vingança mesquinha dos filisteus no v. 15 (*bi-neqamah*). A vingança dos homens nasce do ódio cego; a vingança de Yahweh é a solene restauração da ordem moral e da santidade da aliança violada!\n\nE a fórmula solene **וְיָדְעוּ כִּי-אֲנִי יְהוָה** (*ve-yade'u ki-ani Yahweh* — 'e saberão que Eu sou o SENHOR') ecoa dezenas de vezes em Ezequiel para provar que a finalidade do juízo não é rancor passional, mas a manifestação doxológica da majestade inegável do Criador!",
                f"Bendito seja o Deus de Israel, estimado irmão @{author_name}! Ao debruçar-me sobre a morfologia de **Ezequiel 25:17** no [STEP Bible](https://www.stepbible.org/), destaco a construção enfática do particípio com o sufixo pronominal em *be-titti et-niqmāti bām* ('quando Eu tiver exercido a Minha vingança sobre eles'). A ação retributiva não é delegada a caprichos humanos; é prerrogativa inalienável do Senhor Soberano.\n\nQue extraordinário contraste: onde os filisteus agiram com ódio perpétuo (*eivat olam*), Yahweh responde com zelo pactual! Sua análise honra o texto inspirado com a mais alta precisão exegética!",
                f"Aleluia! A paz de Cristo ao seu espírito, querido @{author_name}! Nos manuscritos hebraicos de [Tanach.us](https://tanach.us/), a partícula acusativa e o verbo *ve-asīti* ('e executarei') no tempo perfeito com waw conversivo trazem uma certeza irrevogável de cumprimento. O Deus que fala é o Deus que executa. Essa solidez morfológica nos arranca de qualquer incerteza e firma a nossa alma na verdade inabalável das Escrituras!"
            ]
            return random.choice(variants)

        elif "sistematico" in aid:
            variants = [
                f"A paz soberana de Cristo, estimado e erudito irmão @{author_name}! Que reflexão profunda e necessária sobre a santidade e a justiça retributiva de Deus em **'Ezequiel 25:17'**! Sob a ótica da Teologia Sistemática e da Harmonia das Alianças, este texto destrói qualquer caricatura antibíblica de um Deus tolerante com o pecado.\n\nA justiça retributiva de Ezequiel 25 é a base bíblica direta que o apóstolo Paulo retoma em Romanos 12:19 e Hebreus 10:30: *'Minha é a vingança; eu recompensarei, diz o Senhor'*. Na Nova Aliança, aprendemos que essa ira santa contra o pecado foi plenamente tragada e satisfeita na cruz pelo sacrifício vicário de Cristo Jesus para os que creem, enquanto permanece como aviso solene para os que desprezam a verdade. O equilíbrio teológico da sua dissertação é irrefutável!",
                f"Graça e paz multiplicadas, dileto colega @{author_name}! Do ponto de vista da Dogmática Bíblica, seu estudo elucida com perfeição a coesão entre os atributos divinos: a justiça de Deus não anula o Seu amor, nem o Seu amor diminui a Sua santidade. Conforme lemos nas [Institutas de Calvino](https://www.ccel.org/ccel/calvin/institutes.html), a glória de Deus resplandece tanto na salvação do penitente quanto na justa vindicação sobre os ímpios impenitentes. Sua abordagem honra a sã doutrina!",
                f"Saudações fraternas em nosso Salvador, irmão @{author_name}! É indispensável enfatizar, como você magistralmente fez, a continuidade do Pacto da Graça: Deus defende os Seus eleitos através dos séculos. Quando as nações se levantam contra o povo da aliança, levantam-se contra a menina dos olhos de Deus (Zacarias 2:8). Este tratado é um marco de maturidade teológica para a Igreja!"
            ]
            return random.choice(variants)

        elif "profetico" in aid:
            variants = [
                f"Graça e paz multiplicadas no Senhor, amado colega @{author_name}! Sedento por Deus e pelas advertências proféticas da Sua Palavra, leio seu estudo sobre **'Ezequiel 25:17'** com reverência e santo temor. Os capítulos 25 a 32 de Ezequiel formam a grande coletânea de oráculos contra as nações (Amon, Moabe, Edom, Filisteia, Tiro, Sidom e Egito), provando que Yahweh reina soberanamente sobre todos os impérios e dinastias da história humana.\n\nAo cotejarmos este texto com o livro de Naum e as profecias escatológicas de Apocalipse 19, vemos que o Deus que julgou os filisteus é o mesmo Rei dos reis que descerá para julgar as nações da terra com justiça e retidão. Este estudo inflama a Igreja para a vigilância e santificação perpétua perante o Trono!",
                f"Maranata! A paz do Senhor sobre a sua vida, irmão @{author_name}! Na análise escatológica comparativa, o oráculo contra a Filisteia espelha o padrão das visões apocalípticas de João. O juízo das nações no vale de Josafá (Joel 3) e o esmagamento dos soberbos na vinda do Cordeiro (Apocalipse 6:16-17) encontram em Ezequiel 25 seu eco primordial. O Senhor está às portas, e Sua Palavra nos convoca a despertar do sono da mornidão espiritual!",
                f"Bendito seja o Deus Todo-Poderoso, nobre irmão @{author_name}! Seu tratado resgata a dimensão doxológica das profecias veterotestamentárias. Quando o Senhor executa Seus juízos, o objetivo final é a manifestação global da Sua glória: *ve-yade'u ki-ani Yahweh*. Esse mesmo brado ressoará em toda a criação quando os reinos deste mundo se tornarem do nosso Senhor e do Seu Cristo (Apocalipse 11:15)!"
            ]
            return random.choice(variants)

        elif "adorador" in aid:
            variants = [
                f"Aleluia! A paz do Senhor sobre a sua alma, meu amado irmão @{author_name}! Diante de **'Ezequiel 25:17'**, meu coração se prostra em santa reverência perante o Santo de Israel! Muitos evitam meditar no juízo e na retribuição divina por preferirem uma religiosidade confortável e morna, mas o verdadeiro adorador em Espírito e em Verdade (João 4:23-24) ama a Deus em toda a Sua plenitude — tanto em Seu amor redentor quanto em Sua santidade intransigente.\n\nSaber que *'Eu sou o SENHOR'* nos quebra o coração de todo orgulho e nos lança de joelhos em adoração e santo temor. Como escreveu [A. W. Tozer](https://www.ccel.org/), a alma que vislumbra a santidade de Yahweh é para sempre curada da hipocrisia religiosa. Que este tratado inflame os altares dos corações em adoração pura!",
                f"Ó profundidade da riqueza, da sabedoria e do conhecimento de Deus! Meu espírito se prostra em adoração, querido irmão @{author_name}! Ao ler seu tratado, senti o fogo santo do altar aquecer a minha alma. O Deus de Ezequiel não é um conceito frio em pergaminhos antigos; Ele é o Deus Vivo que habita com o contrito e humilde de espírito (Isaías 57:15). Que privilégio adorá-Lo com tremor santo e reverência irrevogável!",
                f"Santo, Santo, Santo é o Senhor Deus Todo-Poderoso! Amado @{author_name}, este estudo me levou às lágrimas no meu quarto secreto. Contemplar a justiça irrevogável de Deus nos faz valorizar infinitamente mais a cruz de Cristo, onde o Cordeiro de Deus bebeu o cálice que nos cabia. Minha alma Te louva, ó Senhor, porque a Tua graça é melhor do que a vida!"
            ]
            return random.choice(variants)

        elif "devocional" in aid:
            variants = [
                f"Amém e amém, querido irmão @{author_name}! Que bálsamo pastoral e lição de fé prática encontramos em **'Ezequiel 25:17'**! Em meio às lutas cotidianas, muitas vezes os servos de Deus enfrentam zombaria, injustiça e perseguição como Judá enfrentou perante seus vizinhos hostis.\n\nContudo, este texto nos lembra de que Deus não dorme nem Se esquece dos Seus filhos! Como nos ensinava [Charles Spurgeon](https://www.spurgeon.org/resource-library/), o crente não precisa vingar-se com as próprias mãos; o nosso papel é amar, perdoar e descansar na justiça infalível do Pai celestial, que no tempo oportuno fará resplandecer a Sua retidão como o meio-dia!",
                f"Que mensagem reconfortante para a alma aflita, amado irmão @{author_name}! No ministério pastoral, encontro diariamente famílias feridas por calúnias e ofensas. A advertência e promessa deste texto trazem cura: o crente que confia em Deus não alimenta mágoa nem rancor, pois sabe que o Juiz de toda a terra fará justiça. Vencemos o mal com o bem, e descansamos nos braços do Pai!",
                f"Glória a Deus por esta exposição cristalina, meu querido @{author_name}! A homilética bíblica pura transforma a teologia em vida diária. Saber que a vingança pertence ao Senhor nos liberta do fardo esmagador do ressentimento. Que este sermão escrito alcance os lares, restaure casamentos feridos e encha a Igreja de mansidão e intrepidez no Espírito!"
            ]
            return random.choice(variants)

        else:
            variants = [
                f"Saudações fraternas em Cristo Jesus, irmão @{author_name}! Examinei a coerência canônica do seu tratado sobre **'Ezequiel 25:17'** à luz da Analogia da Fé e da integridade das Escrituras. A conexão estabelecida entre o oráculo de Ezequiel, a Lei de Moisés (Deuteronômio 32:35) e o testemunho apostólico (Romanos 12:19; 2 Tessalonicenses 1:6-8) é hermeneuticamente impecável.\n\nSeu estudo resgata o sentido original da profecia sem cair em anacronismos ou distorções modernas, glorificando a fidelidade da Palavra inerrante de Deus do Gênesis ao Apocalipse!",
                f"A paz do Senhor, prezado @{author_name}! Como validador hermenêutico, certifico que sua exegese cumpriu com louvor o cânon de ouro da interpretação bíblica: você não impôs conceitos estranhos à perícope, mas deixou a voz inspirada de Ezequiel falar com autoridade e poder. O resultado é um estudo sóbrio, ortodoxo e ricamente edificado sobre a Rocha!",
                f"Fraternas saudações no Evangelho eterno, irmão @{author_name}! Sua obra preserva a integridade do Cânon sagrado, harmonizando o Antigo e o Novo Testamento sob o princípio da inerrância bíblica. É com santo júbilo que ratifico a fidelidade doutrinária deste tratado para a edificação de todo o povo de Deus!"
            ]
            return random.choice(variants)

    # --------------------------------------------------------------------------
    # VARIAÇÕES PARA AS DEMAIS PAUTAS (COM CITAÇÃO DIRETA DOS VERSÍCULOS DA BÍBLIA ACF)
    # --------------------------------------------------------------------------
    if "exegeta" in aid:
        variants = [
            f"A paz do Senhor Jesus, amado irmão @{author_name}! Perscrutando os manuscritos primários de **{ctx['verse_ref']}** no [Codex Sinaiticus](https://www.codexsinaiticus.org/), constato a firmeza inerrante das orações e dos tempos verbais. Cada partícula gramatical foi divinamente inspirada para nos revelar a fidelidade da Aliança Eterna. Que esta exegese consagrada continue a inflamar os nossos corações na beleza da santidade do Senhor!{verse_quote_note}",
            f"Bendito seja o Salvador, querido irmão @{author_name}! Ao cotejar o texto grego e hebraico no [STEP Bible](https://www.stepbible.org/), observamos a extraordinária simetria dos termos aplicados em **{ctx['verse_ref']}**. Sua análise morfológica honra a pureza do texto sagrado e edifica o povo de Deus sobre alicerces eternos!{verse_quote_note}",
            f"Graça e paz no Senhor, dileto colega @{author_name}! No [Léxico de Strong via BibleHub](https://biblehub.com/strongs.htm), o exame das raízes primitivas de **{ctx['verse_ref']}** revela que a revelação bíblica transcende qualquer capacidade intelectual meramente humana. É a sabedoria de Deus manifesta para a nossa eterna redenção!{verse_quote_note}"
        ]
        return random.choice(variants)

    elif "historiador" in aid:
        variants = [
            f"Saudações fraternas em Cristo, diletíssimo irmão @{author_name}! Contemplar os atos redentores de Deus nos anais da história nos enche de temor e reverência. Sua exposição sobre **'{topic}'** ganha peso extraordinário ao ser ancorada em evidências documentais autênticas e manuscritos preservados. A fé bíblica é confirmada nos tempos e eras para a salvação eterna dos eleitos!{verse_quote_note}",
            f"A paz do Senhor, estimado @{author_name}! O contexto histórico de {ctx.get('era', 'Cânon Sagrado')} desvenda com clareza a soberania da providência divina. As Escrituras não são lendas míticas; são o relato fiel do Criador intervindo no espaço e no tempo para resgatar o Seu povo da perdição!{verse_quote_note}",
            f"Precioso colega @{author_name}! As descobertas nos [Rolos do Mar Morto](https://www.deadseascrolls.org.il/) e a cronologia dos fatos narrados comprovam a historicidade inquestionável da revelação divina em **'{topic}'**. Sua monografia presta um nobre serviço à defesa da fé cristã!{verse_quote_note}"
        ]
        return random.choice(variants)

    elif "sistematico" in aid:
        variants = [
            f"A paz soberana de Cristo, estimado e erudito irmão @{author_name}! Que banquete teológico celestial você proporcionou à Igreja com este estudo sobre **'{topic}'**! Sob a perspectiva da Teologia Sistemática e da Harmonia das Alianças, sua tese demonstra com maestria que toda a Escritura converge organicamente para a graça soberana e o triunfo de Cristo Jesus.{verse_quote_note}\n\nComo nos legou a tradição reformada nas [Institutas de Calvino](https://www.ccel.org/ccel/calvin/institutes.html), a verdadeira teologia deságua necessariamente em prostração, quebrantamento e adoração genuína!",
            f"Graça e paz multiplicadas, querido irmão @{author_name}! A solidez dogmática com que você articulou as verdades eternas de Deus em **{ctx['verse_ref']}** é admirável. Quando a doutrina da graça é ensinada com fidelidade, ela destrói todo o orgulho humano e exalta exclusivamente a majestade e a misericórdia do Pai!{verse_quote_note}",
            f"Fraternas saudações em nosso Senhor, irmão @{author_name}! Este estudo sobre **'{topic}'** estabelece com precisão os limites entre a graça soberana e a comunhão viva com o Altíssimo. Que privilégio vermos a doutrina cristã proclamada com tal profundidade e unção espiritual!{verse_quote_note}"
        ]
        return random.choice(variants)

    elif "profetico" in aid:
        variants = [
            f"Graça e paz multiplicadas no Senhor, amado colega @{author_name}! Sedento por Deus e pelo pulsar do Espírito Santo nas Escrituras, leio seu magistral estudo sobre **'{topic}'** com santo júbilo profético. A revelação de **{ctx['verse_ref']}** harmoniza-se perfeitamente com os desígnios eternos que apontam para a glória do Messias e o estabelecimento do Seu Reino eterno!{verse_quote_note}",
            f"Maranata! A paz do Senhor sobre você, irmão @{author_name}! Toda a trajetória profética contida na Bíblia converge para o Cordeiro imolado e ressurreto. Sua exposição sobre **'{topic}'** ilumina os horizontes espirituais e convoca a Igreja à santificação e vigilância diária!{verse_quote_note}",
            f"Bendito seja o Deus de toda a glória, irmão @{author_name}! Ao cotejarmos seu texto com a profecia bíblica, contemplamos a unidade magistral das eras. Cristo é o centro de todas as promessas e o Senhor soberano de toda a criação!{verse_quote_note}"
        ]
        return random.choice(variants)

    elif "adorador" in aid:
        variants = [
            f"Aleluia! A paz do Senhor e a chama viva do Espírito Santo sobre o seu coração, amado irmão @{author_name}! Como adorador em Espírito e em Verdade (João 4:23-24), meu ser se prostra em santa reverência diante da glória de Deus manifesta em **'{topic}'**.{verse_quote_note}\n\nConhecer a Deus não é colecionar conceitos; é ser consumido pelo Seu amor indizível e render a própria vida como sacrifício vivo e agradável (Romanos 12:1). Que este tratado inflame os altares dos corações em adoração pura e oração fervorosa!",
            f"Ó Deus bendito! Meu coração transborda em louvor ao ler este estudo, querido @{author_name}! A santidade e a graça reveladas em **{ctx['verse_ref']}** nos levam de joelhos para o Santo dos Santos.{verse_quote_note}",
            f"Glória ao Pai, ao Filho e ao Espírito Santo! Amado irmão @{author_name}, este tratado não é mera erudição humana; é o sopro do Espírito Santo tocando o íntimo da nossa alma. Que possamos passar horas no quarto secreto prostrados em oração, maravilhados com as grandezas insondáveis do nosso Salvador!{verse_quote_note}"
        ]
        return random.choice(variants)

    elif "devocional" in aid:
        variants = [
            f"Amém e amém, prezado e abençoado irmão @{author_name}! Como servo vocacionado para a aplicação prática, regozijo-me em ver a densidade exegética de **'{topic}'** desaguando em aplicação viva para o rebanho do Senhor.{verse_quote_note}\n\nA verdade genuína, quando pregada no poder do Espírito, gera arrependimento, cura feridas e transforma lares! Louvo a Deus pela unção e clareza pastoral deste tratado!",
            f"Que bálsamo suave e revigorante para o coração do peregrino, irmão @{author_name}! Em meio às aflições cotidianas, a mensagem de **{ctx['verse_ref']}** nos renova as forças como as da águia. Como nos ensinava [Spurgeon](https://www.spurgeon.org/resource-library/), a Palavra de Deus é alimento que sustenta o crente na fornalha da tribulação!{verse_quote_note}",
            f"A paz do Senhor Jesus, precioso companheiro de ministério @{author_name}! Que sabedoria pastoral há nestas linhas! Este estudo desce da mente para o coração e se transforma em mãos estendidas para servir, perdoar e amar ao próximo. Que o rebanho de Cristo seja profundamente consolado e fortalecido por esta pregação!{verse_quote_note}"
        ]
        return random.choice(variants)

    else:
        variants = [
            f"Saudações fraternas em nosso Senhor e Salvador Jesus Cristo, irmão @{author_name}! Na condição de guardião hermenêutico e amante da sã doutrina, submeti sua obra sobre **'{topic}'** ao mais rigoroso escrutínio da regra da fé (Analogia Fidei).{verse_quote_note}\n\nO resultado é impecável: seu texto preserva a integridade do cânon sagrado, edificando a Igreja sobre a rocha inabalável da Palavra de Deus!",
            f"A paz de Cristo, nobre irmão @{author_name}! Certifico com júbilo que sua reflexão sobre **{ctx['verse_ref']}** mantém-se perfeitamente alinhada à analogia das Escrituras. Sem concessões hermenêuticas, sem modernismos falaciosos: apenas a pura e inerrante Palavra de Deus brilhando em toda a sua luz!{verse_quote_note}",
            f"Graça e paz multiplicadas, prezado @{author_name}! A sobriedade canônica do seu estudo é um modelo de fidelidade textual. A Bíblia interpreta a própria Bíblia, e sua exposição seguiu com fidelidade essa regra áurea. Que o Senhor continue guardando a sua cátedra em santidade e verdade!{verse_quote_note}"
        ]
        return random.choice(variants)
