#!/usr/bin/env python3
"""Single batch upsert of enriched NJ data to Supabase."""
import json, urllib.request, os, datetime, urllib.parse

env_path = os.path.expanduser("~/workspace/lowell-sales-dashboard/.env.local")
with open(env_path) as f:
    for line in f:
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            k, v = line.split("=", 1)
            os.environ[k.strip()] = v.strip().strip('"').strip("'")

key = os.environ["SUPABASE_SERVICE_KEY"]

# Load enriched NJ data
with open(os.path.expanduser("~/workspace/lowell-migration/scripts/enriched_nj.json")) as f:
    enriched = json.load(f)

now = datetime.datetime.utcnow().isoformat()
headers = {
    "apikey": key,
    "Authorization": f"Bearer {key}",
    "Content-Type": "application/json",
}

url = "https://zjmqssqolcryoyxyonmf.supabase.co/rest/v1/retailer_details"

success = 0
fail = 0
for r in enriched:
    name = r["name"]
    if not r.get("address"):
        fail += 1
        continue
    
    entry = {
        "customer_name": name,
        "google_address": r.get("address"),
        "phone": r.get("phone"),
        "website": r.get("website"),
        "google_place_id": None,
        "enriched_at": now,
    }
    
    # Upsert using POST with on_conflict
    payload = json.dumps(entry).encode()
    
    # Try POST with on_conflict
    post_headers = {**headers, "Prefer": "resolution=merge-duplicates"}
    req = urllib.request.Request(url, data=payload, headers=post_headers, method="POST")
    try:
        urllib.request.urlopen(req, timeout=10)
        success += 1
    except urllib.request.HTTPError as e:
        body = e.read().decode()[:200]
        fail += 1
        if fail <= 5:
            print(f"FAIL {name}: HTTP {e.code} - {body}")
    except Exception as e:
        fail += 1
        if fail <= 5:
            print(f"FAIL {name}: {e}")

print(f"\nDone: {success} OK, {fail} failed")
