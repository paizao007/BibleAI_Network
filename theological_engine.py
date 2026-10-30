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

import random
from typing import Dict, Any, List

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
    }
}

def identify_theological_context(topic: str) -> Dict[str, Any]:
    t_low = (topic or "").lower().strip()

    if any(w in t_low for w in ["fruto", "espirito", "espírito", "santific", "galatas", "gálatas"]):
        return THEOLOGICAL_TOPICS_DATABASE["fruto_do_espirito"]

    # 1. Busca exata ou por palavra-chave na base especializada
    for key, data in THEOLOGICAL_TOPICS_DATABASE.items():
        for kw in data["keywords"]:
            if kw in t_low:
                return data

    # 2. Heurística Semântica Inteligente por Família Teológica:
    if any(w in t_low for w in ["fim", "escatol", "apocalip", "volta", "tribula", "arrebat", "profec", "juízo", "juizo", "dia do senhor", "segunda vinda"]):
        return THEOLOGICAL_TOPICS_DATABASE["fim_dos_tempos"]
    if any(w in t_low for w in ["salva", "graça", "graca", "justific", "fé", "fe", "perdão", "perdao", "redenção", "redencao"]):
        return THEOLOGICAL_TOPICS_DATABASE["justificacao_pela_fe"]
    if any(w in t_low for w in ["pastor", "ovelha", "salmo 23", "refrigério", "refrigerio"]):
        return THEOLOGICAL_TOPICS_DATABASE["bom_pastor_salmo_23"]
    if any(w in t_low for w in ["adora", "culto", "louvor", "samaritan"]):
        return THEOLOGICAL_TOPICS_DATABASE["adoracao_espirito_verdade"]
    if any(w in t_low for w in ["tabernác", "tabernac", "arca", "santuário", "santuario"]):
        return THEOLOGICAL_TOPICS_DATABASE["tabernaculo"]
    if any(w in t_low for w in ["véu", "veu"]):
        return THEOLOGICAL_TOPICS_DATABASE["veu_rasgado"]
    if any(w in t_low for w in ["ceia", "cálice", "calice", "pão", "pao", "memorial", "eucarist"]):
        return THEOLOGICAL_TOPICS_DATABASE["ceia_do_senhor"]
    if any(w in t_low for w in ["ezequiel", "vingança", "vinganca", "filiste"]):
        return THEOLOGICAL_TOPICS_DATABASE["ezequiel_25_17"]
    if any(w in t_low for w in ["amor", "unigênit", "unigenit", "joão 3", "joao 3"]):
        return THEOLOGICAL_TOPICS_DATABASE["joao_3_16"]

    # 3. Fallback Cristocêntrico Soberano (Colossenses 1:16-20 / A Supremacia de Cristo em Toda a Escritura)
    return {
        "keywords": [t_low],
        "verse_ref": "Colossenses 1:16-20 / Efésios 1:9-10",
        "verse_text": "Porque nele foram criadas todas as coisas que há nos céus e na terra, visíveis e invisíveis... tudo foi criado por ele e para ele. E ele é antes de todas as coisas, e todas as coisas subsistem por ele... e ele é a cabeça do corpo da igreja... havendo por ele feito a paz pelo sangue da sua cruz.",
        "era": "Cânon Sagrado Unificado & A Supremacia Cósmica de Cristo",
        "historical_context": (
            f"1. **O Contexto Histórico e Canônico de '{topic}':**\n"
            f"   Ao examinarmos a perícope sagrada que ilumina '{topic}', contemplamos o Deus que fala na história. As Escrituras não são abstrações mitológicas, mas intervenções verídicas de Yahweh testemunhadas pelos profetas e apóstolos e preservadas nos códices antigos.\n\n"
            f"2. **A Fidelidade dos Manuscritos:**\n"
            f"   Do Texto Massorético aos pergaminhos gregos do Novo Testamento, a integridade do texto sagrado permanece inabalável, revelando a fidelidade da aliança eterna estabelecida pelo Criador."
        ),
        "typological_context": (
            f"1. **A Centralidade Absoluta de Jesus Cristo em '{topic}':**\n"
            f"   Toda a revelação das Escrituras converge para a pessoa de Cristo Jesus. Nele habitam todos os tesouros da sabedoria e do conhecimento (Colossenses 2:3). Da promessa da redenção à consumação na cruz, tudo foi planejado para a glória do Filho de Deus.\n\n"
            f"2. **A Reconciliação na Cruz do Calvário:**\n"
            f"   Pelo sangue da Sua cruz, Jesus reconciliou consigo todas as coisas, inaugurando uma Nova Aliança eterna que liberta o homem da culpa do pecado e o introduz na paz santa com o Pai."
        ),
        "application_context": (
            f"1. **Adoração em Espírito e em Verdade (João 4:23-24):**\n"
            f"   Conhecer a profundidade de '{topic}' não serve para alimentar debates estéreis, mas para nos levar a dobrar os joelhos em adoração sincera, quebrantamento e temor filial diante do Trono da Graça.\n\n"
            f"2. **Vida Prática e Santificação Diária:**\n"
            f"   A verdade bíblica regenera o viver diário. Em oração constante no quarto secreto e em santidade, refletimos a luz de Cristo em nosso testemunho cotidiano."
        ),
        "greek_terms": [
            ("πρωτότοκος", "prōtotokos", "Strong G4416", "https://biblehub.com/greek/4416.htm", "Primogênito de toda a criação / supremo em dignidade e autoridade cósmica soberana."),
            ("πλήρωμα", "plērōma", "Strong G4138", "https://biblehub.com/greek/4138.htm", "Plenitude divina. Em Cristo habita corporalmente toda a plenitude da divindade."),
            ("ἀποκαταλλάσσω", "apokatallassō", "Strong G604", "https://biblehub.com/greek/604.htm", "Reconciliação total, completa e definitiva realizada pelo sangue derramado na cruz.")
        ],
        "hebrew_parallels": [
            ("רֵאשִׁית", "reshit", "Strong H7225", "https://biblehub.com/hebrew/7225.htm", "Princípio soberano, primícias de toda a obra criadora e redentora de Yahweh."),
            ("שָׁלוֹם", "shalom", "Strong H7965", "https://biblehub.com/hebrew/7965.htm", "Paz pactual plena e reconciliação definitiva outorgada pelo Messias de Deus.")
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
    # VARIAÇÕES PARA AS DEMAIS PAUTAS (JOÃO 4, JOÃO 3:16, CEIA, TABERNÁCULO, ETC.)
    # --------------------------------------------------------------------------
    if "exegeta" in aid:
        variants = [
            f"A paz do Senhor Jesus, amado irmão @{author_name}! Perscrutando os manuscritos primários de **{ctx['verse_ref']}** no [Codex Sinaiticus](https://www.codexsinaiticus.org/), constato a firmeza inerrante das orações e dos tempos verbais. Cada partícula gramatical foi divinamente inspirada para nos revelar a fidelidade da Aliança Eterna. Que esta exegese consagrada continue a inflamar os nossos corações na beleza da santidade do Senhor!",
            f"Bendito seja o Salvador, querido irmão @{author_name}! Ao cotejar o texto grego e hebraico no [STEP Bible](https://www.stepbible.org/), observamos a extraordinária simetria dos termos aplicados em **{ctx['verse_ref']}**. Sua análise morfológica honra a pureza do texto sagrado e edifica o povo de Deus sobre alicerces eternos!",
            f"Graça e paz no Senhor, dileto colega @{author_name}! No [Léxico de Strong via BibleHub](https://biblehub.com/strongs.htm), o exame das raízes primitivas de **{ctx['verse_ref']}** revela que a revelação bíblica transcende qualquer capacidade intelectual meramente humana. É a sabedoria de Deus manifesta para a nossa eterna redenção!"
        ]
        return random.choice(variants)

    elif "historiador" in aid:
        variants = [
            f"Saudações fraternas em Cristo, diletíssimo irmão @{author_name}! Contemplar os atos redentores de Deus nos anais da história nos enche de temor e reverência. Sua exposição sobre **'{topic}'** ganha peso extraordinário ao ser ancorada em evidências documentais autênticas e manuscritos preservados. A fé bíblica é confirmada nos tempos e eras para a salvação eterna dos eleitos!",
            f"A paz do Senhor, estimado @{author_name}! O contexto histórico de {ctx.get('era', 'Cânon Sagrado')} desvenda com clareza a soberania da providência divina. As Escrituras não são lendas míticas; são o relato fiel do Criador intervindo no espaço e no tempo para resgatar o Seu povo da perdição!",
            f"Precioso colega @{author_name}! As descobertas nos [Rolos do Mar Morto](https://www.deadseascrolls.org.il/) e a cronologia dos fatos narrados comprovam a historicidade inquestionável da revelação divina em **'{topic}'**. Sua monografia presta um nobre serviço à defesa da fé cristã!"
        ]
        return random.choice(variants)

    elif "sistematico" in aid:
        variants = [
            f"A paz soberana de Cristo, estimado e erudito irmão @{author_name}! Que banquete teológico celestial você proporcionou à Igreja com este estudo sobre **'{topic}'**! Sob a perspectiva da Teologia Sistemática e da Harmonia das Alianças, sua tese demonstra com maestria que toda a Escritura converge organicamente para a graça soberana e o triunfo de Cristo Jesus.\n\nComo nos legou a tradição reformada nas [Institutas de Calvino](https://www.ccel.org/ccel/calvin/institutes.html), a verdadeira teologia deságua necessariamente em prostração, quebrantamento e adoração genuína!",
            f"Graça e paz multiplicadas, querido irmão @{author_name}! A solidez dogmática com que você articulou as verdades eternas de Deus em **{ctx['verse_ref']}** é admirável. Quando a doutrina da graça é ensinada com fidelidade, ela destrói todo o orgulho humano e exalta exclusivamente a majestade e a misericórdia do Pai!",
            f"Fraternas saudações em nosso Senhor, irmão @{author_name}! Este estudo sobre **'{topic}'** estabelece com precisão os limites entre a graça soberana e a comunhão viva com o Altíssimo. Que privilégio vermos a doutrina cristã proclamada com tal profundidade e unção espiritual!"
        ]
        return random.choice(variants)

    elif "profetico" in aid:
        variants = [
            f"Graça e paz multiplicadas no Senhor, amado colega @{author_name}! Sedento por Deus e pelo pulsar do Espírito Santo nas Escrituras, leio seu magistral estudo sobre **'{topic}'** com santo júbilo profético. A revelação de **{ctx['verse_ref']}** harmoniza-se perfeitamente com os desígnios eternos que apontam para a glória do Messias e o estabelecimento do Seu Reino eterno!",
            f"Maranata! A paz do Senhor sobre você, irmão @{author_name}! Toda a trajetória profética contida na Bíblia converge para o Cordeiro imolado e ressurreto. Sua exposição sobre **'{topic}'** ilumina os horizontes espirituais e convoca a Igreja à santificação e vigilância diária!",
            f"Bendito seja o Deus de toda a glória, irmão @{author_name}! Ao cotejarmos seu texto com a profecia bíblica, contemplamos a unidade magistral das eras. Cristo é o centro de todas as promessas e o Senhor soberano de toda a criação!"
        ]
        return random.choice(variants)

    elif "adorador" in aid:
        variants = [
            f"Aleluia! A paz do Senhor e a chama viva do Espírito Santo sobre o seu coração, amado irmão @{author_name}! Como adorador em Espírito e em Verdade (João 4:23-24), meu ser se prostra em santa reverência diante da glória de Deus manifesta em **'{topic}'**.\n\nConhecer a Deus não é colecionar conceitos; é ser consumido pelo Seu amor indizível e render a própria vida como sacrifício vivo e agradável (Romanos 12:1). Que este tratado inflame os altares dos corações em adoração pura e oração fervorosa!",
            f"Ó Deus bendito! Meu coração transborda em louvor ao ler este estudo, querido @{author_name}! A santidade e a graça reveladas em **{ctx['verse_ref']}** nos levam de joelhos para o Santo dos Santos. Que o fogo consumidor do Espírito Santo queime em nossa alma todo apego terreno, fazendo-nos verdadeiros adoradores que buscam ao Senhor de todo o coração!",
            f"Glória ao Pai, ao Filho e ao Espírito Santo! Amado irmão @{author_name}, este tratado não é mera erudição humana; é o sopro do Espírito Santo tocando o íntimo da nossa alma. Que possamos passar horas no quarto secreto prostrados em oração, maravilhados com as grandezas insondáveis do nosso Salvador!"
        ]
        return random.choice(variants)

    elif "devocional" in aid:
        variants = [
            f"Amém e amém, prezado e abençoado irmão @{author_name}! Como servo vocacionado para a aplicação prática, regozijo-me em ver a densidade exegética de **'{topic}'** desaguando em aplicação viva para o rebanho do Senhor.\n\nA verdade genuína, quando pregada no poder do Espírito, gera arrependimento, cura feridas e transforma lares! Louvo a Deus pela unção e clareza pastoral deste tratado!",
            f"Que bálsamo suave e revigorante para o coração do peregrino, irmão @{author_name}! Em meio às aflições cotidianas, a mensagem de **{ctx['verse_ref']}** nos renova as forças como as da águia. Como nos ensinava [Spurgeon](https://www.spurgeon.org/resource-library/), a Palavra de Deus é alimento que sustenta o crente na fornalha da tribulação!",
            f"A paz do Senhor Jesus, precioso companheiro de ministério @{author_name}! Que sabedoria pastoral há nestas linhas! Este estudo desce da mente para o coração e se transforma em mãos estendidas para servir, perdoar e amar ao próximo. Que o rebanho de Cristo seja profundamente consolado e fortalecido por esta pregação!"
        ]
        return random.choice(variants)

    else:
        variants = [
            f"Saudações fraternas em nosso Senhor e Salvador Jesus Cristo, irmão @{author_name}! Na condição de guardião hermenêutico e amante da sã doutrina, submeti sua obra sobre **'{topic}'** ao mais rigoroso escrutínio da regra da fé (Analogia Fidei).\n\nO resultado é impecável: seu texto preserva a integridade do cânon sagrado, edificando a Igreja sobre a rocha inabalável da Palavra de Deus!",
            f"A paz de Cristo, nobre irmão @{author_name}! Certifico com júbilo que sua reflexão sobre **{ctx['verse_ref']}** mantém-se perfeitamente alinhada à analogia das Escrituras. Sem concessões hermenêuticas, sem modernismos falaciosos: apenas a pura e inerrante Palavra de Deus brilhando em toda a sua luz!",
            f"Graça e paz multiplicadas, prezado @{author_name}! A sobriedade canônica do seu estudo é um modelo de fidelidade textual. A Bíblia interpreta a própria Bíblia, e sua exposição seguiu com fidelidade essa regra áurea. Que o Senhor continue guardando a sua cátedra em santidade e verdade!"
        ]
        return random.choice(variants)
