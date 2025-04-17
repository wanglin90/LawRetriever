import json
import re
from pdf2image import convert_from_path
import pytesseract

# 1. OCR 提取 PDF 文本
def extract_text_from_pdf(pdf_path):
    images = convert_from_path(pdf_path, dpi=300, poppler_path='F:\\wanglin\\poppler-24.08.0\\Library\\bin', first_page=9, last_page=13)
    full_text = ""
    for image in images:
        pytesseract.pytesseract.tesseract_cmd = r"F:\tesseractocr\tesseract.exe"
        full_text += pytesseract.image_to_string(image, lang='chi_sim') + "\n"
    return full_text.replace(" " , "")

# 2. 正则提取结构化信息
def parse_structure(text):
    pattern = re.compile(
        r"(第([零一二三四五六七八九十百千]+)章\s*([^\n\r]*))|"       # group 1: 章，2: 章号，3: 章标题
        r"(第([零一二三四五六七八九十百千]+)节\s*([^\n\r]*))|"       # group 4: 节，5: 节号，6: 节标题
        r"(第([零一二三四五六七八九十百千]+)条)\s*([\s\S]*?)(?=(第[零一二三四五六七八九十百千]+条)|\Z)"  # group 7: 条，8: 条号，9: 内容
    )
    data = []
    chapter_title = section_title = None
    chapter_num = section_num = None

    for match in pattern.finditer(text):
        if match.group(1):  # 章
            chapter_num = match.group(2)
            chapter_title = match.group(3).strip()
        elif match.group(4):  # 节
            section_num = match.group(5)
            section_title = match.group(6).strip()
        elif match.group(7):  # 条
            article_title = match.group(7).strip()
            article_num = match.group(8).strip()
            content = match.group(9).strip().replace('\n', '')
            data.append({
                "chapter_num": chapter_num,
                "chapter_title": chapter_title,
                "section_num": section_num,
                "section_title": section_title,
                "article_num": article_num,
                "article_title": article_title,
                "content": content
            })
    return data

# 3. 主流程执行
pdf_path = "../test_data/civil_code.pdf"
text = extract_text_from_pdf(pdf_path)
structured_data = parse_structure(text)

# 4. 导出 JSON
with open("civil_code.json", "w", encoding="utf-8") as f:
    json.dump(structured_data, f, ensure_ascii=False, indent=2)

print("已成功提取并保存为 civil_code.json")
