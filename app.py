
import streamlit as st
from google import genai
from google.genai import types
import os

# 1. Konfigurasi Tampilan Tab Browser dengan nama SeHe.AI
st.set_page_config(page_title="SeHe.AI - Asisten Cerdas Nelayan", page_icon="🐟", layout="centered")

# Custom CSS Premium, Ringan, Minimalis & Kontras Tinggi (Anti Tulisan Samar)
st.markdown("""
<style>
    /* ------------------------------------------------------------- */
    /* ------------------------------------------------------------- */
/* MENYEMBUNYIKAN LOGO MERAH TANPA MENGGANGGU APP MANAGER ADMIN  */
/* ------------------------------------------------------------- */
header {visibility: hidden !important; height: 0px !important;}
footer {visibility: hidden !important;}
[data-testid="stDecoration"] {display: none !important;}

/* HANYA MENYEMBUNYIKAN LOGO STREAMLIT MERAH DI HP ORANG LAIN */
.viewerBadge_link__1S137, 
[data-testid="stViewerBadge"], 
a[href*="streamlit.io"] {
    display: none !important;
    visibility: hidden !important;
    opacity: 0 !important;
    height: 0px !important;
}

/* CATATAN: Kode [data-testid="stStatusWidget"] sengaja DIHAPUS */
/* agar tombol "Manage app" di HP Anda tetap muncul normal. */

    /* Import Font Premium */
    @import url('https://googleapis.com');
    * { font-family: 'Plus Jakarta Sans', sans-serif; }
    
    /* ------------------------------------------------------------- */
    /* MEMAKSA SEMUA TEKS BERWARNA PUTIH TERANG (KONTRAS TINGGI)     */
    /* PERBAIKAN: Mengecualikan area ketikan agar tidak ikut putih  */
    /* ------------------------------------------------------------- */
    .stApp p, .stApp li, .stApp span, .stApp div:not([data-testid="stChatInput"]), .stApp h1, .stApp h2, .stApp h3, .stApp h4 {
        color: #ffffff !important;
    }
    
    /* ------------------------------------------------------------- */
    /* LATAR BELAKANG LAUTAN DEEP SEA                                */
    /* ------------------------------------------------------------- */
    .stApp {
        background: linear-gradient(135deg, #04080f 0%, #01243f 50%, #001417 100%) !important;
        background-attachment: fixed !important;
        overflow-x: hidden;
    }
    
    /* ------------------------------------------------------------- */
    /* NAVIGASI & SIDEBAR MINIMALIS (GLASSMORPHISM)                  */
    /* ------------------------------------------------------------- */
    [data-testid="stSidebar"] {
        background: rgba(4, 8, 15, 0.85) !important;
        backdrop-filter: blur(20px);
        border-right: 1px solid rgba(255, 255, 255, 0.05);
        z-index: 3;
    }
    
    /* AREA KOTAK PESAN PERCAKAPAN & TEKS DI DALAMNYA */
    .stChatMessage {
        background: rgba(255, 255, 255, 0.05) !important;
        backdrop-filter: blur(12px);
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 12px !important;
        margin-bottom: 12px !important;
    }
    
    /* Memastikan teks respon AI di dalam chat tetap putih tajam */
    [data-testid="stChatMessageContent"] {
        color: #ffffff !important;
    }
    
    /* ------------------------------------------------------------- */
    /* KOTAK INPUT UTAMA MELAYANG & WARNA HURUF SAAT MENGETIK CHAT   */
    /* ------------------------------------------------------------- */
    [data-testid="stChatInput"] {
        border-radius: 12px !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
        background-color: #ffffff !important;
        backdrop-filter: blur(10px);
    }
    
    [data-testid="stChatInput"] textarea {
        color: #0f172a !important; 
        font-weight: 500 !important;
    }
    
    /* Desain Ramping Scrollbar */
    ::-webkit-scrollbar { width: 6px; }
    ::-webkit-scrollbar-track { background: transparent; }
    ::-webkit-scrollbar-thumb { background: rgba(3, 169, 244, 0.2); border-radius: 10px; }
</style>
""", unsafe_allow_html=True)

# 2. Desain Tampilan Depan / Header Utama
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
    <h1 style="color: #03a9f4 !important; margin: 0; font-size: 36px; font-weight: bold; letter-spacing: 0.5px; display: inline-block;">SeHe.AI</h1>
    <span style="font-size: 11px; color: rgba(255, 255, 255, 0.5) !important; font-style: italic; position: absolute; bottom: -8px; right: 2px; white-space: nowrap;">by rikoba</span>
</div>
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

# --- Menyimpan Client di session_state agar koneksi tidak terputus ---
if "gemini_client" not in st.session_state:
    st.session_state.gemini_client = genai.Client(api_key=GEMINI_API_KEY)

# 4. Konfigurasi Karakter (Optimasi Kode Nomor 5 - Format Tabel Administrasi Formal)
ai_config = types.GenerateContentConfig(
    system_instruction=(
        "Anda adalah SeHe.AI, asisten super cerdas dengan kemampuan ganda di bidang perikanan pesisir "
        "dan administrasi pendidikan/sekolah. "
        "PENTING 1: Jika pengguna menanyakan cuaca, tinggi gelombang, atau data terkini, WAJIB gunakan alat Google Search. "
        "PENTING 2: Jika pengguna meminta tabel, laporan, kurikulum, surat, atau draf administrasi kelas/sekolah, "
        "Anda WAJIB menampilkannya dalam format tabel/elemen HTML murni dengan inline CSS yang sangat rapi (TANPA menggunakan tag markdown ```html). "
        "Gunakan standar desain dokumen formal dengan aturan CSS berikut: "
        "- Seluruh font tabel harus berwarna putih atau abu-abu terang kontras (color: #ffffff !important;). "
        "- Gunakan border tipis transparan elegan (border: 1px solid rgba(255,255,255,0.15);). "
        "- Gunakan padding yang lega agar teks tidak mepet (padding: 10px 12px;). "
        "- Kepala tabel (th) wajib diberi warna latar belakang yang tegas (background-color: #014d7c; text-align: left;). "
        "- Sediakan efek baris selang-seling atau zebra striping pada baris tabel (tr:nth-child(even) { background-color: rgba(255,255,255,0.03); }) agar dokumen mudah dianalisis dan dibaca."
    ),
    temperature=0.7, 
    tools=[{"google_search": {}}]
)

# 5. Inisialisasi Memori Obrolan (Chat Session) menggunakan model Flash yang stabil
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
        
        # --- FITUR DOWNLOAD: Menambahkan tombol download untuk setiap jawaban riwayat AI ---
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
            st.markdown(ai_response, unsafe_allow_html=True)
            
            # --- FITUR DOWNLOAD: Menambahkan tombol download untuk jawaban AI yang baru ---
            new_idx = len(st.session_state.messages)
            st.download_button(
                label="⬇️ Download sebagai HTML",
                data=ai_response,
                file_name=f"Dokumen_SeHe_AI_{new_idx}.html",
                mime="text/html",
                key=f"dl_btn_{new_idx}"
            )
            

            
        st.session_state.messages.append({"role": "assistant", "content": ai_response})

    except Exception as e:
        st.error(f"Terjadi kesalahan: {e}. Pastikan internet Anda aktif.")
