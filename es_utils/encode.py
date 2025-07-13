from config.settings import load_config
from sentence_transformers import SentenceTransformer
import os
config = load_config()
vector_config = config.vector_service

base_dir = os.path.dirname(os.path.abspath(__file__))
model_path = os.path.join(base_dir, "..", vector_config.model_path)
model = SentenceTransformer(model_path, device="cpu")
model.encode("warmup", normalize_embeddings=True)


def encode_vector(text: str) -> list:
    vec = model.encode(text, normalize_embeddings=True).tolist()


    return vec



if __name__ == "__main__":

    text ="物模型是什么呀"
    res = encode_vector(text)
    print(res)
