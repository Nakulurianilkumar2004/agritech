# app/modules/crop_chatbot/rag_retriever.py
import pandas as pd
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import os

df = None
embeddings = None
embed_model = None

# Paths to models folder inside this module
MODULE_DIR = os.path.dirname(__file__)
MODELS_DIR = os.path.join(MODULE_DIR, "models")
CSV_FILE = os.path.join(MODELS_DIR, "processed_dataset_100000.csv")
EMBED_FILE = os.path.join(MODELS_DIR, "embeddings.npy")

def load_rag_data():
    global df, embeddings, embed_model
    try:
        df = pd.read_csv(CSV_FILE)
        embeddings = np.load(EMBED_FILE)
        embed_model = SentenceTransformer("all-MiniLM-L6-v2")
        print("✅ RAG data loaded from models folder.")
    except Exception as e:
        print("❌ RAG load error:", e)

def get_top_answers(query, n=2):
    q_emb = embed_model.encode([query])
    sims = cosine_similarity(q_emb, embeddings)
    idx = np.argsort(sims[0])[::-1][:n]
    return df.iloc[idx]["answers"].tolist()