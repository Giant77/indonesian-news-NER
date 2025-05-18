# 📝 indonesian-news-NER

Sistem yang berpotensi mampu secara otomatis mengekstrak entitas-entitas penting ini dari artikel berita politik berbahasa Indonesia. Kemampuan ini diharapkan dapat mempermudah analisis konten berita, identifikasi aktor dan isu penting, serta pemantauan sentimen publik terkait peristiwa politik.

---

## 📦 Fitur Utama

-   Memilih kategori email: Akademik, Skripsi, Magang, dll.
-   Menentukan nada (tone) penulisan: formal, netral, atau santai.
-   Mendukung Bahasa Indonesia dan Inggris.
-   Mengisi poin-poin utama yang ingin disampaikan dalam email.
-   Menghasilkan email yang profesional, jelas, dan padat secara otomatis.

---

## 📁 Struktur Proyek

```
root
├── .env.example            # Contoh file API key Gemini
├── app.py                  # Frontend dengan Streamlit
├── backend/
│   └── main.py             # Backend API menggunakan FastAPI
├── frontend/
│   └── app.py              # frontEnd
└── requirements.txt        # Dependensi project

```

---

## ⚙️ Instalasi dan Menjalankan Proyek

### 1. Clone repository & setup local environment

-   Clone repository

```bash
git clone https://github.com/Giant77/indonesian-news-NER.git
cd indonesian-news-NER
```

### 2. Setup dan jalankan Backend (FastAPI)

-   Buat dan aktifkan environment

```bash
python3 -m venv env       # Aktivasi venv
source env/bin/activate   # Linux/macOS
env\Scripts\activate      # Windows
```

-   install library yang dibutuhkan

```bash
pip install -r requirements.txt
```

-   Jalankan server
    note: pastikan anda masih berada pada root project

```bash
uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
```

### 3. Setup dan jalankan Frontend (Streamlit)

-   Buka terminal baru:
    note: Pastikan sudah berada di direktori project

```bash
streamlit run app.py
```

---

## 🔐 Konfigurasi API Key Gemini

1. Buka [https://aistudio.google.com/app/apikey](https://aistudio.google.com/app/apikey)
2. Klik **Create API Key**.
3. Copy API key dan simpan ke dalam file `.env` di root project dengan format:

```env
GEMINI_API_KEY=YourSecretGeminiAPIKey
```

---

## 📬 Contoh Penggunaan

1. Pilih kategori dan gaya penulisan email.
2. Masukkan informasi penerima, subjek, dan poin-poin penting.
3. Klik tombol **"Buat Email"**.
4. Email hasil generate akan ditampilkan di halaman aplikasi.
