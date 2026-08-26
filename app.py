Import streamlit as st
from google import genai
from google.genai import types
import os
from docx import Document
import io
import base64

# =====================================================================
# 1. KONFIGURASI TAMPILAN TAB BROWSER & CUSTOM CSS PREMIUM (ANTI SAMAR)
# =====================================================================
st.set_page_config(page_title="SeHe.AI - Asisten Cerdas Nelayan", page_icon="🐟", layout="centered")

st.markdown("""
<style>
    /* ELEMEN MINIMALIS: MENYEMBUNYIKAN HEADER, GITHUB, & DEKORASI */
    header {visibility: hidden !important; height: 0px !important;}
    footer {visibility: hidden !important;}
    .viewerBadge_link__1S137 {display: none !important;}
    [data-testid="stDecoration"] {display: none !important;}
    
    /* MENYEMBUNYIKAN IKON BAWAAN STREAMLIT DI HP */
    [data-testid="stViewerBadge"], .viewerBadge_container__1S137, a[href*="streamlit.io"] {
        display: none !important; visibility: hidden !important; opacity: 0 !important; height: 0px !important; width: 0px !important;
    }
    [data-testid="stConnectionStatus"], .stConnectionStatus, div[class*="stConnectionStatus"] {
        display: none !important; visibility: hidden !important; opacity: 0 !important; height: 0px !important;
    }
    
    .block-container {
        padding-top: 2.5rem !important; padding-bottom: 2.5rem !important; max-width: 1000px !important; position: relative; z-index: 2;
    }
    
    /* Import Font Premium */
    @import url('https://googleapis.com');
    
    /* PERBAIKAN FONT GLOBAL: Mengecualikan ikon bawaan Streamlit agar tidak merusak & menindih teks */
    *:not(ul):not(li):not(html):not(style):not(script):not(svg):not(path):not(g):not(i):not([class*="icon"]):not([class*="icon"] *) { 
        font-family: 'Plus Jakarta Sans', sans-serif !important; 
    }
    
    /* Latar Belakang Gradasi Laut Dalam */
    .stApp {
        background: linear-gradient(135deg, #020617 0%, #071e3d 50%, #032d56 100%) !important; 
        background-attachment: fixed !important; 
        overflow-x: hidden;
    }
    
    /* Memaksa Semua Teks Berwarna Putih Terang */
    .stApp p, .stApp li, .stApp span:not(.btn-action), .stApp h1, .stApp h2, .stApp h3, .stApp h4 {
        color: #ffffff !important;
    }
    
    /* Sidebar Semi-Transparan */
    [data-testid="stSidebar"] {
        background: rgba(2, 6, 23, 0.85) !important; 
        backdrop-filter: blur(20px) !important; 
        border-right: 1px solid rgba(255, 255, 255, 0.08) !important; 
        z-index: 3;
    }
    
    /* GELEMBUNG CHAT GLASSMORPHISM MEWAH */
    .stChatMessage, [data-testid="stChatMessage"] {
        background: rgba(255, 255, 255, 0.04) !important; 
        backdrop-filter: blur(16px) !important;
        -webkit-backdrop-filter: blur(16px) !important;
        border: 1px solid rgba(255, 255, 255, 0.08) !important;
        border-radius: 16px !important;
        margin-bottom: 16px !important;
        padding: 20px !important;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.3) !important;
        transition: all 0.3s ease;
    }
    .stChatMessage:hover {
        border-color: rgba(3, 169, 244, 0.3) !important;
        box-shadow: 0 8px 32px 0 rgba(3, 169, 244, 0.1) !important;
    }
    [data-testid="stChatMessageContent"] { color: #ffffff !important; font-size: 15px !important; line-height: 1.6 !important; }
    [data-testid="stChatMessageContent"] div, [data-testid="stChatMessageContent"] span { background-color: transparent !important; }
    
    /* WADAH INPUT CHAT ELEGAN */
    [data-testid="stChatInput"] {
        border-radius: 16px !important; 
        border: 1px solid rgba(255, 255, 255, 0.15) !important; 
        background: rgba(255, 255, 255, 0.06) !important; 
        backdrop-filter: blur(20px) !important;
        -webkit-backdrop-filter: blur(20px) !important;
        box-shadow: 0 4px 24px 0 rgba(0, 0, 0, 0.2) !important;
        padding: 4px !important;
    }
    /* PERBAIKAN TOTAL: Memaksa teks ketikan kita agar berwarna gelap terang di dalam kotak input */
    [data-testid="stChatInput"] textarea { 
        color: #0f172a !important; /* Warna gelap arang pekat agar tulisan kontras dan jelas */
        font-weight: 500 !important; 
        background: #ffffff !important; /* Memaksa latar belakang tempat mengetik tetap putih bersih */
    }

    
    /* 1. KOTAK LUAR UNGGAH FILE (TRANSISI LUAR) */
    [data-testid="stFileUploader"] {
        background: transparent !important;
        border: none !important;
        padding: 0px !important;
        margin-bottom: 25px !important;
    }
    
    /* 2. KOTAK DALAM DI DALAM GARIS PUTUS-PUTUS (PERBAIKAN TOTAL ANTI PUTIH NEON) */
    [data-testid="stFileUploaderDropzone"], [data-testid="stFileUploader"] section {
        /* Mengubah latar kotak dalam dari putih neon menjadi biru laut sangat gelap */
        background: rgba(2, 14, 30, 0.75) !important;
        backdrop-filter: blur(12px) !important;
        -webkit-backdrop-filter: blur(12px) !important;
        /* Mewarnai ulang garis putus-putus pembatas kotak */
        border: 2px dashed rgba(3, 169, 244, 0.25) !important;
        border-radius: 20px !important;
        padding: 24px !important;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1) !important;
        box-shadow: inset 0 0 20px rgba(0, 0, 0, 0.6) !important;
    }
    
    /* Efek menyala redup yang mewah saat kursor menyentuh kotak dalam */
    [data-testid="stFileUploaderDropzone"]:hover, [data-testid="stFileUploader"] section:hover {
        border-color: rgba(3, 169, 244, 0.6) !important;
        background: rgba(3, 169, 244, 0.05) !important;
        box-shadow: 0 0 25px rgba(3, 169, 244, 0.15), inset 0 0 15px rgba(0, 0, 0, 0.4) !important;
    }
    
    /* Menyembunyikan total teks batas info ukuran bawaan Streamlit (200MB per file) */
    [data-testid="stFileUploaderRequirements"], 
    [data-testid="stFileUploader"] small,
    [data-testid="stFileUploader"] section + div {
        display: none !important;
        visibility: hidden !important;
        opacity: 0 !important;
        height: 0px !important;
        font-size: 0px !important;
        line-height: 0 !important;
        padding: 0 !important;
        margin: 0 !important;
    }


 /* Menyembunyikan teks info ukuran file bawaan Streamlit (200MB per file) */
    [data-testid="stFileUploaderRequirements"] {
        display: none !important;
        visibility: hidden !important;
        height: 0px !important;
    }

    
    /* Memisahkan tombol "Browse files" ke baris bawah agar tidak menumpuk */
    [data-testid="stFileUploader"] button {
        margin-top: 4px !important;
    }

       
    /* TOMBOL CETAK & SIMPAN GRADASI BERKILAU */
    .action-buttons-container { display: flex; gap: 16px; margin-top: 20px; margin-bottom: 12px; }
    .btn-action {
        padding: 14px 28px; border-radius: 14px; font-size: 14px; font-weight: 600;
        text-decoration: none; border: none; cursor: pointer;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        display: inline-flex; align-items: center; justify-content: center; gap: 10px;
    }
    .btn-blue {
        background: linear-gradient(135deg, #0288d1 0%, #005691 100%) !important; color: #ffffff !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important; box-shadow: 0 4px 20px rgba(2, 136, 209, 0.25) !important;
    }
    .btn-blue:hover { 
        background: linear-gradient(135deg, #039be5 0%, #0288d1 100%) !important;
        transform: translateY(-3px); box-shadow: 0 8px 25px rgba(3, 155, 229, 0.45) !important;
    }
    .btn-green {
        background: linear-gradient(135deg, #2e7d32 0%, #1b5e20 100%) !important; color: #ffffff !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important; box-shadow: 0 4px 20px rgba(46, 125, 50, 0.25) !important;
    }
    .btn-green:hover { 
        background: linear-gradient(135deg, #388e3c 0%, #2e7d32 100%) !important;
        transform: translateY(-3px); box-shadow: 0 8px 25px rgba(56, 142, 60, 0.45) !important;
    }
    
    /* MODIFIKASI TOMBOL REKOMENDASI PINTASAN STREAMLIT (BAGIAN #8) */
    div[data-testid="stColumn"] button {
        background: rgba(255, 255, 255, 0.05) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        color: #ffffff !important;
        border-radius: 14px !important;
        padding: 14px 20px !important;
        font-weight: 500 !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1) !important;
    }
    div[data-testid="stColumn"] button:hover {
        background: linear-gradient(135deg, #0288d1 0%, #005691 100%) !important;
        border-color: #03a9f4 !important;
        box-shadow: 0 6px 20px rgba(3, 169, 244, 0.35) !important;
        transform: translateY(-3px) !important;
    }
    div[data-testid="stColumn"] button:active {
        transform: translateY(-1px) !important;
    }

    /* Scrollbar Halus Khas Aplikasi Web Premium */
    ::-webkit-scrollbar { width: 8px; }
    ::-webkit-scrollbar-track { background: transparent; }
    ::-webkit-scrollbar-thumb { background: rgba(3, 169, 244, 0.25); border-radius: 10px; }
    ::-webkit-scrollbar-thumb:hover { background: rgba(3, 169, 244, 0.45); }
</style>

""", unsafe_allow_html=True)

