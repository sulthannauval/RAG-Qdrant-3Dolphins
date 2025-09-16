import os
import google.generativeai as genai
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from qdrant_client import QdrantClient
from sentence_transformers import SentenceTransformer

# --- Konfigurasi dan Inisialisasi ---
app = FastAPI(
    title="European Football Champions RAG API",
    description="API untuk menjawab pertanyaan seputar juara liga di eropa 2025 menggunakan RAG."
)

# Konfigurasi Google AI API Key dari environment variable
try:
    api_key = os.environ['GOOGLE_API_KEY']
    genai.configure(api_key=api_key)
except KeyError:
    raise RuntimeError("GOOGLE_API_KEY environment variable tidak diatur.")

# Muat model embedding dan hubungkan ke Qdrant
encoder = SentenceTransformer('all-MiniLM-L6-v2')
qdrant_client = QdrantClient(host='localhost', port=6333)
collection_name = "european_league_champions_2025"

# --- Model Data Pydantic ---
class QuestionRequest(BaseModel):
    question: str

class AnswerResponse(BaseModel):
    answer: str
    retrieved_context: list[str]

# --- Fungsi Inti RAG ---
def construct_prompt(question: str, context: list[str]) -> str:
    context_str = "\n\n".join(context)
    prompt = f"""
    Anda adalah asisten AI ahli sepak bola. Jawab pertanyaan berikut HANYA berdasarkan konteks yang diberikan.
    Jika informasi tidak ada di dalam konteks, katakan 'Informasi tersebut tidak ditemukan dalam data saya'.

    Konteks:
    {context_str}

    Pertanyaan: {question}
    Jawaban:
    """
    return prompt

def call_llm(prompt: str):
    try:
        model = genai.GenerativeModel('gemini-1.5-flash-latest')
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print(f"Error saat memanggil Gemini API: {e}")
        return "Maaf, terjadi kesalahan saat menghubungi layanan AI."

# --- API Endpoint ---
@app.post("/ask", response_model=AnswerResponse)
async def ask_question(request: QuestionRequest):
    # 1. Ubah pertanyaan menjadi vektor
    question_vector = encoder.encode(request.question).tolist()

    # 2. Cari dokumen relevan di Qdrant
    search_results = qdrant_client.search(
        collection_name=collection_name,
        query_vector=question_vector,
        limit=2
    )
    retrieved_context = [hit.payload['text'] for hit in search_results]
    
    # 3. Buat prompt yang diperkaya dengan konteks
    prompt = construct_prompt(request.question, retrieved_context)

    # 4. Kirim prompt ke LLM untuk mendapatkan jawaban
    llm_answer = call_llm(prompt)

    # 5. Kembalikan jawaban dan konteks yang digunakan
    return AnswerResponse(
        answer=llm_answer,
        retrieved_context=retrieved_context
    )