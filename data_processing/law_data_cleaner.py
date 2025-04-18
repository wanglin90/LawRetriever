import json
import re

def clean_articles(input_path: str, output_path: str):
    """清洗法律条文数据"""
    with open(input_path, "r", encoding="utf-8") as f:
        raw_data = json.load(f)

    cleaned = []
    for article in raw_data:
        # 去除多余空格和换行符
        clean_content = re.sub(r"\s+", " ", article["content"]).strip()
        # # 添加清洗规则（示例）
        # if len(clean_content) < 5: continue  # 过滤无效条目

        cleaned.append({
            "article_num": article["article_id"],
            "content": clean_content,
            "metadata": article["metadata"]
        })

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(cleaned, f, ensure_ascii=False, indent=2)