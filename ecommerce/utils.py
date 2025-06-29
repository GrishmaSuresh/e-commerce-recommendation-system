# utils.py
from serpapi import GoogleSearch
import os

SERPAPI_KEY = "41bfb2c32185d34fbe49bf9c6f6ad3a1a2355ff3258ba6218ee26c22dd00a6ba"  # replace this

def get_product_image(product_name):
    params = {
        "q": product_name,
        "tbm": "isch",
        "api_key": SERPAPI_KEY
    }

    search = GoogleSearch(params)
    results = search.get_dict()

    # Get the first image result
    try:
        return results["images_results"][0]["thumbnail"]
    except Exception:
        return None  # fallback if no image is found
