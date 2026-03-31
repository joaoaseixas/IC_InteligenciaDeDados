BASE_URL = "https://theconversation.com/br"

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    )
}

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
    "saude", "bem-estar", "bem estar",
    "qualidade de vida", "cuidado", "cuidados",
    "doenca", "doencas", "tratamento",
    "mental", "cognitivo", "cognicao", "memoria",
    "demencia", "alzheimer", "parkinson",
    "depressao", "ansiedade", "solidao",
    "atividade fisica", "exercicio", "mobilidade",
    "nutricao", "alimentacao", "sono",
    "autonomia", "independencia", "fragilidade",
    "reabilitacao", "fisioterapia", "medicamento",
    "hospital", "clinica", "medico", "enfermagem",
    "morte", "mortalidade", "morbidade",
    "pressao arterial", "diabetes", "osteoporose",
    "queda", "quedas", "fratura", "osso",
    "cerebro", "neurologico", "neurologia",
    "andar", "marcha", "equilibrio"
]

# Termos que sozinhos já indicam artigo relevante (sem precisar de AND)
KEYWORDS_STANDALONE = [
    "demencia", "alzheimer", "parkinson",
    "envelhecimento", "envelhecemos", "envelhecer",
    "geriatria", "gerontologia",
    "longevidade", "velhice",
    "terceira idade"
]

DATA_DIR = "data"
PDF_DIR = "data/pdfs"
ARTICLES_DIR = "data/articles"

REQUEST_DELAY = 0.5  # segundos entre requisições
MAX_WORKERS = 5      # requisições paralelas ao processar artigos
CHECKPOINT_FILE = "data/checkpoint.json"
