import streamlit as st
from google import genai

# 1. Konfigurasi Tampilan Tab Browser dengan nama SeHe.AI
st.set_page_config(page_title="SeHe.AI - Asisten Cerdas Nelayan", page_icon="🐟", layout="centered")

# 2. Desain Tampilan Depan / Header Utama (Ciri Khas Daerah Nelayan)
st.markdown("<h1 style='text-align: center; color: #0288d1;'>🐟 SeHe.AI 🐟</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-style: italic; color: #555;'>\"Asisten Digital Cerdas, Terinspirasi dari Tangguhnya Ikan Terbang Daerah Nelayan\"</p>", unsafe_allow_html=True)

# Menampilkan Ilustrasi Ikan Terbang Minimalis di Halaman Depan Web
st.code("""
         ______
       _/_/|  _\\_
   _.-'  / | /   `-._
 <'__   <  |/  _    _>     ===<*)))><  (Ikan Terbang SeHe.AI)
     `-. \\ | /  _.-'
        `-\\_|/_/
""", language="text")

st.caption("Aplikasi web AI interaktif bertenaga Google Gemini. Ringan untuk semua spesifikasi laptop.")
st.divider()

# 3. Masukkan API Key Gemini Anda di sini
# GANTI teks di dalam tanda kutip dengan API Key yang Anda salin dari Google AI Studio
GEMINI_API_KEY = "MASUKKAN_API_KEY_GEMINI_ANDA_DI_SINI"

# Inisialisasi klien resmi Google GenAI
client = genai.Client(api_key=GEMINI_API_KEY)

# 4. Wadah untuk menyimpan riwayat percakapan agar SeHe.AI ingat konteks chat
if "messages" not in st.session_state:
    st.session_state.messages = []

# 5. Menampilkan riwayat chat di layar web
for message in st.session_state.messages:
    # Mengubah ikon chat default menjadi lebih ramah sesuai tema nelayan
    avatar_icon = "🐟" if message["role"] == "assistant" else "👤"
    with st.chat_message(message["role"], avatar=avatar_icon):
        st.markdown(message["content"])

# 6. Kolom input chat di bagian bawah layar
if prompt := st.chat_input("Tanya sesuatu ke SeHe.AI..."):
    # Tampilkan pesan yang Anda ketik ke layar
    st.chat_message("user", avatar="👤").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Kirim pertanyaan beserta seluruh riwayat chat ke server Google
    try:
        with st.spinner("SeHe.AI sedang mengarungi lautan data..."):
            # Format riwayat pesan agar sesuai dengan kebutuhan struktur data Google
            formatted_contents = []
            for m in st.session_state.messages:
                role_name = "model" if m["role"] == "assistant" else "user"
                formatted_contents.append({"role": role_name, "parts": [{"text": m["content"]}]})
            
            # Memanggil model Gemini 2.5 Flash terbaru yang sangat cepat dan gratis
            response = client.models.generate_content(
                model='gemini-2.5-flash',
                contents=formatted_contents,
            )
            
            # Ambil teks jawaban dari Google
            ai_response = response.text

        # Tampilkan jawaban AI di layar web dengan avatar ikan
        with st.chat_message("assistant", avatar="🐟"):
            st.markdown(ai_response)
        st.session_state.messages.append({"role": "assistant", "content": ai_response})

    except Exception as e:
        st.error(f"Terjadi kesalahan: {e}. Pastikan API Key sudah benar dan laptop terhubung ke internet.")