import os

class Config:
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    PROJECT_DIR = os.path.join(BASE_DIR, "LawRetriever")

    DATA_PATHS = {
        "raw_pdf": os.path.join(PROJECT_DIR, "test_data/civil_code.pdf"),
        "structured_json": os.path.join(PROJECT_DIR, "data/civil_code_articles.json"),
        "embeddings": os.path.join(PROJECT_DIR, "data/civil_code_embeddings.json"),
        "faiss_index": os.path.join(PROJECT_DIR, "data/civil_code.index"),
        "id_metadata_json": os.path.join(PROJECT_DIR, "data/id_metadata.json")
    }

    MODEL_SETTINGS = {
        "embedding_model": "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2",
        "generation_model": "gpt-3.5-turbo"
    }