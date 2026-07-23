import streamlit as st
from google import genai
from google.genai import types
import os

# 1. Konfigurasi Tampilan Tab Browser dengan nama SeHe.AI
st.set_page_config(page_title="SeHe.AI - Asisten Cerdas Nelayan", page_icon="🐟", layout="centered")

# Custom CSS untuk tampilan premium minimalis, animasi ikan, & background lautan hidup
st.markdown("""
<style>
    /* ------------------------------------------------------------- */
    /* ELEMEN MINIMALIS: MENYEMBUNYIKAN HEADER, GITHUB, & DEKORASI   */
    /* ------------------------------------------------------------- */
    header {visibility: hidden !important; height: 0px !important;}
    footer {visibility: hidden !important;}
    .viewerBadge_link__1S137 {display: none !important;}
    [data-testid="stStatusWidget"] {visibility: hidden !important;}
    [data-testid="stDecoration"] {display: none !important;}
    
    /* Mengurangi ruang kosong (padding) atas yang terlalu besar */
    .block-container {
        padding-top: 2rem !important;
        padding-bottom: 2rem !important;
        max-width: 1000px !important;
        position: relative;
        z-index: 2;
    }

    /* Import Font Premium */
    @import url('https://googleapis.com');
    * { font-family: 'Plus Jakarta Sans', sans-serif; }
    
    /* ------------------------------------------------------------- */
    /* LATER BELAKANG LAUTAN & ANIMASI BIOTA LAUT (IKAN & GELEMBUNG) */
    /* ------------------------------------------------------------- */
    .stApp {
        background: linear-gradient(135deg, #060a12 0%, #013152 50%, #001f22 100%);
        background-attachment: fixed;
        overflow-x: hidden;
    }

    /* Membuat kontainer animasi di latar belakang */
    .stApp::before {
        content: "";
        position: fixed;
        top: 0; left: 0; width: 100%; height: 100%;
        background-image: 
            /* Gambar Ikan 1 */
            url('data:image/svg+xml;utf8,<svg xmlns="http://w3.org" width="30" height="20" viewBox="0 0 30 20"><path d="M5,10 C12,4 22,5 26,10 C22,15 12,16 5,10 Z M26,10 L30,6 L28,10 L30,14 Z" fill="rgba(38, 198, 218, 0.25)"/><circle cx="8" cy="9" r="1" fill="rgba(255,255,255,0.4)"/></svg>'),
            /* Gambar Ikan 2 */
            url('data:image/svg+xml;utf8,<svg xmlns="http://w3.org" width="24" height="16" viewBox="0 0 24 16"><path d="M4,8 C10,3 18,4 21,8 C18,12 10,13 4,8 Z M21,8 L24,5 L22,8 L24,11 Z" fill="rgba(3, 169, 244, 0.2)"/><circle cx="7" cy="7" r="0.8" fill="rgba(255,255,255,0.4)"/></svg>'),
            /* Gelembung Udara */
            url('data:image/svg+xml;utf8,<svg xmlns="http://w3.org" width="10" height="10" viewBox="0 0 10 10"><circle cx="5" cy="5" r="3" stroke="rgba(255,255,255,0.15)" stroke-width="0.8" fill="none"/></svg>'),
            url('data:image/svg+xml;utf8,<svg xmlns="http://w3.org" width="14" height="14" viewBox="0 0 14 14"><circle cx="7" cy="7" r="5" stroke="rgba(255,255,255,0.1)" stroke-width="0.8" fill="none"/></svg>');
        background-position: 10% 20%, 85% 60%, 30% 80%, 75% 30%;
        background-repeat: no-repeat;
        animation: oceanMove 25s infinite linear;
        z-index: 1;
        pointer-events: none;
    }

    /* Gerakan Arus Alami Bawah Laut */
    @keyframes oceanMove {
        0% { background-position: -5% 20%, 105% 60%, 30% 110%, 75% 110%; }
        50% { background-position: 50% 18%, 45% 63%, 33% 50%, 72% 40%; }
        100% { background-position: 105% 20%, -5% 60%, 36% -10%, 70% -10%; }
    }
    
    /* ------------------------------------------------------------- */
    /* NAVIGASI & SIDEBAR MINIMALIS (GLASSMORPHISM)                  */
    /* ------------------------------------------------------------- */
    [data-testid="stSidebar"] {
        background: rgba(6, 10, 18, 0.7) !important;
        backdrop-filter: blur(20px);
        border-right: 1px solid rgba(255, 255, 255, 0.05);
        z-index: 3;
    }
    
    /* AREA CHAT & INPUT UTAMA */
    .stChatMessage {
        background: rgba(255, 255, 255, 0.03) !important;
        backdrop-filter: blur(12px);
        border: 1px solid rgba(255, 255, 255, 0.05) !important;
        border-radius: 12px !important;
        margin-bottom: 12px !important;
        padding: 15px !important;
        color: #f1f5f9 !important;
    }
    
    [data-testid="stChatInput"] {
        border-radius: 12px !important;
        border: 1px solid rgba(255, 255, 255, 0.08) !important;
        background-color: rgba(10, 18, 32, 0.85) !important;
        backdrop-filter: blur(10px);
    }
    
    ::-webkit-scrollbar { width: 6px; }
    ::-webkit-scrollbar-track { background: transparent; }
    ::-webkit-scrollbar-thumb { background: rgba(3, 169, 244, 0.2); border-radius: 10px; }
</style>
""", unsafe_allow_html=True)

