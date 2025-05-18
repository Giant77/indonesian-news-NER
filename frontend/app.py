import requests
import streamlit as st

API_URL = "http://localhost:8000/predict"

st.set_page_config(
    page_title="Indonesian's News Entity Recognition", 
    layout="centered"
)

st.title("📝 Smart Entity Detections For Indonesian News")

# 1. Judul berita
title = st.text_input(
    "Judul Berita",
    placeholder="Dekan Fakultas Kehutanan UGM Pastikan Kasmudjo Dosen Pembimbing Akademik Jokowi"
)

# 2. Isi berita
body = st.text_area(
    "Isi Berita",
    placeholder="""YOGYAKARTA, KOMPAS.com - Nama Ir. Kasmudjo kembali menjadi perbincangan usai dikunjungi 
    oleh Presiden ke-7, Joko Widodo. Ir. Kasmudjo selama ini diketahui sebagai dosen pembimbing akademik 
    Joko Widodo semasa kuliah di Fakultas Kehutanan UGM. Hal itu dibenarkan oleh Dekan Fakultas Kehutanan 
    UGM, Sigit Sunarta. Baca juga: Tawaran Jokowi untuk Kasmudjo Jelang Sidang Gugatan Ijazah Palsu... 
    'Iya benar (Ir. Kasmudjo pembimbing akademik Joko Widodo semasa kuliah),' ujar Dekan Fakultas Kehutanan 
    UGM, Sigit Sunarta saat dihubungi, Sabtu (17/05/2025). Sigit menyampaikan, Kasmudjo mulai menjalankan 
    tugasnya sebagai asisten ahli di Fakultas Kehutanan UGM pada tahun 1977."""
)

# 3. Pilih Model (opsional)
model = st.selectbox(
    "Model",
    ["IndoBert", "Xlm-Roberta", "Xlm-Roberta-ID"]
)

# generate email
if st.button("✉️ Deteksi Entitas"):
    if not (title and body):
        st.error("Mohon isi paling tidak: Judul, dan Isi Berita.")
        
    else:
        # susun payload
        payload = {
            "title": title,
            "body": body,
            "model": model,
        }

        # kirim ke backend
        try:
            # kirim request ke API
            response = requests.post(API_URL, json=payload, timeout=15)
            
            # cek status code
            response.raise_for_status()
            
            # ambil data dari response
            data = response.json()
            
            # tampilkan hasil
            st.subheader("📄 Entitas yang terdeteksi:")
            st.markdown(data.get("entity_list", "– Tidak ada output –"))

        except requests.exceptions.HTTPError as e:
            st.error(f"Server Error {response.status_code}: {response.text}")

        except requests.exceptions.RequestException as e:
            st.error(f"Gagal menghubungi server: {e}")
