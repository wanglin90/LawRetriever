from fastapi import FastAPI
from pydantic import BaseModel
from retrieval.law_retriever import LawRetriever
from generation.answer_generator import generate_legal_answer
from config import Config

app = FastAPI()
retriever = LawRetriever(Config.DATA_PATHS["faiss_index"], Config.DATA_PATHS["id_metadata_json"])

class QueryRequest(BaseModel):
    question: str

@app.post("/ask")
async def ask_question(request: QueryRequest):
    # 检索
    results = retriever.search_articles(request.question)
    # 生成
    answer = generate_legal_answer(request.question, results[:3])
    return {"answer": answer}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)