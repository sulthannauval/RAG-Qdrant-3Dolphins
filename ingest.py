from qdrant_client import QdrantClient, models
from sentence_transformers import SentenceTransformer

# 1. Inisialisasi model embedding untuk mengubah teks menjadi vektor
encoder = SentenceTransformer('all-MiniLM-L6-v2')

# 2. Hubungkan ke Qdrant
client = QdrantClient(host='localhost', port=6333)

# 3. Siapkan nama koleksi
collection_name = "european_league_champions_2025"

# 4. Buat ulang koleksi agar selalu mulai dari keadaan bersih
client.recreate_collection(
    collection_name=collection_name,
    vectors_config=models.VectorParams(
        size=encoder.get_sentence_embedding_dimension(), # Ukuran vektor 384
        distance=models.Distance.COSINE
    )
)

# 5. Siapkan dokumen yang akan dimasukkan
# Data ini berisi para juara liga sepak bola top Eropa musim 2024-2025.
documents = [
    "Juara Liga Premier Inggris musim 2024-2025 adalah Liverpool.",
    "Barcelona berhasil menjuarai La Liga Spanyol pada musim 2024-2025.",
    "Di Italia, Napoli memenangkan gelar juara Serie A untuk musim 2024-2025.",
    "Bayern Munich kembali menjadi juara Bundesliga Jerman di musim 2024-2025.",
    "Paris Saint-Germain (PSG) adalah pemenang Ligue 1 Prancis musim 2024-2025."
]

# 6. Lakukan proses ingesti ke Qdrant
client.upload_records(
    collection_name=collection_name,
    records=[
        models.Record(
            id=idx,
            vector=encoder.encode(doc).tolist(),
            payload={'text': doc}
        ) for idx, doc in enumerate(documents)
    ]
)

print(f"Berhasil ingest {len(documents)} dokumen ke koleksi '{collection_name}'.")