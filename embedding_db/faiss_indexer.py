import faiss
import numpy as np
import json
from config import  Config


def build_faiss_index(embeddings_path):
    with open(embeddings_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    embeddings = np.array([item["embedding"] for item in data], dtype=np.float32)
    dimension = embeddings.shape[1]

    index = faiss.IndexFlatL2(dimension)
    index.add(embeddings)
    faiss.write_index(index, Config.DATA_PATHS["faiss_index"])

    # 存储元数据映射
    id_to_metadata = {
        str(i): {
            "article_num": item["article_num"],
            "content": item["content"]
        }
        for i, item in enumerate(data)}

    with open(Config.DATA_PATHS["id_metadata_json"], "w", encoding="utf-8") as f:
        json.dump(id_to_metadata, f, ensure_ascii=False)


if __name__ == "__main__":
    build_faiss_index(Config.DATA_PATHS["embeddings"])