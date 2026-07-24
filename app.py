import streamlit as st
from google import genai
from google.genai import types
import os

# 1. Konfigurasi Tampilan Tab Browser dengan nama SeHe.AI
st.set_page_config(page_title="SeHe.AI - Asisten Cerdas Nelayan", page_icon="🐟", layout="centered")

# Custom CSS Premium, Ringan, Minimalis & Kontras Tinggi (Anti Tulisan Samar)
st.markdown("""
<style>
    /* ELEMEN MINIMALIS: MENYEMBUNYIKAN HEADER, GITHUB, & DEKORASI */
    header {visibility: hidden !important; height: 0px !important;}
    footer {visibility: hidden !important;}
    .viewerBadge_link__1S137 {display: none !important;}
    [data-testid="stDecoration"] {display: none !important;}
    
    /* MENYEMBUNYIKAN KEDUA IKON MERAH DI HP ORANG LAIN */
    [data-testid="stViewerBadge"], .viewerBadge_container__1S137, a[href*="streamlit.io"] {
        display: none !important; visibility: hidden !important; opacity: 0 !important; height: 0px !important; width: 0px !important;
    }
    [data-testid="stConnectionStatus"], .stConnectionStatus, div[class*="stConnectionStatus"] {
        display: none !important; visibility: hidden !important; opacity: 0 !important; height: 0px !important;
    }
    
    .block-container {
        padding-top: 2rem !important; padding-bottom: 2rem !important; max-width: 1000px !important; position: relative; z-index: 2;
    }
    
    /* Import Font Premium */
    @import url('https://googleapis.com');
    * { font-family: 'Plus Jakarta Sans', sans-serif; }
    
    .stApp p, .stApp li, .stApp span, .stApp div:not([data-testid="stChatInput"]), .stApp h1, .stApp h2, .stApp h3, .stApp h4 {
        color: #ffffff !important;
    }
    .stApp {
        background: linear-gradient(135deg, #04080f 0%, #01243f 50%, #001417 100%) !important; background-attachment: fixed !important; overflow-x: hidden;
    }
    [data-testid="stSidebar"] {
        background: rgba(4, 8, 15, 0.85) !important; backdrop-filter: blur(20px); border-right: 1px solid rgba(255, 255, 255, 0.05); z-index: 3;
    }
    .stChatMessage {
        background: rgba(255, 255, 255, 0.05) !important; backdrop-filter: blur(12px); border: 1px solid rgba(255, 255, 255, 0.1) !important; border-radius: 12px !important; margin-bottom: 12px !important;
    }
    [data-testid="stChatMessageContent"] { color: #ffffff !important; }
    
    [data-testid="stChatInput"] {
        border-radius: 12px !important; border: 1px solid rgba(255, 255, 255, 0.2) !important; background-color: #ffffff !important; backdrop-filter: blur(10px);
    }
    [data-testid="stChatInput"] textarea { color: #0f172a !important; font-weight: 500 !important; }
    ::-webkit-scrollbar { width: 6px; }
    ::-webkit-scrollbar-track { background: transparent; }
    ::-webkit-scrollbar-thumb { background: rgba(3, 169, 244, 0.2); border-radius: 10px; }
</style>
""", unsafe_allow_html=True)

# JAVASCRIPT INJEKTOR: PEMUSNAH LOGO MERAH UNTUK USER UMUM
st.components.v1.html("""
<script>
    function hapusElemenMerah() {
        const appToolbar = window.parent.document.querySelector('div[data-testid="stStatusWidget"]');
        if (appToolbar) {
            const statusKoneksi = appToolbar.querySelector('div[data-testid="stConnectionStatus"]');
            if (statusKoneksi) statusKoneksi.style.setProperty('display', 'none', 'important');
            const mahkotaMerah = appToolbar.querySelector('div[data-testid="stViewerBadge"]');
            if (mahkotaMerah) mahkotaMerah.style.setProperty('display', 'none', 'important');
        }
    }
    setInterval(hapusElemenMerah, 500);
</script>
""", height=0, width=0)

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
# Tombol Reset diletakkan di halaman utama agar terhindar dari pemblokiran CSS Sidebar
col_reset1, col_reset2, col_reset3 = st.columns([1, 2, 1])
with col_reset2:
    if st.button("🗑️ Bersihkan Riwayat & Mulai Chat Baru", use_container_width=True):
        st.session_state.messages = []
        st.clear_cache()
        st.rerun()
st.divider()

# 3. Membaca Beberapa Kunci API Secara Aman (Sistem Cadangan)
api_keys = []
if "GEMINI_API_KEY_1" in st.secrets and st.secrets["GEMINI_API_KEY_1"]:
    api_keys.append(st.secrets["GEMINI_API_KEY_1"])
if "GEMINI_API_KEY_2" in st.secrets and st.secrets["GEMINI_API_KEY_2"]:
    api_keys.append(st.secrets["GEMINI_API_KEY_2"])
if "GEMINI_API_KEY_3" in st.secrets and st.secrets["GEMINI_API_KEY_3"]:
    api_keys.append(st.secrets["GEMINI_API_KEY_3"]) # Jalur cadangan ketiga aktif!

