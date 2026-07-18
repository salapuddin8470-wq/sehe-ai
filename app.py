import streamlit as st
import google.generativeai as genai
import os

# 1. Konfigurasi Tampilan Tab Browser dengan nama SeHe.AI
st.set_page_config(page_title="SeHe.AI - Asisten Cerdas Nelayan", page_icon="🐟", layout="centered")

# 2. Desain Tampilan Depan / Header Utama (Menggunakan Ilustrasi Ikan Torani/Taroni)
# Tautan gambar menggunakan ilustrasi ikan terbang digital yang transparan dan sangat ringan
url_ikan_terbang = "https://githubusercontent.com" # Contoh ilustrasi, Anda bisa menggantinya nanti jika memiliki aset gambar sendiri

# Mengatur tata letak logo agar gambar ikan mengapit teks SeHe.AI dengan rapi
col1, col2, col3 = st.columns([1, 2, 1])

with col1:
    # Ikan terbang sisi kiri (menghadap ke kanan)
    st.image("https://wikimedia.org", width=70)

with col2:
    st.markdown("<h1 style='text-align: center; color: #0288d1; margin-top: 10px; margin-bottom: 0;'>SeHe.AI</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; font-size: 15px; color: #666; font-weight: bold; margin-top: 0;'>by rikoba</p>", unsafe_allow_html=True)

with col3:
    # Ikan terbang sisi kanan (efek dibalik menghadap ke kiri menggunakan CSS html)
    st.markdown("<div style='text-align: right;'><img src='https://wikimedia.org' style='transform: scaleX(-1);' width='70'></div>", unsafe_allow_html=True)

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
