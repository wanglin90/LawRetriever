from sentence_transformers import SentenceTransformer
import json
from config import Config

model = SentenceTransformer('sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2')


def generate_law_embeddings(data_path):
    with open(data_path, 'r', encoding='utf-8') as f:
        articles = json.load(f)

    embeddings = []
    for article in articles:
        text = f"第{article['article_num']}条: {article['content']}"
        embedding = model.encode(text, normalize_embeddings=True)
        article["embedding"] = embedding.tolist()

    with open(Config.DATA_PATHS["embeddings"], "w", encoding="utf-8") as f:
        json.dump(articles, f, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    generate_law_embeddings(Config.DATA_PATHS["structured_json"])