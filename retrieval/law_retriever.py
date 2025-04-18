import faiss
import numpy as np
import json
from sentence_transformers import SentenceTransformer
from config import Config


class LawRetriever:
    def __init__(self, index_path, metadata_path):
        self.index = faiss.read_index(index_path)
        with open(metadata_path, 'r', encoding='utf-8') as f:
            self.id_metadata = json.load(f)
        self.model = SentenceTransformer('sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2')

    def search_articles(self, query, k=5):
        # 语义检索
        query_embedding = self.model.encode(query, normalize_embeddings=True)
        query_embedding = np.expand_dims(query_embedding, axis=0)
        distances, indices = self.index.search(query_embedding, k)

        # 获取结果
        results = []
        for idx in indices[0]:
            if str(idx) in self.id_metadata:
                results.append({
                    "article_number": self.id_metadata[str(idx)]["article_num"],
                    "content": self.id_metadata[str(idx)]["content"]
                })
        return results


if __name__ == "__main__":
    retriever = LawRetriever(Config.DATA_PATHS["faiss_index"], Config.DATA_PATHS["id_metadata_json"])
    print(retriever.search_articles("离婚后子女抚养权如何分配？"))