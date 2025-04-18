import tkinter as tk
from tkinter import scrolledtext

from config import Config
from generation.answer_generator import Generator
from retrieval.law_retriever import LawRetriever


class App:
    def __init__(self, root):
        # GUI
        self.root = root
        root.title("中国民法典个人小助手")

        # 设置初始窗口尺寸
        root.geometry("800x600")  # 新增：初始窗口大小
        root.minsize(800, 600)  # 新增：最小尺寸限制


        # API密鑰輸入
        self.api_label = tk.Label(root, text="Deepseek API 密钥:")
        self.api_label.pack()
        self.api_entry = tk.Entry(root, width=80)
        self.api_entry.pack()

        # 輸入框
        self.input_label = tk.Label(root, text="输入你想问的问题:")
        self.input_label.pack()
        self.input_entry = tk.Entry(root, width=80)
        self.input_entry.pack()

        # 生成按鈕
        self.generate_btn = tk.Button(root, text="提交", command=self.generate)
        self.generate_btn.pack(pady=10)


        # 結果展示
        self.title_label = tk.Label(root, text="回答内容:")
        self.title_label.pack()
        self.title_text = scrolledtext.ScrolledText(root, height=15)
        self.title_text.pack()

        self.retriever = LawRetriever(Config.DATA_PATHS["faiss_index"], Config.DATA_PATHS["id_metadata_json"])

    def generate(self):
        generator = Generator(self.api_entry.get())
        # 检索
        results = self.retriever.search_articles(self.input_entry.get())
        # 生成
        answer = generator.generate_legal_answer(self.input_entry.get(), results)

        self.title_text.delete('1.0', tk.END)
        self.title_text.insert(tk.END, answer)


if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()