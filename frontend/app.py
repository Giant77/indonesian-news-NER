import streamlit as st
import requests
from streamlit_extras.badges import badge

# Konfigurasi tampilan halaman
st.set_page_config(layout="wide", page_title="Entitas Politik Berita Indonesia", page_icon="📰")

# Judul Aplikasi
st.markdown("""
    <h1 style='text-align: center; color: #1f77b4;'>Ekstraksi Entitas Politik dari Berita Indonesia</h1>
    <p style='text-align: center; font-size: 18px; color: gray;'>Kenali entitas penting seperti <b>tokoh</b>, <b>organisasi</b>, dan <b>lokasi</b> dari teks berita Indonesia.</p>
    <hr>
""", unsafe_allow_html=True)

# Tentang Proyek
with st.expander("📌 Tentang Proyek", expanded=True):
    st.markdown("""
    Proyek ini mengembangkan sistem Named Entity Recognition (NER) berbasis Transformer untuk mengenali entitas politik seperti tokoh, organisasi, dan lokasi dalam berita berbahasa Indonesia.
    Sistem ini memanfaatkan dataset IDN-NER, yang kaya akan anotasi entitas relevan, untuk mengoptimalkan kemampuan model dalam mengenali informasi penting.
    Aplikasi ini memungkinkan pengguna mengunggah teks berita dan melihat entitas yang dikenali secara visual melalui highlight warna yang informatif.

    <span style='color: gray;'>Entitas ditandai dengan warna:</span>
    - <span style='background-color:#BB9CC0; color:#1A1A1D; padding:2px 6px; border-radius:4px;'>PER</span> untuk orang  
    - <span style='background-color:#7AB2D3; color:#1A1A1D; padding:2px 6px; border-radius:4px;'>LOC</span> untuk lokasi  
    - <span style='background-color:#FFE99A; color:#1A1A1D; padding:2px 6px; border-radius:4px;'>ORG</span> untuk organisasi  
    """, unsafe_allow_html=True)

# Input Teks Berita
st.markdown("<h3 style='color:#1f77b4;'>Masukkan Teks Berita</h3>", unsafe_allow_html=True)
text_input = st.text_area("Teks Berita", placeholder="Tulis atau tempel teks berita di sini...", height=200, label_visibility="collapsed")

# Pilihan Model
st.markdown("<h3 style='color:#1f77b4;'>Pilih Model NER</h3>", unsafe_allow_html=True)
model_option = st.selectbox(
    label="Pilih model ekstraksi entitas:",
    options=["xlm-roberta-indonesia", "indobert", "xlm-roberta"],
    index=0,
    help="Pilih model bahasa yang akan digunakan untuk ekstraksi entitas."
)

# Fungsi highlight entitas
def highlight_entities(text, entities):
    entities = sorted(entities, key=lambda x: x["start"])
    result = ""
    last_idx = 0

    colors = {
        "PER": "#BB9CC0",
        "LOC": "#7AB2D3",
        "ORG": "#FFE99A"
    }

    for ent in entities:
        start, end, label = ent["start"], ent["end"], ent["label"]
        color = colors.get(label, "#ddd")

        result += text[last_idx:start]
        result += f"<mark style='background-color:{color}; color:#000; padding:2px 4px; border-radius:4px'>{text[start:end]} <span style='font-size:0.8em; color:#000;'>[{label}]</span></mark>"
        last_idx = end

    result += text[last_idx:]
    return result

# Tombol Ekstraksi
st.markdown("<h3 style='color:#1f77b4;'>Ekstrak Entitas</h3>", unsafe_allow_html=True)
if st.button("🔎 Jalankan Ekstraksi"):
    if not text_input.strip():
        st.warning("Teks tidak boleh kosong.")
    else:
        with st.spinner("Memproses teks..."):
            try:
                response = requests.post(
                    "http://localhost:8000/predict",
                    json={"text": text_input, "model_name": model_option}
                )
                response.raise_for_status()
                result = response.json()
                text, entities = result["input_text"], result["entities"]

                # Group entitas berdasarkan label
                from collections import defaultdict
                grouped_entities = defaultdict(list)
                for ent in entities:
                    grouped_entities[ent["label"]].append(ent["word"])

                # Tampilkan daftar entitas yang dikelompokkan
                st.markdown("### 📄 <span style='color:#1f77b4'>Daftar Entitas Terdeteksi</span>", unsafe_allow_html=True)
                for label in sorted(grouped_entities.keys()):
                    words = grouped_entities[label]
                    words_display = ", ".join(words)
                    st.markdown(f"{label} ({len(words)}): {words_display}")

                # Tampilkan visualisasi entitas dalam teks
                st.markdown("### 📄 <span style='color:#1f77b4'>Visualisasi Entitas dalam Teks</span>", unsafe_allow_html=True)
                highlighted_text = highlight_entities(text, entities)
                st.markdown(f"<div style='line-height: 1.8em; font-size: 16px'>{highlighted_text}</div>", unsafe_allow_html=True)
                st.markdown("<div style='margin-top: 30px'></div>", unsafe_allow_html=True)

                if entities:
                    st.success(f"Ditemukan {len(entities)} entitas.")
                else:
                    st.info("Tidak ada entitas yang dikenali.")

            except requests.exceptions.RequestException as e:
                st.error(f"Gagal memproses teks. Detail: {e}")

# Footer
st.markdown("""
    <hr style="margin-top: 100px;">
    <div style="text-align: center; font-size: 14px; color: gray;">
        Dibuat dengan ❤️ oleh Kelompok 8 · Powered by FastAPI & HuggingFace Transformers
    </div>
""", unsafe_allow_html=True)
