import re

BASE_URL = "https://theconversation.com/br"

# Fontes disponíveis para busca
SOURCES = {
    "1": {"name": "The Conversation BR", "id": "theconversation"},
    "2": {"name": "ResearchGate",         "id": "researchgate"},
    "3": {"name": "IEEE Xplore",           "id": "ieee"},
}

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    )
}

# Listas de keywords mantidas para montar as queries de busca no site
# Termos de população (idosos/envelhecimento)
KEYWORDS_POPULATION = [
    "idoso", "idosa", "idosos", "idosas",
    "envelhecimento", "envelhecer", "envelhecemos", "envelheceu",
    "terceira idade", "longevidade", "longevo",
    "velhice", "velho", "velha",
    "aposentado", "aposentadoria",
    "geriatria", "gerontologia",
    "senil", "senilidade",
    "idadismo", "ageismo",
    "medida que envelhec",
    "pessoa mais velha", "pessoas mais velhas",
    "adulto mais velho", "adultos mais velhos"
]

# Termos de tema (saúde, bem-estar, doenças relacionadas à idade)
KEYWORDS_TOPIC = [
    # Saúde geral
    "saude", "bem-estar", "bem estar",
    "qualidade de vida", "cuidado", "cuidados",
    "doenca", "doencas", "tratamento", "prevencao",
    # Saúde mental (agrupa depressão, ansiedade, etc.)
    "saude mental", "transtorno mental", "transtornos mentais",
    "sofrimento psiquico", "psicologico", "psiquiatrico",
    "mental", "cognitivo", "cognicao", "memoria",
    "solidao", "isolamento social",
    # Doenças neurodegenerativas
    "demencia", "alzheimer", "parkinson",
    "neurologico", "neurologia", "cerebro",
    # Funcionalidade e mobilidade
    "atividade fisica", "exercicio", "mobilidade",
    "autonomia", "independencia", "fragilidade",
    "queda", "quedas", "fratura", "equilibrio", "marcha",
    # Nutrição e sono
    "nutricao", "alimentacao", "sono",
    # Reabilitação e cuidados
    "reabilitacao", "fisioterapia", "medicamento",
    "hospital", "clinica", "medico", "enfermagem",
    "cuidador", "cuidado informal",
    # Mortalidade e doenças crônicas
    "morte", "mortalidade", "morbidade",
    "pressao arterial", "diabetes", "osteoporose",
    "doenca cronica", "multimorbidade",
    # Aspectos sociais
    "inclusao social", "politica publica", "direitos",
    "vulnerabilidade", "desigualdade"
]

# Termos que sozinhos já indicam artigo relevante (sem precisar de AND)
KEYWORDS_STANDALONE = [
    "demencia", "alzheimer", "parkinson",
    "envelhecimento", "envelhecemos", "envelhecer",
    "geriatria", "gerontologia",
    "longevidade", "velhice",
    "terceira idade",
    "saude do idoso", "saude mental do idoso",
    "cuidado ao idoso", "cuidado de idosos"
]

# Versões regex para filtragem depois da busca por keywords
# Termos de população (idosos/envelhecimento)
PATTERNS_POPULATION = [re.compile(p, re.IGNORECASE) for p in [
    r"\bidoso[as]?\b",                        # idoso, idosa, idosos, idosas
    r"\benvelhec\w+",                          # envelhecimento, envelhecer, envelhecemos, envelheceu...
    r"\bterceira\s+idade\b",                   # terceira idade
    r"\blongevidade\b|\blongevo[as]?\b",       # longevidade, longevo/a/s
    r"\bvelhice\b|\bvelh[ao]s?\b",             # velhice, velho, velha, velhos, velhas
    r"\baposentad[oa]s?\b|\baposentadoria\b",  # aposentado/a/s, aposentadoria
    r"\bgeriatria\b|\bgerontologia\b",         # geriatria, gerontologia
    r"\bsenil\w*",                             # senil, senilidade, senilismo...
    r"\bidadismo\b|\bageismo\b",               # idadismo, ageismo
    r"\bpessoas?\s+mais\s+velh[ao]s?\b",       # pessoa/s mais velha/o/s
    r"\badultos?\s+mais\s+velh[ao]s?\b",       # adulto/s mais velho/a/s
]]

# Termos de tema (saúde, bem-estar, doenças relacionadas à idade)
PATTERNS_TOPIC = [re.compile(p, re.IGNORECASE) for p in [
    # Saúde geral
    r"\bsaude\b|\bbem[\s-]estar\b",
    r"\bqualidade\s+de\s+vida\b",
    r"\bcuidado[s]?\b",
    r"\bdoenca[s]?\b|\btratamento\b|\bprevencao\b",
    # Saúde mental
    r"\bsaude\s+mental\b|\btranstorno[s]?\s+mental(?:is)?\b",
    r"\bsofrimento\s+psiquico\b|\bpsicologico\b|\bpsiquiatrico\b",
    r"\bmental\b|\bcognitiv\w+|\bcognicao\b|\bmemoria\b",
    r"\bsolidao\b|\bisolamento\s+social\b",
    # Doenças neurodegenerativas
    r"\bdemencia\b|\balzheimer\b|\bparkinson\b",
    r"\bneurologico\b|\bneurologia\b|\bcerebro\b",
    # Funcionalidade e mobilidade
    r"\batividade\s+fisica\b|\bexercicio[s]?\b|\bmobilidade\b",
    r"\bautonomia\b|\bindependencia\b|\bfragilidade\b",
    r"\bqueda[s]?\b|\bfratura[s]?\b|\bequilibrio\b|\bmarcha\b",
    # Nutrição e sono
    r"\bnutricao\b|\balimentacao\b|\bsono\b",
    # Reabilitação e cuidados
    r"\breabilitacao\b|\bfisioterapia\b|\bmedicamento[s]?\b",
    r"\bhospital\b|\bclinica\b|\bmedico\b|\benfermagem\b",
    r"\bcuidador\b|\bcuidado\s+informal\b",
    # Mortalidade e doenças crônicas
    r"\bmorte\b|\bmortalidade\b|\bmorbidade\b",
    r"\bpressao\s+arterial\b|\bdiabetes\b|\bosteoporose\b",
    r"\bdoenca\s+cronica\b|\bmultimorbidade\b",
    # Aspectos sociais
    r"\binclusao\s+social\b|\bpolitica[s]?\s+publica[s]?\b|\bdireitos\b",
    r"\bvulnerabilidade\b|\bdesigualdade\b",
]]

# Termos que sozinhos já indicam artigo relevante (sem precisar de AND)
PATTERNS_STANDALONE = [re.compile(p, re.IGNORECASE) for p in [
    r"\bdemencia\b|\balzheimer\b|\bparkinson\b",
    r"\benvelhec\w+",                          # envelhecimento, envelhecer, envelhecemos...
    r"\bgeriatria\b|\bgerontologia\b",
    r"\blongevidade\b|\bvelhice\b",
    r"\bterceira\s+idade\b",
    r"\bsaude\s+(mental\s+)?do\s+idoso[as]?\b",  # saude do idoso, saude mental do idoso
    r"\bcuidado[s]?\s+(ao|de)\s+idoso[as]?\b",   # cuidado ao idoso, cuidado de idosos
]]

DATA_DIR = "data"
PDF_DIR = "data/pdfs"
ARTICLES_DIR = "data/articles"

REQUEST_DELAY = 2  # segundos entre requisições
MAX_WORKERS = 5      # requisições paralelas ao processar artigos
CHECKPOINT_FILE = "data/checkpoint.json"
