import os
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_qdrant import QdrantVectorStore

# Fizik klasörü yoksa oluştur
os.makedirs("./Fizik", exist_ok=True)

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200
)

print("🧠 Embedding modeli yükleniyor...")
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

qdrant_url = "http://localhost:6333"

# --- Koleksiyon 1: Yönetmelikler ---
print("\n🏗️ 1. Adım: Yönetmelikler klasörü okunuyor...")
loader1 = PyPDFDirectoryLoader("./Yönetmelikler")
docs1 = loader1.load()
chunks1 = text_splitter.split_documents(docs1)
print(f"Toplam {len(chunks1)} adet yönetmelik parçacığı oluşturuldu.")

print("💾 Yönetmelikler Qdrant'a yazılıyor...")
QdrantVectorStore.from_documents(
    chunks1,
    embeddings,
    url=qdrant_url,
    collection_name="yonetmelikler_koleksiyonu"
)
print("✅ Yönetmelikler koleksiyonu tamamlandı.")

# --- Koleksiyon 2: Fizik ---
print("\n📐 2. Adım: Fizik klasörü okunuyor...")
loader2 = PyPDFDirectoryLoader("./Fizik")
docs2 = loader2.load()

if docs2:
    chunks2 = text_splitter.split_documents(docs2)
    print(f"Toplam {len(chunks2)} adet fizik parçacığı oluşturuldu.")
    print("💾 Fizik verileri Qdrant'a yazılıyor...")
    QdrantVectorStore.from_documents(
        chunks2,
        embeddings,
        url=qdrant_url,
        collection_name="fizik_koleksiyonu"
    )
    print("✅ Fizik koleksiyonu tamamlandı.")
else:
    print("⚠️ Fizik klasörü boş — PDF eklendiğinde tekrar çalıştırın.")

print("\n✅ BAŞARILI! Tüm veriler yapay zekanın beynine kalıcı olarak işlendi.")
