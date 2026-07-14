from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

VOCAB = {
    "silhouette": ["a-line", "ball gown", "mermaid", "sheath", "empire", "fit and flare", "trumpet"],
    "fabric": ["chiffon", "satin", "tulle", "velvet", "jersey", "silk", "organza", "crepe", "glitter"],
    "neckline": ["v neckline", "sweetheart neckline", "off shoulder", "square neckline",
                 "illusion neckline", "halter neckline", "one shoulder", "strapless", "boat neckline"],
    "sleeve": ["long sleeves", "cap sleeves", "puff sleeves", "sleeveless", "three quarter sleeves", "bell sleeves"],
    "length": ["floor length", "short", "tea length", "knee length", "ankle length"],
    "embellishment": ["beaded", "sequin embellishment", "embroidery", "feather trim", "lace applique", "crystal detailing"],
    "color": ["sage", "dusty blue", "royal navy", "ivory", "blush pink", "black", "burgundy", "emerald", "gold", "silver"],
    "category": ["bridesmaid dress", "prom gown", "wedding dress", "cocktail dress", "evening gown", "formal dress"],
}


def extract_attributes(description):
    text = description.lower()
    final_result = {}

    for attr in VOCAB:
        words_list = VOCAB[attr]
        matched = []
        for w in words_list:
            if w in text:
                matched.append(w)

        if len(matched) > 0:
            final_result[attr] = ", ".join(matched)
        else:
            final_result[attr] = "none"

    return final_result


class DescriptionInput(BaseModel):
    description: str


@app.post("/extract")
def extract(input: DescriptionInput):
    result = extract_attributes(input.description)
    return result