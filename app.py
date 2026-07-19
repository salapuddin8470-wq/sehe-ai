import streamlit as st
from google import genai
from google.genai import types
import os

# 1. Konfigurasi Tampilan Tab Browser dengan nama SeHe.AI
st.set_page_config(page_title="SeHe.AI - Asisten Cerdas Nelayan", page_icon="🐟", layout="centered")

# 2. Desain Tampilan Depan / Header Utama (Versi html Murni Tanpa Bug Kotak Abu-abu)
st.html("""
<div style="text-align: center; margin-bottom: 20px; font-family: sans-serif;">
<svg width="220" height="150" viewBox="0 0 220 150" fill="none" xmlns="http://w3.org" style="display: block; margin: 0 auto;">
<path d="M20 125 C 40 125, 45 105, 55 105 C 65 105, 62 120, 52 122 C 45 123, 40 115, 48 110 C 53 107, 60 112, 58 116" stroke="#0288d1" stroke-width="3" stroke-linecap="round" fill="none"/>
<path d="M15 130 C 50 130, 70 126, 100 126 C 140 126, 170 131, 205 130" stroke="#0288d1" stroke-width="2.5" stroke-linecap="round"/>
<path d="M35 135 C 75 135, 95 132, 130 132 C 160 132, 180 136, 200 135" stroke="#0288d1" stroke-width="1.5" stroke-dasharray="4 4" stroke-linecap="round"/>
<g transform="translate(65, 30) rotate(-12)">
<path d="M10 40 C 25 35, 55 35, 75 52 C 60 55, 30 52, 10 40 Z" fill="#0288d1"/>
<path d="M42 37 C 45 15, 75 5, 85 8 C 80 15, 65 25, 48 37 Z" fill="#03a9f4" opacity="0.85"/>
<path d="M45 43 C 50 55, 68 62, 72 60 C 68 55, 58 48, 47 43 Z" fill="#03a9f4" opacity="0.7"/>
<path d="M10 40 L 0 33 L 3 40 L 0 47 Z" fill="#0288d1"/>
<circle cx="70" cy="46" r="2" fill="white"/>
</g>
</svg>
<h1 style="color: #0288d1; margin-top: -10px; margin-bottom: 0; font-size: 34px; font-weight: bold; letter-spacing: 0.5px;">SeHe.AI</h1>
<p style="font-size: 14px; color: #777; font-weight: 600; margin-top: 3px; margin-bottom: 0; letter-spacing: 1px;">by rikoba</p>
</div>
""")

st.divider()

# 3. Membaca API Key secara aman dari sistem Secrets Streamlit
if "GEMINI_API_KEY" in st.secrets:
    GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]
else:
    GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")

if not GEMINI_API_KEY:
    st.error("API Key Gemini belum diatur di menu Secrets!")
    st.stop()

# --- PERBAIKAN UTAMA: Menyimpan Client di session_state agar koneksi tidak terputus ---
if "gemini_client" not in st.session_state:
    st.session_state.gemini_client = genai.Client(api_key=GEMINI_API_KEY)

# 4. Konfigurasi Karakter (System Instruction) & Akses Internet
ai_config = types.GenerateContentConfig(
    system_instruction=(
        "Anda adalah SeHe.AI, asisten cerdas, profesional, dan ramah yang dirancang khusus untuk "
        "membantu nelayan dan pembudidaya pesisir. Anda memiliki keahlian teknis dalam bidang perikanan, "
        "teknologi tepat guna kelautan, budidaya kerang mutiara (Pinctada maxima), teknik perakitan longline, "
        "desain sistem penjangkaran (termasuk pemberat/batu peredam), hingga desain wadah budidaya mandiri. "
        "Anda sangat memahami kondisi dan tantangan maritim pesisir, khususnya karakteristik perairan seperti di Sumbawa, NTB. "
        "Selalu berikan panduan yang praktis, masuk akal, aman, dan solutif. "
        "PENTING: Jika pengguna menanyakan kondisi cuaca, tinggi gelombang, pasang surut air laut, atau informasi terkini lainnya, "
        "Anda WAJIB menggunakan alat penelusuran (Google Search) untuk memberikan data yang paling akurat, real-time, dan relevan dengan lokasi pengguna saat ini."
    ),
    temperature=0.7, 
    tools=[{"google_search": {}}] # <--- FITUR BARU: Memberikan akses internet agar AI bisa melihat cuaca BMKG secara langsung
)

# 5. Inisialisasi Memori Obrolan (Chat Session) menggunakan Client yang sudah disimpan
if "chat_session" not in st.session_state:
    st.session_state.chat_session = st.session_state.gemini_client.chats.create(
        model='gemini-2.5-flash',
        config=ai_config
    )

# 6. Wadah untuk menyimpan riwayat percakapan khusus untuk tampilan layar
if "messages" not in st.session_state:
    st.session_state.messages = []

# 7. Menampilkan riwayat chat di layar web
for message in st.session_state.messages:
    avatar_icon = "🐟" if message["role"] == "assistant" else "👤"
    with st.chat_message(message["role"], avatar=avatar_icon):
        st.markdown(message["content"])

# 8. Kolom input chat di bagian bawah layar
if prompt := st.chat_input("Tanya sesuatu ke SeHe.AI..."):
    # Tampilkan pesan yang Anda ketik ke layar
    st.chat_message("user", avatar="👤").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Kirim pertanyaan menggunakan metode Chat Session agar riwayat diingat oleh AI
    try:
        with st.spinner("SeHe.AI sedang mengarungi lautan data..."):
            response = st.session_state.chat_session.send_message(prompt)
            ai_response = response.text

        # Tampilkan jawaban AI di layar web dengan avatar ikan
        with st.chat_message("assistant", avatar="🐟"):
            st.markdown(ai_response)
        st.session_state.messages.append({"role": "assistant", "content": ai_response})

    except Exception as e:
        st.error(f"Terjadi kesalahan: {e}. Pastikan internet Anda aktif.")
