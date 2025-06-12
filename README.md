# 📝 indonesian-news-NER

Sistem yang berpotensi mampu secara otomatis mengekstrak entitas-entitas penting ini dari artikel berita politik berbahasa Indonesia. Kemampuan ini diharapkan dapat mempermudah analisis konten berita, identifikasi aktor dan isu penting, serta pemantauan sentimen publik terkait peristiwa politik.

---

## 📁 Struktur Proyek

```
root
├── backend/
│   ├── main.py             # Backend API menggunakan FastAPI
│   └── output.json         # Log entitas yang terdeteksi
├── frontend/
│   └── app.py              # Frontend dengan Streamlit
├── saved_models/           # Direktori model
│   └── model_dirs/
└── requirements.txt        # Dependensi project

```

---

## ⚙️ Instalasi dan Menjalankan Proyek

### 1. Clone repository & setup local environment

- Clone repository

```bash
git clone https://github.com/Giant77/indonesian-news-NER.git
cd indonesian-news-NER
```

### 2. Download model

Jalankan snippet berikut, atau download model yang telah di fine-tune pada
web kaggle pada link [berikut](https://www.kaggle.com/code/svzip/240287985),
atau lihat detail pada notebook [berikut](https://www.kaggle.com/code/giant77/id-ner-news/notebook)

```bash
kaggle kernels output giant77/id-ner-news -p .
```

### 3. Setup dan jalankan Backend (FastAPI)

- Buat dan aktifkan environment (Opsional)

```bash
python3 -m venv env       # Aktivasi venv
source env/bin/activate   # Linux/macOS
env\Scripts\activate      # Windows
```

- install library yang dibutuhkan

```bash
pip install -r requirements.txt
```

- Jalankan server
  note: pastikan anda masih berada pada root project

```bash
uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
```

### 4. Setup dan jalankan Frontend (Streamlit)

- Buka terminal baru:
  note: Pastikan sudah berada di direktori project.

```bash
streamlit run app.py
```

---

## 📬 Contoh Penggunaan

1. Masukkan kutipan berita ataupun text yang ingin dilakukan extraksi entitas.
2. Pilih Model yang ingin digunakan.
3. Output dihasilkan dalam 2 bentuk:
   - Daftar entitas pada text,
   - Text input dengan _highlight_ pada entitas yang terdeteksi.
