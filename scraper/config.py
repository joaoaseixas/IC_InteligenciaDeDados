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

DATA_DIR = "data"
PDF_DIR = "data/pdfs"
ARTICLES_DIR = "data/articles"

REQUEST_DELAY = 0.5  # segundos entre requisições
MAX_WORKERS = 5      # requisições paralelas ao processar artigos
CHECKPOINT_FILE = "data/checkpoint.json"
