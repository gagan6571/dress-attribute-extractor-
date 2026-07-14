# Dress Attribute Extractor

An AI/NLP pipeline that extracts structured attributes (Silhouette, Fabric, Neckline, Sleeve, Length, Embellishment, Color, Category) from unstructured fashion product descriptions and exposes them via a REST API.

## Problem Statement

Fashion product descriptions are written in free-form text. This project converts that text into structured, machine-readable JSON — useful for catalog tagging, search, filtering, and recommendation systems.

**Example**

Input:
> "Floor length chiffon bridesmaid dress with pleated bodice and V neckline available in sage and dusty blue"

Output:
```json
{
  "fabric": "chiffon",
  "neckline": "v neckline",
  "length": "floor length",
  "color": "sage, dusty blue",
  "category": "bridesmaid dress"
}
```

## Approach

A **lexicon-based extraction pipeline** was implemented: a curated vocabulary of known attribute values (necklines, fabrics, silhouettes, etc.) is matched against each description after text normalization.

This approach was chosen over a deep-learning model for two reasons:
- The labeled dataset has only 50 examples — too small to train a generalizable neural model without overfitting
- Attribute values in this domain come from a **bounded, known vocabulary** (fixed set of necklines, fabrics, etc.), making lexicon matching both accurate and fully interpretable

To validate this decision, a supervised ML baseline (**TF-IDF + Logistic Regression**) was also trained to predict the `category` field. It reached 95% training accuracy but only 40% test accuracy — confirming overfitting on small data and supporting the choice of the rule-based method as the primary approach.

## Dataset

- 50 labeled product descriptions across 8 attribute types
- 10 examples taken directly from the provided brief; 40 additional examples generated through templated combination of the attribute vocabulary for balanced coverage
- File: `dataset.csv`

## API

**Framework:** FastAPI + Uvicorn

**Endpoint:** `POST /extract`

Request:
```json
{ "description": "Off shoulder satin ball gown with corset bodice in royal navy" }
```

Response:
```json
{
  "silhouette": "ball gown",
  "fabric": "satin",
  "neckline": "off shoulder",
  "color": "royal navy",
  "category": "evening gown"
}
```

Run locally:
```bash
pip install fastapi uvicorn pandas scikit-learn
uvicorn api:app
```
Docs: `http://127.0.0.1:8000/docs`

## Evaluation

| Attribute | Accuracy | F1 |
|---|---|---|
| Silhouette | 0.88 | 0.82 |
| Fabric | 0.74 | 0.44 |
| Neckline | 0.98 | 0.89 |
| Sleeve | 0.70 | 0.71 |
| Length | 0.84 | 0.77 |
| Embellishment | 0.80 | 0.45 |
| Color | 0.98 | 0.99 |
| Category | 0.92 | 0.81 |

**Overall F1 Score: 0.73**

## Failure Case Analysis

1. **Vocabulary overlap across attribute types** — terms like "lace applique" (embellishment) share root words with the fabric vocabulary ("lace"), causing occasional mislabeling (e.g. predicting `fabric: "satin, lace"` instead of just `"satin"`). This is the main driver of lower F1 on Fabric and Embellishment.
2. **Missing synonyms** — informal terms not in the vocabulary (e.g. "glitter" instead of "sequin") go unmatched, resulting in a `"none"` prediction. Can be addressed with a synonym mapping or a semantic-similarity fallback layer.

## Tech Stack
- **Python, Pandas** — data handling
- **FastAPI, Uvicorn** — API layer
- **Scikit-learn** — ML baseline (TF-IDF + Logistic Regression), evaluation metrics (accuracy, F1)

## Project Structure
```
dress-attr-extractor/
├── dataset.csv
├── attribute_extraction.ipynb
├── api.py
├── requirements.txt
└── README.md
```