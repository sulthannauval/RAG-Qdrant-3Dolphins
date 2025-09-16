# RAG System: European Football Champions 2025

Proyek ini adalah implementasi sistem Retrieval-Augmented Generation (RAG) untuk menjawab pertanyaan tentang juara liga sepak bola Eropa musim 2024-2025, sebagai bagian dari "Take Home Quiz: Python Developer".

## Teknologi
- **Python**: Bahasa pemrograman utama.
- **FastAPI**: Kerangka kerja untuk membangun API.
- **Qdrant**: Database vektor untuk pencarian kemiripan.
- **Sentence-Transformers**: Untuk membuat embedding teks.
- **Google Gemini**: Model Bahasa Besar (LLM) untuk menghasilkan jawaban.
- **Docker**: Untuk menjalankan Qdrant.

## Setup & Instalasi
1.  **Prasyarat**: Python 3.8+, Docker.
2.  **Clone Repositori**:
    ```bash
    git clone https://github.com/sulthannauval/RAG-Qdrant-3Dolphins/
    cd [NAMA_FOLDER]
    ```
3.  **Buat & Aktifkan Virtual Environment**:
    ```bash
    # Windows (PowerShell)
    python -m venv .venv
    .\.venv\Scripts\activate
    ```
4.  **Install Dependensi**:
    ```bash
    pip install -r requirements.txt
    ```
5.  **Siapkan API Key**:
    Dapatkan API Key dari Google AI Studio dan atur sebagai environment variable:
    ```powershell
    $env:GOOGLE_API_KEY="MASUKKAN_API_KEY_ANDA_DI_SINI"
    ```
6.  **Jalankan Qdrant**:
    ```bash
    docker run -p 6333:6333 -p 6334:6334 -v "$(pwd)/qdrant_storage:/qdrant/storage:z" qdrant/qdrant
    ```

## Cara Menjalankan Proyek
1.  **Ingesti Data ke Qdrant (Jalankan sekali)**:
    ```bash
    python ingest.py
    ```
2.  **Jalankan Server API**:
    ```bash
    uvicorn main:app --reload
    ```
    Buka `http://127.0.0.1:8000/docs` untuk mengakses Swagger UI.

## Contoh Penggunaan API

[cite_start]**Contoh Input JSON:** 
```json
{
  "question": "siapa juara liga inggris tahun 2025?"
}
```

[cite_start]**Contoh Output JSON:** 
```json
{
  "answer": "Liverpool",
  "retrieved_context": [
    "Juara Liga Premier Inggris musim 2024-2025 adalah Liverpool."
  ]
}
```