# 2. Desain Tampilan Depan / Header Utama (Posisi Kredit Digeser ke Kanan Bawah)
st.html("""
<div style="text-align: center; margin-bottom: 20px; font-family: sans-serif; position: relative;">
<svg width="220" height="130" viewBox="0 0 220 150" fill="none" xmlns="http://w3.org" style="display: block; margin: 0 auto;">
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
<div style="display: inline-block; text-align: left; position: relative;">
    <h1 style="color: #03a9f4; margin: 0; font-size: 36px; font-weight: bold; letter-spacing: 0.5px; display: inline-block;">SeHe.AI</h1>
    <span style="font-size: 11px; color: rgba(255, 255, 255, 0.4); font-style: italic; position: absolute; bottom: -8px; right: 2px; white-space: nowrap;">by rikoba</span>
</div>
</div>
""", unsafe_allow_html=True)

st.divider()

# 3. Membaca API Key secara aman dari sistem Secrets Streamlit
if "GEMINI_API_KEY" in st.secrets:
    GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]
else:
    GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")

if not GEMINI_API_KEY:
    st.error("API Key Gemini belum diatur di menu Secrets!")
    st.stop()

# --- Menyimpan Client di session_state agar koneksi tidak terputus ---
if "gemini_client" not in st.session_state:
    st.session_state.gemini_client = genai.Client(api_key=GEMINI_API_KEY)

# 4. Konfigurasi Karakter (System Instruction), Akses Internet & Desain Dokumen
ai_config = types.GenerateContentConfig(
    system_instruction=(
        "Anda adalah SeHe.AI, asisten cerdas, profesional, dan ramah yang dirancang khusus untuk "
        "membantu nelayan dan pembudidaya pesisir. Anda memiliki keahlian teknis dalam bidang perikanan, "
        "teknologi tepat guna kelautan, budidaya kerang mutiara (Pinctada maxima), teknik perakitan longline, "
        "desain sistem penjangkaran, hingga desain wadah budidaya mandiri. "
        "PENTING 1: Jika pengguna menanyakan cuaca, tinggi gelombang, atau data terkini, WAJIB gunakan alat Google Search. "
        "PENTING 2: Jika pengguna meminta Anda membuat dokumen, laporan, surat, atau proposal, buatlah desain tampilan menggunakan elemen HTML dan inline CSS (tanpa tag markdown ```html). Gunakan warna latar belakang, tipografi, bingkai, atau tabel yang elegan dan warnanya otomatis menyesuaikan tema/konteks dokumen tersebut."
    ),
    temperature=0.7, 
    tools=[{"google_search": {}}]
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
for i, message in enumerate(st.session_state.messages):
    avatar_icon = "🐟" if message["role"] == "assistant" else "👤"
    with st.chat_message(message["role"], avatar=avatar_icon):
        st.markdown(message["content"], unsafe_allow_html=True)
        
        # --- FITUR BARU: Menambahkan tombol download untuk setiap jawaban riwayat AI ---
        if message["role"] == "assistant":
            st.download_button(
                label="⬇️ Download sebagai HTML",
                data=message["content"],
                file_name=f"Dokumen_SeHe_AI_{i}.html",
                mime="text/html",
                key=f"dl_btn_{i}"
            )

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
