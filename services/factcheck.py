from dotenv import load_dotenv
load_dotenv()

import os, json, time
from googleapiclient.discovery import build

CACHE_FILE = "factcheck_cache.json"
API_KEY = os.getenv("FACTCHECK_API_KEY")

def _load_cache():
    try:
        with open(CACHE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return {}

def _save_cache(cache):
    with open(CACHE_FILE, "w", encoding="utf-8") as f:
        json.dump(cache, f, indent=2)

def _service():
    if not API_KEY:
        return None
    return build("factchecktools", "v1alpha1", developerKey=API_KEY)

def search_claims(query, language="en", page_size=5, use_cache=True):
    cache = _load_cache() if use_cache else {}
    key = f"{language}:{query}"
    if use_cache and key in cache:
        return cache[key]["resp"]

    svc = _service()
    if svc is None:
        return {"claims": []}

    req = svc.claims().search(query=query, languageCode=language, pageSize=page_size)
    resp = req.execute()
    if use_cache:
        cache[key] = {"fetched_at": int(time.time()), "resp": resp}
        _save_cache(cache)
    return resp
