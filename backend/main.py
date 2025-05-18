import os
import json
from typing import List, Optional
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from pathlib import Path
from transformers import AutoTokenizer, AutoModelForTokenClassification, pipeline
import uvicorn

app = FastAPI(title="Indonesian News Entity Recognition API")

BASE_DIR = Path(__file__).resolve().parent

def load_model(model_name: str):
    model_dict = {
        "IndoBert": "indobenchmark_indobert-base-p1",
        "Xlm-Roberta": "xlm-roberta-base",
        "Xlm-Roberta-ID": "cahya_xlm-roberta-base-indonesian-NER",
    }

    if model_name not in model_dict:
        raise ValueError(f"Unsupported model: {model_name}")
    
    model_dir = BASE_DIR.parent / "models" / model_dict[model_name]

    global label2id, id2label
    with open(model_dir / "label2id.json") as f:
        label2id = json.load(f)
    with open(model_dir / "id2label.json") as f:
        id2label = json.load(f)
    
    return model_dir

class NewsRequest(BaseModel):
    title: str
    body: str
    model: Optional[str] = "Xlm-Roberta-ID"  # ["IndoBert", "Xlm-Roberta", "Xlm-Roberta-ID"]

def preprocess_text(req: NewsRequest) -> str:
    """Combine title and body into a single text block for NER processing."""
    # TODO: preprocess tokenize text
    return f"{req.title.strip()}\n\n{req.body.strip()}"

def run_pipeline(text: str, model_path: Path):
    try:
        tokenizer = AutoTokenizer.from_pretrained(model_path)
        model = AutoModelForTokenClassification.from_pretrained(model_path)
        ner_pipeline = pipeline("ner", model=model, tokenizer=tokenizer, aggregation_strategy="simple")
        return ner_pipeline(text)
    except Exception as e:
        raise RuntimeError(f"Inference failed: {e}")

@app.post("/predict")
async def predict_entities(req: NewsRequest):
    model_path = load_model(req.model)
    processed_text = preprocess_text(req)
    entity_list = run_pipeline(processed_text, model_path)

    if not entity_list:
        raise HTTPException(status_code=404, detail=f"No entities detected by model {req.model}")
    
    return {"entities": entity_list}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