# Jika memakai format lama (antisipasi fallback)
if not api_keys and "GEMINI_API_KEY" in st.secrets:
    api_keys.append(st.secrets["GEMINI_API_KEY"])

if not api_keys:
    st.error("API Key Gemini belum diatur di menu Secrets!")
    st.stop()

# 4. Konfigurasi Sistem Instruksi Tabel Formal (VERSI GRATIS TANPA SEARCH)
ai_config = types.GenerateContentConfig(
    system_instruction=(
        "Anda adalah SeHe.AI, asisten super cerdas dengan kemampuan ganda di bidang perikanan pesisir "
        "dan administrasi pendidikan/sekolah. "
        "Jika pengguna meminta tabel, laporan, kurikulum, surat, atau draf administrasi kelas/sekolah, "
        "Anda WAJIB menampilkannya dalam format tabel/elemen HTML murni dengan inline CSS yang sangat rapi (TANPA menggunakan tag markdown ```html). "
        "Gunakan standar desain dokumen formal dengan aturan CSS berikut: "
        "- Seluruh font tabel harus berwarna putih atau abu-abu terang kontras (color: #ffffff !important;). "
        "- Gunakan border tipis transparan elegan (border: 1px solid rgba(255,255,255,0.15);). "
        "- Gunakan padding yang lega agar teks tidak mepet (padding: 10px 12px;). "
        "- Kepala tabel (th) wajib diberi warna latar belakang yang tegas (background-color: #014d7c; text-align: left;). "
        "- Sediakan efek baris selang-seling atau zebra striping pada baris tabel (tr:nth-child(even) { background-color: rgba(255,255,255,0.03); }) agar dokumen mudah dianalisis dan dibaca."
    ),
    temperature=0.7,
    # Baris 'tools' di bawah ini sengaja DIHAPUS/DIMATIKAN agar aplikasi tetap GRATIS selamanya
    tools=[]
)


# 6. Wadah untuk menyimpan riwayat percakapan khusus untuk tampilan layar
if "messages" not in st.session_state:
    st.session_state.messages = []

# 7. Menampilkan riwayat chat di layar web
for i, message in enumerate(st.session_state.messages):
    avatar_icon = "🐟" if message["role"] == "assistant" else "👤"
    with st.chat_message(message["role"], avatar=avatar_icon):
        st.markdown(message["content"], unsafe_allow_html=True)
        
        if message["role"] == "assistant":
            st.download_button(
                label="⬇️ Download sebagai HTML",
                data=message["content"],
                file_name=f"Dokumen_SeHe_AI_{i}.html",
                mime="text/html",
                key=f"dl_btn_{i}"
            )
# Tambahkan Tombol Reset di Sidebar untuk membersihkan memori obrolan yang tersumbat
with st.sidebar:
    st.write("---")
    if st.button("🔄 Reset Obrolan Baru", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

# 8. Kolom input chat di bagian bawah layar (Sistem Proteksi Ganda & Auto-Switch yang Stabil)
if prompt := st.chat_input("Tanya sesuatu ke SeHe.AI..."):
    st.chat_message("user", avatar="👤").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    ai_response = None
    last_error_msg = ""
    
    # Perulangan otomatis mencoba setiap API Key yang terdaftar secara tangguh
    for idx, current_key in enumerate(api_keys):
        try:
            with st.spinner(f"SeHe.AI sedang mengarungi lautan data (Jalur Kunci {idx+1}/{len(api_keys)})..."):
                temp_client = genai.Client(api_key=current_key)
                response = temp_client.models.generate_content(
                    model='gemini-2.0-flash',
                    contents=prompt,
                    config=ai_config
                )
                
                if response and hasattr(response, 'text'):
                    ai_response = response.text
                    break  # Berhasil mendapatkan jawaban, keluar dari perulangan kunci
        except Exception as e:
            last_error_msg = str(e)
            # Jika ini bukan kunci terakhir, abaikan error dan langsung coba kunci berikutnya
            if idx < len(api_keys) - 1:
                continue
            else:
                # Jika SEMUA kunci sudah dicoba dan gagal, baru tampilkan pesan peringatan
                ai_response = "⚠️ Trafik server sedang sangat padat di seluruh jalur kunci gratis Anda. Mohon tunggu 30 detik sebelum mengirim pesan berikutnya."

    # Tampilkan jawaban akhir di layar web dengan avatar ikan
    if ai_response is not None:
        with st.chat_message("assistant", avatar="🐟"):
            st.markdown(ai_response, unsafe_allow_html=True)
            
            new_idx = len(st.session_state.messages)
            st.download_button(
                label="⬇️ Download sebagai HTML",
                data=ai_response,
                file_name=f"Dokumen_SeHe_AI_{new_idx}.html",
                mime="text/html",
                key=f"dl_btn_{new_idx}"
            )
            
        st.session_state.messages.append({"role": "assistant", "content": ai_response})
    else:
        st.error(f"Gagal mendapatkan respons dari server Google AI Studio. Detail error terakhir: {last_error_msg}")