st.components.v1.html("""
<script>
    function hancurkanLogoMerah() {
        const rootDOM = window.parent.document;
        if (rootDOM) {
            const badges = rootDOM.querySelectorAll('a[href*="streamlit.io"], [data-testid="stViewerBadge"], [class*="viewerBadge"]');
            badges.forEach(el => {
                el.style.setProperty('display', 'none', 'important');
                el.style.setProperty('visibility', 'hidden', 'important');
            });
            const statusKoneksi = rootDOM.querySelectorAll('[data-testid="stConnectionStatus"], [class*="stConnectionStatus"]');
            statusKoneksi.forEach(el => {
                el.style.setProperty('display', 'none', 'important');
                el.style.setProperty('visibility', 'hidden', 'important');
            });
            const statusWidget = rootDOM.querySelector('div[data-testid="stStatusWidget"]');
            if (statusWidget) {
                const childElements = statusWidget.children;
                for (let child of childElements) {
                    if (!child.innerText || !child.innerText.includes("Manage app")) {
                        if (child.querySelector('a') || child.querySelector('svg')) {
                            child.style.setProperty('display', 'none', 'important');
                        }
                    }
                }
            }
        }
    }
    setInterval(hancurkanLogoMerah, 300);
</script>
""", height=0, width=0)

