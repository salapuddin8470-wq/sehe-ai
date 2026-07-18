import streamlit as st
import google.generativeai as genai
import os

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

st.caption("Aplikasi web AI interaktif bertenaga Google Gemini.")
st.divider()

# 3. Membaca API Key secara aman dari sistem Secrets Streamlit
if "GEMINI_API_KEY" in st.secrets:
    GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]
else:
    GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")

if not GEMINI_API_KEY:
    st.error("API Key Gemini belum diatur di menu Secrets!")
    st.stop()

# Inisialisasi API Google Gemini versi stabil
genai.configure(api_key=GEMINI_API_KEY)

# 4. Wadah untuk menyimpan riwayat percakapan agar SeHe.AI ingat konteks chat
if "messages" not in st.session_state:
    st.session_state.messages = []

# 5. Menampilkan riwayat chat di layar web
for message in st.session_state.messages:
    avatar_icon = "🐟" if message["role"] == "assistant" else "👤"
    with st.chat_message(message["role"], avatar=avatar_icon):
        st.markdown(message["content"])

# 6. Kolom input chat di bagian bawah layar
if prompt := st.chat_input("Tanya sesuatu ke SeHe.AI..."):
    # Tampilkan pesan yang Anda ketik ke layar
    st.chat_message("user", avatar="👤").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Kirim pertanyaan ke server Google menggunakan metode versi stabil
    try:
        with st.spinner("SeHe.AI sedang mengarungi lautan data..."):
            model = genai.GenerativeModel('gemini-2.5-flash')
            response = model.generate_content(prompt)
            ai_response = response.text

        # Tampilkan jawaban AI di layar web dengan avatar ikan
        with st.chat_message("assistant", avatar="🐟"):
            st.markdown(ai_response)
        st.session_state.messages.append({"role": "assistant", "content": ai_response})

    except Exception as e:
        st.error(f"Terjadi kesalahan: {e}. Pastikan internet Anda aktif.")
