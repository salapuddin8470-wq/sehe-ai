import streamlit as st
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
    
    /* MENYEMBUNYIKAN KEDUA IKON MERAH DI HP ORANG LAIN (BACKUP CSS) */
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
    
    /* Memaksa Semua Teks Berwarna Putih Terang (Kecuali Input & Area Dokumen HTML) */
    .stApp p, .stApp li, .stApp span:not(.btn-action), .stApp h1, .stApp h2, .stApp h3, .stApp h4 {
        color: #ffffff !important;
    }
    .stApp {
        background: linear-gradient(135deg, #04080f 0%, #01243f 50%, #001417 100%) !important; background-attachment: fixed !important; overflow-x: hidden;
    }
    [data-testid="stSidebar"] {
        background: rgba(4, 8, 15, 0.85) !important; backdrop-filter: blur(20px); border-right: 1px solid rgba(255, 255, 255, 0.05); z-index: 3;
    }
    
    /* PENGATURAN GELEMBUNG CHAT: CEGAH LATAR PUTIH DAN KUNCI WARNA TEKS */
    .stChatMessage, [data-testid="stChatMessage"] {
        background-color: rgba(255, 255, 255, 0.05) !important; 
        backdrop-filter: blur(12px) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 12px !important;
        margin-bottom: 12px !important;
        padding: 15px !important;
    }
    [data-testid="stChatMessageContent"] { 
        color: #ffffff !important; 
    }
    [data-testid="stChatMessageContent"] div, [data-testid="stChatMessageContent"] span {
        background-color: transparent !important;
    }
    
    [data-testid="stChatInput"] {
        border-radius: 12px !important; border: 1px solid rgba(255, 255, 255, 0.2) !important; background-color: #ffffff !important; backdrop-filter: blur(10px);
    }
    [data-testid="stChatInput"] textarea { color: #0f172a !important; font-weight: 500 !important; }
    
    /* Styling Elemen Kotak Unggah File */
    [data-testid="stFileUploader"] {
        background-color: rgba(255, 255, 255, 0.02) !important;
        border: 1px dashed rgba(255, 255, 255, 0.15) !important;
        padding: 12px !important;
        border-radius: 12px !important;
        margin-bottom: 15px;
    }
    
    /* STYLING TOMBOL PINTASAN CEPAT (GLASSMORPHISM MEWAH GLOWING - ANTI PUTIH POLOS) */
    div[data-testid="stColumn"] button {
        background: rgba(3, 169, 244, 0.05) !important;
        backdrop-filter: blur(10px) !important;
        border: 1px solid rgba(3, 169, 244, 0.25) !important;
        border-radius: 12px !important;
        color: #03a9f4 !important;
        font-weight: 600 !important;
        padding: 12px 10px !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2) !important;
    }
    div[data-testid="stColumn"] button:hover {
        background: rgba(3, 169, 244, 0.15) !important;
        border: 1px solid #03a9f4 !important;
        color: #ffffff !important;
        box-shadow: 0 0 15px rgba(3, 169, 244, 0.5) !important;
        transform: translateY(-2px);
    }
    
    /* STYLING KUSTOM TOMBOL CETAK & SIMPAN AGAR MEWAH & KONTRAS (TIDAK SAMAR) */
    .action-buttons-container {
        display: flex;
        gap: 12px;
        margin-top: 15px;
        margin-bottom: 10px;
    }
    .btn-action {
        padding: 10px 20px;
        border-radius: 8px;
        font-size: 14px;
        font-weight: 600;
        text-decoration: none;
        border: none;
        cursor: pointer;
        transition: all 0.2s ease;
        display: inline-flex;
        align-items: center;
        justify-content: center;
        box-shadow: 0 4px 6px rgba(0,0,0,0.15);
    }
    .btn-action:hover {
        transform: translateY(-1px);
        box-shadow: 0 6px 8px rgba(0,0,0,0.2);
    }
    .btn-blue {
        background-color: #0288d1 !important;
        color: #ffffff !important;
    }
    .btn-blue:hover { background-color: #039be5 !important; }
    .btn-green {
        background-color: #2e7d32 !important;
        color: #ffffff !important;
    }
    .btn-green:hover { background-color: #388e3c !important; }
    
    ::-webkit-scrollbar { width: 6px; }
    ::-webkit-scrollbar-track { background: transparent; }
    ::-webkit-scrollbar-thumb { background: rgba(3, 169, 244, 0.2); border-radius: 10px; }
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
        "- TAMPILAN MONOKROMATIK PREMIUM & MINIMALIS KONTEMPORER. DILARANG KERAS MENGGUNAKAN GAYA ZEBRA STRIPING ATAU BARIS SELANG-SELING. Latar belakang baris data harus bersih polos transparan. "
        "- WARNA TEMA OTOMATIS: Pilih satu warna tema solid yang mewah berdasarkan topik dokumen (Contoh: Deep Oceanic Blue #014d7c untuk kelautan/perikanan/cuaca, Emerald Green #0d5c3a untuk pendidikan/sekolah, Charcoal Gray #2d3748 untuk keuangan/anggaran biaya). "
        "- Gunakan warna tema otomatis pilihan Anda tersebut untuk latar belakang Kepala Tabel (th) dengan teks putih tebal (color: #ffffff !important; font-weight: 600; padding: 12px 14px; text-align: left; letter-spacing: 0.5px;). "
        "- Desain Garis Pembatas Sleek: Hilangkan seluruh garis vertikal kaku. Hanya gunakan garis horizontal bawah yang tipis transparan di setiap baris data (border-bottom: 1px solid rgba(255,255,255,0.15);). "
        "- Padding Sel Harus Lega (padding: 12px 14px;) agar teks seimbang, mewah, memiliki ruang napas tinggi, dan mudah dianalisis. "
        "- Seluruh huruf dokumen wajib berwarna putih terang kontras (color: #ffffff !important;)."
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
        
        if message["role"] == "assistant":
            # Proteksi desimal menggunakan titik (.), bukan koma (,)
            css_word_hist = (
                "@page { size: 21cm 29.7cm; margin: 2.54cm 2.54cm 2.54cm 2.54cm; mso-page-orientation: portrait; } "
                "body { font-family: 'Segoe UI', Arial, sans-serif; padding: 0px; line-height: 1.6; background-color: #ffffff !important; color: #1e293b !important; } "
                "table { border-collapse: collapse; width: 100%; margin: 20px 0; mso-table-lspace: 0pt; mso-table-rspace: 0pt; } "
                "th { color: #ffffff !important; font-weight: bold; padding: 12px 14px; border-bottom: 2px solid #000000; } "
                "td { color: #334155 !important; padding: 12px 14px; border-bottom: 1px solid #e2e8f0; mso-line-height-rule: exactly; } "
                "th, td { border-left: none !important; border-right: none !important; }"
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
            
            html_wrapped_hist = html_wrapped_hist.replace("DOKUMEN_SEHE_AI_CONTENT", message["content"])
            b64_html_hist = base64.b64encode(html_wrapped_hist.encode('utf-8')).decode('utf-8')
            
            # Tampilkan Dua Tombol Berjejer Estetis Kontras Tinggi Khusus Riwayat Chat
            html_tombol_hist = """
            <div class="action-buttons-container">
                <button class="btn-action btn-blue" onclick="window.print()">
                    🖨️ Cetak / PDF
                </button>
                <a class="btn-action btn-green" href="data:text/html;base64,B64_DATA_DOKUMEN" download="Dokumen_SeHe_AI_INDEX.html">
                    💾 Simpan .HTML
                </a>
            </div>
            """
            html_tombol_hist = html_tombol_hist.replace("B64_DATA_DOKUMEN", b64_html_hist).replace("INDEX", str(i))
            st.markdown(html_tombol_hist, unsafe_allow_html=True)

# =====================================================================
# 8. AREA FITUR BARU: PERINTAH CEPAT (3 NAVIGASI MARITIM MEWAH BENING)
# =====================================================================
st.write("### 🎯 Rekomendasi Pintasan Cepat")
cp1, cp2, cp3 = st.columns(3)

# Menggunakan session_state agar nilai tidak hilang saat halaman rerun otomatis
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

# AREA HUBUNGAN FILE DATA PENDUKUNG (WORD & PDF SEPAKAT MAKS 10MB)
st.write("### 📄 Lampirkan Dokumen Rujukan (.PDF / .DOCX)")
file_pendukung = st.file_uploader("Unggah file kurikulum, RPP asli, atau proposal dari HP/Drive Anda sebagai basis data rujukan SeHe.AI:", type=["pdf", "docx"])

# Logika penentuan prompt akhir dari chat input atau tombol pintasan cepat
prompt_input = st.chat_input("Tanya sesuatu ke SeHe.AI...")

# Ambil input, utamakan chat_input, jika kosong ambil dari tombol pintasan
final_prompt = prompt_input if prompt_input else st.session_state.prompt_pilihan

if final_prompt:
    # Reset prompt_pilihan setelah digunakan agar tidak memicu perulangan
    st.session_state.prompt_pilihan = None
    
    # Proteksi Ukuran File Terlebih Dahulu Sebelum Memulai Pengiriman (Batas 10MB)
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
        
        # Proses pembacaan dokumen rujukan lokal (Upload HP/Drive)
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

        # Jalankan pemindaian otomatis ke Drive latar belakang via kata kunci pipa (|)
        teks_tanya = str(final_prompt)
        referensi_lokal = baca_data_bantuan_drive(teks_tanya)
        if referensi_lokal:
            paket_konten.append(f"{referensi_lokal}\n\n")
            
        # Gabungkan teks pertanyaan utama pengguna ke paket pengiriman
        paket_konten.append(teks_tanya)

        # Perulangan otomatis mencoba API Key dan cadangan model jika server sibuk / Error 429 / Error 503
        for idx, current_key in enumerate(api_keys):
            sukses_merespons = False
            # Daftar model yang dicoba secara berurutan per API Key
            daftar_model = ['gemini-2.5-flash', 'gemini-1.5-flash']
            
            for target_model in daftar_model:
                try:
                    with st.spinner(f"SeHe.AI membedah data ({target_model} | Jalur {idx+1}/{len(api_keys)})..."):
                        temp_client = genai.Client(api_key=current_key)
                        response = temp_client.models.generate_content(
                            model=target_model,
                            contents=paket_konten,
                            config=ai_config
                        )
                        
                        if response and hasattr(response, 'text'):
                            ai_response = response.text
                            sukses_merespons = True
                            break # Keluar dari loop model karena sukses
                except Exception as e:
                    last_error_msg = str(e)
                    # Jika error karena server sibuk (503) atau batas limit (429), lanjut coba model berikutnya/key berikutnya
                    if "503" in last_error_msg or "429" in last_error_msg or "RESOURCE_EXHAUSTED" in last_error_msg:
                        continue
                    else:
                        # Jika error tipe lain (misal sinyal putus total), langsung hentikan loop model ini
                        break
            
            if sukses_merespons:
                break # Keluar dari loop API Key karena sudah dapat jawaban
            
            # Jika sudah di kunci terakhir dan semua model gagal karena sibuk
            if idx == len(api_keys) - 1 and not sukses_merespons:
                st.error("⚠️ Seluruh jalur kunci dan model cadangan SeHe.AI sedang padat di server Google. Silakan tunggu 10 detik lalu kirim ulang pesan Anda.")
                ai_response = None

            else:
                ai_response = f"Terjadi kesalahan sistem: {last_error_msg}. Pastikan internet Anda aktif."
                break

        # Tampilkan jawaban akhir di layar web dengan avatar ikan
        if ai_response is not None:
            with st.chat_message("assistant", avatar="🐟"):
                st.markdown(ai_response, unsafe_allow_html=True)
                
                # =============================================================
                # SOLUSI TOTAL KEBAL SYNTAXERROR: ENKAPSULASI TEKS HORIZONTAL
                # =============================================================
                css_bag_1 = "@page { size: 21cm 29.7cm; margin: 2.54cm 2.54cm 2.54cm 2.54cm; mso-page-orientation: portrait; } "
                css_bag_2 = "body { font-family: 'Segoe UI', Arial, sans-serif; padding: 0px; line-height: 1.6; background-color: #ffffff !important; color: #1e293b !important; } "
                css_bag_3 = "table { border-collapse: collapse; width: 100%; margin: 20px 0; mso-table-lspace: 0pt; mso-table-rspace: 0pt; } "
                css_bag_4 = "th { color: #ffffff !important; font-weight: bold; padding: 12px 14px; border-bottom: 2px solid #000000; } "
                css_bag_5 = "td { color: #334155 !important; padding: 12px 14px; border-bottom: 1px solid #e2e8f0; mso-line-height-rule: exactly; } "
                css_bag_6 = "th, td { border-left: none !important; border-right: none !important; }"
                
                css_word_style = css_bag_1 + css_bag_2 + css_bag_3 + css_bag_4 + css_bag_5 + css_bag_6
                
                # Gabungkan struktur HTML Word secara bersih tanpa merusak pembaca Python
                html_wrapped = """<html xmlns:o='urn:schemas-microsoft-com:office:office' xmlns:w='urn:schemas-microsoft-com:office:word' xmlns='http://w3.org'><head><meta charset='utf-8'><title>Dokumen SeHe AI</title><!--[if gte mso 9]><xml><w:WordDocument><w:View>Print</w:View><w:Zoom>100</w:Zoom><w:DoNotOptimizeForBrowser/></w:WordDocument></xml><![endif]--><style>""" + css_word_style + """</style></head><body>DOKUMEN_SEHE_AI_CONTENT</body></html>"""
                
                html_wrapped = html_wrapped.replace("DOKUMEN_SEHE_AI_CONTENT", ai_response)
                b64_html = base64.b64encode(html_wrapped.encode('utf-8')).decode('utf-8')
                new_idx = len(st.session_state.messages)
                
                # Tampilkan Dua Tombol Berjejer Estetis Kontras Tinggi (Cetak PDF & Simpan HTML)
                html_tombol = """
                <div class="action-buttons-container">
                    <button class="btn-action btn-blue" onclick="window.print()">
                        Cetak / PDF
                    </button>
                    <a class="btn-action btn-green" href="data:text/html;base64,B64_DATA_DOKUMEN" download="Dokumen_SeHe_AI_INDEX_BARU.html">
                        Simpan .HTML
                    </a>
                </div>
                """
                html_tombol = html_tombol.replace("B64_DATA_DOKUMEN", b64_html).replace("INDEX_BARU", str(new_idx))
                st.markdown(html_tombol, unsafe_allow_html=True)
                
            st.session_state.messages.append({"role": "assistant", "content": ai_response})
        else:
            if "429" not in last_error_msg and "RESOURCE_EXHAUSTED" not in last_error_msg:
                st.error(f"Gagal mendapatkan respons dari server Google AI Studio. Detail: {last_error_msg}")
