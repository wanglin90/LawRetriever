import os
import sys

def get_base_path():
    """
    获取项目运行的基础路径：
    - 开发环境：返回项目的根目录
    - 打包后：返回 PyInstaller 解压后的临时路径
    """
    if hasattr(sys, '_MEIPASS'):
        return sys._MEIPASS  # PyInstaller 临时目录
    return os.path.dirname(os.path.abspath(__file__))

class Config:

    BASE_DIR = get_base_path()

    DATA_PATHS = {
        "raw_pdf": os.path.join(BASE_DIR, "test_data", "civil_code.pdf"),
        "structured_json": os.path.join(BASE_DIR, "data", "civil_code_articles.json"),
        "embeddings": os.path.join(BASE_DIR, "data", "civil_code_embeddings.json"),
        "faiss_index": os.path.join(BASE_DIR, "data", "civil_code.index"),
        "id_metadata_json": os.path.join(BASE_DIR, "data", "id_metadata.json")
    }

    MODEL_SETTINGS = {
        "embedding_model": "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2",
        "generation_model": "gpt-3.5-turbo"
    }