# =====================================================================
# 2. DESAIN TAMPILAN DEPAN / HEADER UTAMA & BUTTON RESET MEMORI
# =====================================================================
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
    <span style="font-size: 11px; color: rgba(255, 255, 255, 0.4) !important; font-style: italic; position: absolute; bottom: -8px; right: 2px; white-space: nowrap;">by rikoba</span>
</div>
</div>
""")

col_reset1, col_reset2, col_reset3 = st.columns([1, 2, 1])
with col_reset2:
    if st.button("🗑️ Bersihkan Riwayat & Mulai Chat Baru", use_container_width=True):
        st.session_state.messages = []
        st.cache_data.clear()
        st.rerun()

st.sidebar.write("---")
with st.sidebar:
    if st.button("🔄 Reset Obrolan Baru", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

# =====================================================================
# 3. MEMBACA TIGA KUNCI API SECARA AMAN (SISTEM CADANGAN OTOMATIS)
# =====================================================================
api_keys = []
if "GEMINI_API_KEY_1" in st.secrets and st.secrets["GEMINI_API_KEY_1"]:
    api_keys.append(st.secrets["GEMINI_API_KEY_1"])
if "GEMINI_API_KEY_2" in st.secrets and st.secrets["GEMINI_API_KEY_2"]:
    api_keys.append(st.secrets["GEMINI_API_KEY_2"])
if "GEMINI_API_KEY_3" in st.secrets and st.secrets["GEMINI_API_KEY_3"]:
    api_keys.append(st.secrets["GEMINI_API_KEY_3"])


if not api_keys and "GEMINI_API_KEY" in st.secrets:
    api_keys.append(st.secrets["GEMINI_API_KEY"])

if not api_keys:
    st.error("API Key Gemini belum diatur di menu Secrets!")
    st.stop()

# =====================================================================
# 4. KONFIGURASI SISTEM INSTRUKSI (DOKUMEN MEWAH, ELEGAN, WARNA OTOMATIS)
# =====================================================================
ai_config = types.GenerateContentConfig(
    system_instruction=(
        "Anda adalah SeHe.AI, asisten super cerdas berkemampuan tinggi di bidang perikanan pesisir "
        "dan administrasi pendidikan/sekolah. "
        "TUGAS UTAMA: Anda wajib mematuhi dan memasukkan SETIAP poin data yang diminta pengguna atau yang termuat dalam file rujukan secara utuh tanpa ada yang dikurangi/disingkat. "
        "PENTING 1: Jika pengguna menanyakan cuaca, tinggi gelombang, data pasang surut, fase bulan, atau data terkini, WAJIB gunakan alat Google Search. "
        "PENTING 2: Jika pengguna meminta tabel, laporan, kurikulum, proposal, RPP, atau draf administrasi, "
        "Anda WAJIB menampilkannya secara UTUH, PANJANG, DAN DETAIL dalam bentuk dokumen HTML murni dengan inline CSS yang elegan (TANPA tag markdown ```html). "
        "IKUTI ATURAN WAJIB DESAIN DOKUMEN MEWAH & PROFESIONAL BERIKUT: "
        "- STRUKTUR KOP DOKUMEN FORMAL: Setiap dokumen draf/laporan wajib diawali dengan Kop Dokumen resmi di bagian paling atas: "
        "  Teks tebal nama instansi di tengah (font-size: 18px; text-align: center;), diikuti alamat sub-teks kecil, "
        "  dan ditutup dengan garis pembatas hitam tebal horizontal ganda (<hr style='border: 0; border-top: 4px double #1e293b; margin: 15px 0;'>). "
        "- TAMPILAN MONOKROMATIK PREMIUM & MINIMALIS KONTEMPORER: DILARANG KERAS MENGGUNAKAN GAYA ZEBRA STRIPING ATAU BARIS SELANG-SELING. Latar belakang baris data harus bersih polos transparan/putih. "
        "- WARNA TEMA UTOMATIS: Gunakan warna solid mewah Deep Oceanic Blue #014d7c untuk kelautan/perikanan/cuaca, Emerald Green #0d5c3a untuk pendidikan/sekolah, atau Charcoal Gray #2d3748 untuk keuangan/anggaran biaya. "
        "- Gunakan warna tema pilihan tersebut untuk latar belakang Kepala Tabel (th) dengan teks putih tebal (color: #ffffff !important; font-weight: 600; padding: 12px 14px; text-align: left;). "
        "- Desain Garis Pembatas Sleek: Hilangkan seluruh garis vertikal kaku pada tabel. Hanya gunakan garis horizontal bawah yang tipis gelap transparan di setiap baris data (border-bottom: 1px solid #e2e8f0;). "
        "- Padding Sel Harus Lega (padding: 12px 14px;) agar teks seimbang, mewah, memiliki ruang napas tinggi, dan mudah dianalisis. "
        "- KONTRAST TEKS DOKUMEN: Seluruh huruf isi konten, paragraf, dan isi data tabel wajib menggunakan warna gelap arang profesional (color: #1e293b !important;) agar terbaca sempurna di kertas putih saat dibuka di Word atau PDF, dengan pengecualian teks di dalam Kepala Tabel (th) yang tetap putih."
    ),
    temperature=0.3,
    tools=[{"google_search": {}}]
)


# =====================================================================
# 5. SINKRONISASI OTOMATIS FOLDER GOOGLE DRIVE KHUSUS SEHE.AI
# =====================================================================
def baca_data_bantuan_drive(prompt_user):
    referensi_drive = ""
    try:
        from googleapiclient.discovery import build
        from google.oauth2.service_account import Credentials
        info_kunci = dict(st.secrets["gcp_service_account"])
        kredensial = Credentials.from_service_account_info(info_kunci)
        layanan = build('drive', 'v3', credentials=kredensial)
        id_folder = st.secrets["DRIVE_FOLDER_ID"]
        query = f"'{id_folder}' in parents and mimeType = 'text/plain' and trashed = false"
        hasil = layanan.files().list(q=query, fields="files(id, name)").execute()
        berkas_list = hasil.get('files', [])
        for berkas in berkas_list:
            id_berkas = berkas['id']
            konten = layanan.files().get_media(fileId=id_berkas).execute()
            teks_berkas = konten.decode('utf-8')
            for baris in teks_berkas.splitlines():
                if "|" in baris and not baris.strip().startswith("#"):
                    kata_kunci, isi_informasi = baris.strip().split("|", 1)
                    if kata_kunci.lower().strip() in prompt_user.lower():
                        referensi_drive += f"\n[REFERENSI DRIVE - {berkas['name']}]: {isi_informasi.strip()}\n"
    except Exception as e:
        pass
    return referensi_drive

# =====================================================================
# 6. WADAH UNTUK MENYIMPAN RIWAYAT PERCAKAPAN KHUSUS TAMPILAN LAYAR
# =====================================================================
if "messages" not in st.session_state:
    st.session_state.messages = []


# =====================================================================
# 7. MENAMPILKAN RIWAYAT CHAT DI LAYAR WEB (PERBAIKAN TOTAL BEBAS ERROR)
# =====================================================================
for i, message in enumerate(st.session_state.messages):
    avatar_icon = "🐟" if message["role"] == "assistant" else "👤"
    with st.chat_message(message["role"], avatar=avatar_icon):
        st.markdown(message["content"], unsafe_allow_html=True)
        
        # PENGGABUNGAN BLOK LOGIKA ASISTEN: Mencegah NameError & Sinkronisasi Tombol Unduh
        if message["role"] == "assistant":
            # CSS TERPADU: Disamakan persis dengan gaya dokumen HTML & Word Premium
            css_word_hist = (
                "@page { size: 21cm 29.7cm; margin: 2.54cm 2.54cm 2.54cm 2.54cm; mso-page-orientation: portrait; } "
                "body { font-family: 'Segoe UI', Arial, sans-serif; padding: 0px; line-height: 140%; background-color: #ffffff; color: #1e293b; } "
                "table { border-collapse: collapse; width: 100%; margin: 20px 0; mso-table-lspace: 0pt; mso-table-rspace: 0pt; background-color: #ffffff; margin-top: 0px; } "
                "th { background-color: #014d7c; color: #ffffff !important; font-weight: bold; padding: 12px 14px; border-bottom: 2px solid #003353; text-align: left; line-height: 140%; mso-line-height-rule: at-least; } "
                "td { color: #1e293b; padding: 12px 14px; border-bottom: 1px solid #e2e8f0; background-color: #ffffff; line-height: 140%; mso-line-height-rule: at-least; } "
                "th, td { border-left: none !important; border-right: none !important; } "
            )
            
            html_wrapped_hist = (
                "<html xmlns:o='urn:schemas-microsoft-com:office:office' xmlns:w='urn:schemas-microsoft-com:office:word' xmlns='http://w3.org'>"
                "<head><meta charset='utf-8'><title>Dokumen SeHe AI</title>"
                "<!--[if gte mso 9]><xml><w:WordDocument><w:View>Print</w:View><w:Zoom>100</w:Zoom><w:DoNotOptimizeForBrowser/></w:WordDocument></xml><![endif]-->"
                "<style>" + css_word_hist + "</style>"
                "</head>"
                "<body>DOKUMEN_SEHE_AI_CONTENT</body>"
                "</html>"
            )
            
            # STERILISASI SEHE.AI: Mengunci pemotongan langsung pada awal tag tabel utama
            konten_bersih_hist = message["content"].strip()
            
            # Deteksi posisi tabel utama untuk memotong tag kosong buatan AI di atasnya
            posisi_tabel_hist = konten_bersih_hist.find("<table")
            if posisi_tabel_hist != -1:
                konten_bersih_hist = konten_bersih_hist[posisi_tabel_hist:]
            
            # Hapus paksa jika ada tag kaku markdown yang merusak visual HTML
            konten_bersih_hist = konten_bersih_hist.replace("```html", "").replace("```", "").strip()
            
            # Terapkan gaya desain terpadu konsisten
            konten_bersih_hist = konten_bersih_hist.replace("<table", '<table style="margin-top: 0px; border-collapse: collapse; width: 100%; background-color: #ffffff;"')
            konten_bersih_hist = konten_bersih_hist.replace("<th", '<th bgcolor="#014d7c" style="background-color: #014d7c; color: #ffffff; font-weight: bold; padding: 12px 14px; text-align: left;"').replace("<th>", '<th bgcolor="#014d7c" style="background-color: #014d7c; color: #ffffff; font-weight: bold; padding: 12px 14px; text-align: left;">')
            konten_bersih_hist = konten_bersih_hist.replace("<td", '<td style="color: #1e293b; padding: 12px 14px; border-bottom: 1px solid #e2e8f0; background-color: #ffffff;"')

            html_wrapped_hist = html_wrapped_hist.replace("DOKUMEN_SEHE_AI_CONTENT", konten_bersih_hist)
            b64_html_hist = base64.b64encode(html_wrapped_hist.encode('utf-8')).decode('utf-8')
            
            html_tombol = """
            <div class="action-buttons-container">
                <a class="btn-action btn-blue" href="data:application/msword;base64,B64_DATA_DOKUMEN" download="Dokumen_SeHe_AI_INDEX.doc">
                    📝 Simpan .WORD
                </a>
                <a class="btn-action btn-green" href="data:text/html;base64,B64_DATA_DOKUMEN" download="Dokumen_SeHe_AI_INDEX.html">
                    💾 Simpan .HTML
                </a>
            </div>
            """
            html_tombol = html_tombol.replace("B64_DATA_DOKUMEN", b64_html_hist).replace("INDEX", str(i))
            st.markdown(html_tombol, unsafe_allow_html=True)

# =====================================================================
# 8. AREA FITUR BARU: PERINTAH CEPAT (3 NAVIGASI MARITIM MEWAH BENING)
# =====================================================================
st.write("### 🎯 Rekomendasi Pintasan Cepat")
cp1, cp2, cp3 = st.columns(3)

if "prompt_pilihan" not in st.session_state:
    st.session_state.prompt_pilihan = None

with cp1:
    if st.button("⛅ Cek Cuaca & Gelombang", use_container_width=True):
        st.session_state.prompt_pilihan = "Bagaimana kondisi cuaca, suhu, arah angin, dan tinggi gelombang laut di wilayah pesisir hari ini? Berikan analisis kelayakan aman atau tidaknya untuk melaut."
with cp2:
    if st.button("🌊 Cek Pasang Surut Laut", use_container_width=True):
        st.session_state.prompt_pilihan = "Bagaimana data grafik perkiraan waktu pasang surut air laut di wilayah pesisir hari ini? Berikan analisis waktu aman untuk nelayan menyandarkan kapal."
with cp3:
    if st.button("🌙 Cek Fase Bulan Terkini", use_container_width=True):
        st.session_state.prompt_pilihan = "Bagaimana kondisi fase bulan hari ini secara real-time? Berikan analisis dampaknya terhadap pergerakan kuat-lemah arus air laut dan kelimpahan tangkapan ikan nelayan malam ini."

# KODE BARU: Kotak unggah file langsung terbuka lebar di layar tanpa dilipat
st.write("### 📂 Lampirkan Dokumen Basis Data Rujukan (.PDF / .DOCX)")
file_pendukung = st.file_uploader(
    "Silakan unggah dokumen rujukan sebagai acuan analisis SeHe.AI (Maks 10MB):", 
    type=["pdf", "docx"], 
    label_visibility="visible"
)
st.write("") # Memberi sedikit ruang napas di bawahnya

prompt_input = st.chat_input("Tanya sesuatu ke SeHe.AI...")
final_prompt = prompt_input if prompt_input else st.session_state.prompt_pilihan

if final_prompt:
    st.session_state.prompt_pilihan = None
    
    file_valid = True
    if file_pendukung is not None:
        ukuran_file_mb = file_pendukung.size / (1024 * 1024)
        if ukuran_file_mb > 10.0:
            file_valid = False

    if not file_valid:
        st.error("⚠️ File terlalu besar (Maksimal 10 MB) agar proses membaca cepat dan instan. Silakan kompres dokumen Anda sebelum diunggah.")
    else:
        st.chat_message("user", avatar="👤").markdown(final_prompt)
        st.session_state.messages.append({"role": "user", "content": final_prompt})

        ai_response = None
        last_error_msg = ""
        paket_konten = []
        
        if file_pendukung is not None:
            nama_file = file_pendukung.name.lower()
            if nama_file.endswith('.docx'):
                try:
                    doc = Document(io.BytesIO(file_pendukung.read()))
                    teks_word = "\n".join([paragraph.text for paragraph in doc.paragraphs])
                    paket_konten.append(f"[DOKUMEN RUJUKAN UTAMA WORD]:\n{teks_word}\n\n")
                except Exception as e:
                    st.warning(f"Gagal membaca file Word: {e}")
            elif nama_file.endswith('.pdf'):
                try:
                    pdf_data = file_pendukung.read()
                    paket_konten.append(
                        types.Part.from_bytes(
                            data=pdf_data,
                            mime_type="application/pdf"
                        )
                    )
                except Exception as e:
                    st.warning(f"Gagal memproses file PDF: {e}")

        teks_tanya = str(final_prompt)
        referensi_lokal = baca_data_bantuan_drive(teks_tanya)
        if referensi_lokal:
            paket_konten.append(f"{referensi_lokal}\n\n")
            
        paket_konten.append(teks_tanya)

        if len(st.session_state.messages) > 1:
            paket_konten = [teks_tanya]

        # PERBAIKAN LOGIKA FAILOVER API: Menjamin kunci cadangan berjalan berurutan
        for idx, current_key in enumerate(api_keys):
            sukses_merespons = False
            daftar_model = ['gemini-2.5-flash', 'gemini-2.5-pro']  # Nama model produksi stabil Google GenAI SDK
            
            for target_model in daftar_model:
                try:
                    with st.spinner(f"SeHe.AI membedah data ({target_model} | Jalur {idx+1}/{len(api_keys)})..."):
                        temp_client = genai.Client(api_key=current_key)
                        
                        riwayat_gemini = []
                        for msg in st.session_state.messages[-3:-1]:
                            riwayat_gemini.append(
                                types.Content(
                                    role="model" if msg["role"] == "assistant" else "user",
                                    parts=[types.Part.from_text(text=msg["content"])]
                                )
                            )

                        chat_session = temp_client.chats.create(
                            model=target_model,
                            config=ai_config,
                            history=riwayat_gemini
                        )
                        
                        response = chat_session.send_message(message=paket_konten)
                        if response and hasattr(response, 'text'):
                            ai_response = response.text
                            sukses_merespons = True
                            break 
                except Exception as e:
                    last_error_msg = str(e)
                    if "429" in last_error_msg or "RESOURCE_EXHAUSTED" in last_error_msg:
                        import time
                        time.sleep(2)
                        break 
                    elif "503" in last_error_msg:
                        continue  
                    else:
                        break

            if sukses_merespons:
                break 
            
            # Jika berada di ujung kunci terakhir dan seluruhnya gagal total
            if idx == len(api_keys) - 1 and not sukses_merespons:
                st.error("⚠️ Seluruh jalur kunci dan model cadangan SeHe.AI sedang padat di server Google. Silakan tunggu 10 detik lalu kirim ulang pesan Anda.")
                ai_response = None

        # T TAMPILKAN JAWABAN AKHIR DI LAYAR WEB
                # TAMPILKAN JAWABAN AKHIR DI LAYAR WEB
                # TAMPILKAN JAWABAN AKHIR DI LAYAR WEB
        if ai_response is not None:
            with st.chat_message("assistant", avatar="🐟"):
                st.markdown(ai_response, unsafe_allow_html=True)
                
            # =============================================================
            # SOLUSI TOTAL KEBAL SYNTAXERROR: ENKAPSULASI TEKS HORIZONTAL
            # =============================================================
            css_bag_1 = "@page { size: 21cm 29.7cm; margin: 2.54cm 2.54cm 2.54cm 2.54cm; mso-page-orientation: portrait; } "
            css_bag_2 = "body { font-family: 'Segoe UI', Arial, sans-serif; padding: 0px; line-height: 140%; background-color: #ffffff; color: #1e293b; } "
            css_bag_3 = "table { border-collapse: collapse; width: 100%; margin: 20px 0; mso-table-lspace: 0pt; mso-table-rspace: 0pt; background-color: #ffffff; margin-top: 0px; } "
            css_bag_4 = "th { background-color: #014d7c; color: #ffffff !important; font-weight: bold; padding: 12px 14px; border-bottom: 2px solid #003353; text-align: left; line-height: 140%; mso-line-height-rule: at-least; } "
            css_bag_5 = "td { color: #1e293b; padding: 12px 14px; border-bottom: 1px solid #e2e8f0; background-color: #ffffff; line-height: 140%; mso-line-height-rule: at-least; } "
            css_bag_6 = "th, td { border-left: none; border-right: none; } "

            css_word_style = css_bag_1 + css_bag_2 + css_bag_3 + css_bag_4 + css_bag_5 + css_bag_6
            
            html_wrapped = """<html xmlns:o='urn:schemas-microsoft-com:office:office' xmlns:w='urn:schemas-microsoft-com:office:word' xmlns='http://w3.org'><head><meta charset='utf-8'><title>Dokumen SeHe AI</title><!--[if gte mso 9]><xml><w:WordDocument><w:View>Print</w:View><w:Zoom>100</w:Zoom><w:DoNotOptimizeForBrowser/></w:WordDocument></xml><![endif]--><style>""" + css_word_style + """</style></head><body>DOKUMEN_SEHE_AI_CONTENT</body></html>"""
            
            # STERILISASI SEHE.AI: Mengunci pemotongan langsung pada awal tag tabel utama
            konten_bersih = ai_response.strip()
            
            # Deteksi posisi tabel utama untuk memotong tag kosong buatan AI di atasnya
            posisi_tabel = konten_bersih.find("<table")
            if posisi_tabel != -1:
                konten_bersih = konten_bersih[posisi_tabel:]
                
            # Hapus paksa jika ada tag kaku markdown yang merusak visual HTML
            konten_bersih = konten_bersih.replace("```html", "").replace("```", "").strip()
            
            # Terapkan gaya desain terpadu konsisten
            konten_bersih = konten_bersih.replace("<table", '<table style="margin-top: 0px; border-collapse: collapse; width: 100%; background-color: #ffffff;"')
            konten_bersih = konten_bersih.replace("<th", '<th bgcolor="#014d7c" style="background-color: #014d7c; color: #ffffff; font-weight: bold; padding: 12px 14px; text-align: left;"').replace("<th>", '<th bgcolor="#014d7c" style="background-color: #014d7c; color: #ffffff; font-weight: bold; padding: 12px 14px; text-align: left;">')
            konten_bersih = konten_bersih.replace("<td", '<td style="color: #1e293b; padding: 12px 14px; border-bottom: 1px solid #e2e8f0; background-color: #ffffff;"')

            html_wrapped = html_wrapped.replace("DOKUMEN_SEHE_AI_CONTENT", konten_bersih)
            b64_html = base64.b64encode(html_wrapped.encode('utf-8')).decode('utf-8')
            new_idx = len(st.session_state.messages)
            
            html_tombol = """
            <div class="action-buttons-container">
                <a class="btn-action btn-blue" href="data:application/msword;base64,B64_DATA_DOKUMEN" download="Dokumen_SeHe_AI_INDEX_BARU.doc">
                    📝 Simpan .WORD
                </a>
                <a class="btn-action btn-green" href="data:text/html;base64,B64_DATA_DOKUMEN" download="Dokumen_SeHe_AI_INDEX_BARU.html">
                    💾 Simpan .HTML
                </a>
            </div>
            """

            html_tombol = html_tombol.replace("B64_DATA_DOKUMEN", b64_html).replace("INDEX_BARU", str(new_idx))
            st.markdown(html_tombol, unsafe_allow_html=True)

            st.session_state.messages.append({"role": "assistant", "content": ai_response})
            st.rerun()



            
        else:
            if "429" not in last_error_msg and "RESOURCE_EXHAUSTED" not in last_error_msg:
                st.error(f"Gagal mendapatkan respons dari server Google AI Studio. Detail: {last_error_msg}")

