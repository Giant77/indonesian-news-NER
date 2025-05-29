from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from transformers import AutoTokenizer, AutoModelForTokenClassification
from collections import defaultdict
import torch
import uvicorn
import os
import json

# Path ke folder root project
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))

# Inisialisasi FastAPI
app = FastAPI(title="Indonesian NER API", description="Ekstraksi Entitas Politik dari Berita", version="1.0")

# Struktur request
class NERRequest(BaseModel):
    text: str
    model_name: str

# Daftar model yang disediakan
MODELS = {
    "xlm-roberta-indonesia": os.path.join(BASE_DIR, "saved_models", "cahya_xlm-roberta-base-indonesian-NER"),
    "indobert": os.path.join(BASE_DIR, "saved_models", "indobenchmark_indobert-base-p1"),
    "xlm-roberta-base": os.path.join(BASE_DIR, "saved_models", "xlm-roberta-base")
}

# Load semua model & tokenizer
loaded_models = {}
for name, path in MODELS.items():
    tokenizer = AutoTokenizer.from_pretrained(path)
    model = AutoModelForTokenClassification.from_pretrained(path)
    model.eval()
    loaded_models[name] = (tokenizer, model)

# Fungsi prediksi entitas
def predict(text, tokenizer, model):
    tokens = tokenizer(
        text,
        return_tensors="pt",
        truncation=True,
        return_offsets_mapping=True,
        return_attention_mask=True,
        return_token_type_ids=False,
        is_split_into_words=False
    )

    input_ids = tokens["input_ids"]
    attention_mask = tokens["attention_mask"]
    offset_mapping = tokens["offset_mapping"][0]
    word_ids = tokens.word_ids()

    with torch.no_grad():
        outputs = model(input_ids=input_ids, attention_mask=attention_mask)
    predictions = torch.argmax(outputs.logits, dim=2)[0]
    id2label = model.config.id2label

    entities = []
    current_word = ""
    current_label = None
    current_start = None
    current_end = None
    last_word_id = None

    for idx, word_id in enumerate(word_ids):
        if word_id is None:
            continue

        label = id2label[predictions[idx].item()]
        start, end = offset_mapping[idx].tolist()

        if label.startswith("B-"):
            if current_word:
                entities.append({
                    "word": current_word,
                    "label": current_label,
                    "start": current_start,
                    "end": current_end
                })
            current_word = text[start:end]
            current_label = label[2:]
            current_start = start
            current_end = end

        elif label.startswith("I-") and current_label == label[2:] and start == current_end:
            current_word += text[start:end]
            current_end = end
        elif label.startswith("I-") and current_label == label[2:]:
            current_word += " " + text[start:end]
            current_end = end

        else:
            if current_word:
                entities.append({
                    "word": current_word,
                    "label": current_label,
                    "start": current_start,
                    "end": current_end
                })
                current_word = ""
                current_label = None
                current_start = None
                current_end = None

    if current_word:
        entities.append({
            "word": current_word,
            "label": current_label,
            "start": current_start,
            "end": current_end
        })

    # Gabungkan entitas berturut-turut dengan label yang sama
    merged_entities = []
    for ent in entities:
        if merged_entities and ent["label"] == merged_entities[-1]["label"] and ent["start"] == merged_entities[-1]["end"]:
            # Lanjutkan entitas sebelumnya
            merged_entities[-1]["word"] += ent["word"]
            merged_entities[-1]["end"] = ent["end"]
        else:
            merged_entities.append(ent)

    return merged_entities


# Endpoint utama: /predict
@app.post("/predict")
def predict_ner(req: NERRequest):
    if req.model_name not in loaded_models:
        raise HTTPException(status_code=400, detail="Model tidak ditemukan. Gunakan salah satu dari: " + ", ".join(loaded_models.keys()))

    tokenizer, model = loaded_models[req.model_name]
    entities = predict(req.text, tokenizer, model)

    # Kelompokkan entitas berdasarkan label
    grouped_entities = defaultdict(list)
    for ent in entities:
        grouped_entities[ent["label"]].append(ent["word"])

    # Hilangkan duplikat & urutkan tiap grup
    grouped_entities = {
        label: sorted(list(set(words)))
        for label, words in grouped_entities.items()
    }

    # Hasil akhir
    result = {
        "grouped_entities": grouped_entities,  # tampilkan ini lebih awal
        "input_text": req.text,
        "model_used": req.model_name,
        "entities": entities  # masih dipakai untuk highlight
        }

    # Simpan ke output.json
    output_path = os.path.join(os.path.dirname(__file__), "output.json")

    # Cek jika file sudah ada dan berisi list
    if os.path.exists(output_path):
        with open(output_path, "r", encoding="utf-8") as f:
            try:
                data = json.load(f)
                if not isinstance(data, list):
                    data = [data]
            except json.JSONDecodeError:
                data = []
    else:
        data = []

    # Tambahkan hasil baru
    data.append(result)

    # Simpan ulang seluruh list
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    return result

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
