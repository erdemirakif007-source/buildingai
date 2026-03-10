import os
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_qdrant import QdrantVectorStore
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage # 📸 FOTOĞRAF İÇİN EKLENDİ

# API Key (Şefim, ileride bunu .env dosyasına saklamanı öneririm)
os.environ["GOOGLE_API_KEY"] = "AIzaSyDSfjWCKfW3nJ7Asy7mT4RlXuAgvw6eOwk"

try:
    # Hafıza Modelini Kuruyoruz
    embeddings = HuggingFaceEmbeddings(
        model_name="all-MiniLM-L6-v2",
        model_kwargs={'device': 'cpu'}
    )

    vector_store = QdrantVectorStore.from_existing_collection(
        embedding=embeddings,
        collection_name="yonetmelikler_koleksiyonu",
        url="http://localhost:6333",
    )
except Exception as e:
    print(f"⚠️ Hafıza yüklenirken hata oluştu (Muhtemelen Qdrant kapalı): {e}")
    vector_store = None

try:
    fizik_store = QdrantVectorStore.from_existing_collection(
        embedding=embeddings,
        collection_name="fizik_koleksiyonu",
        url="http://localhost:6333",
    )
except Exception:
    fizik_store = None

# Zeka Modeli (Gemini 3.1 Pro)
llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.1)

# 🚨 DÜZELTME: resim_base64 parametresi eklendi
def cevap_uret(soru, hava_durumu="Bilinmiyor", resim_base64=None):
    try:
        # 1. RAG (Hafıza) Taraması: Her iki koleksiyonda ara ve birleştir
        baglam = ""
        try:
            parcalar = []
            if vector_store is not None:
                yonetmelik_docs = vector_store.similarity_search(soru, k=3)
                parcalar.extend([d.page_content for d in yonetmelik_docs])
            if fizik_store is not None:
                fizik_docs = fizik_store.similarity_search(soru, k=2)
                parcalar.extend([d.page_content for d in fizik_docs])
            baglam = "\n".join(parcalar)
        except Exception:
            pass  # Qdrant kapalıysa çökmeden devam et
        
        # 2. Şefin Ana Talimatı (Sivas ve Yönetmelik Birleşimi)
        # 2. Şefin Ana Talimatı (DİNAMİK KONUM)
        text_prompt = (
            f"Sen, 30 yıllık deneyime sahip, teknik detaylara aşırı hakim, nezaket kurallarından asla ödün vermeyen kıdemli bir Başmühendissin. Görevin; kullanıcıya hatalarını yüzüne vurmak değil, projeyi en güvenli ve standartlara uygun şekilde tamamlaması için profesyonel rehberlik etmektir."
            f"Şu anki şantiye konumun ve hava durumun: {hava_durumu}. "
            "Bulunduğun bu bölgenin iklim şartlarına ve teknik verilere dayanarak net cevap ver. Risk varsa uyar.\n"
            "Yanıt verirken 'Durum Analizi' ve 'Acil Aksiyon Planı' olarak iki kısa bölüme ayır. Toplamda 3-4 cümleyi ve 3-4 maddeyi geçme. Mühendislik ciddiyetini koru ama laf kalabalığı yapma."
        )
        if baglam:
            text_prompt += f"\n[YÖNETMELİK BİLGİSİ]:\n{baglam}\n"
        
        text_prompt += f"\n[SORU/TALİMAT]: {soru}"

        # 3. 📸 FOTOĞRAF KONTROLÜ VE YÜKLEME (LangChain Mantığı)
        if resim_base64:
            # Ön yüzden gelen veride 'data:image...' tag'i yoksa sistemi bozmamak için ekliyoruz
            if not resim_base64.startswith("data:image"):
                resim_base64 = f"data:image/jpeg;base64,{resim_base64}"
            
            # LangChain'in fotoğraf okuyabildiği özel 'HumanMessage' formatı
            mesaj = HumanMessage(
                content=[
                    {"type": "text", "text": text_prompt + "\n\nEkrandaki fotoğrafı bir mühendis gözüyle (çatlak, donatı, İSG vb.) detaylıca analiz et."},
                    {"type": "image_url", "image_url": {"url": resim_base64}}
                ]
            )
            # Hem metni hem fotoğrafı yolla
            cevap = llm.invoke([mesaj])
        else:
            # Fotoğraf yoksa eski usul sadece metin gönder
            cevap = llm.invoke(text_prompt)
            
        # 3. Fotoğraf Yükleme ve Analiz
        if resim_base64:
            if not resim_base64.startswith("data:image"):
                resim_base64 = f"data:image/jpeg;base64,{resim_base64}"
            
            mesaj = HumanMessage(
                content=[
                    {"type": "text", "text": text_prompt + "\n\nEkrandaki fotoğrafı bir mühendis gözüyle (çatlak, donatı, İSG vb.) detaylıca analiz et."},
                    {"type": "image_url", "image_url": {"url": resim_base64}}
                ]
            )
            cevap = llm.invoke([mesaj])
        else:
            cevap = llm.invoke(text_prompt)
            
        # 🚨 DÜZELTME: LangChain'in karmaşık cevabını temiz metne çevirme 🚨
        if isinstance(cevap.content, list):
            # Eğer cevap liste/sözlük olarak geldiyse içindeki sadece 'text' kısmını al
            temiz_metin = "".join([item['text'] for item in cevap.content if 'text' in item])
            return temiz_metin
        else:
            # Standart metinse doğrudan gönder
            return str(cevap.content)

    except Exception as e:
        return f"Şefim, zeka şu an meşgul veya bağlantı koptu. Hata: {str(e)}"