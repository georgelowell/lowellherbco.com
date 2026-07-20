#!/usr/bin/env python3
"""Upsert NJ records individually to handle duplicates."""
import json, urllib.request, os, datetime, urllib.parse

env_path = os.path.expanduser("~/workspace/lowell-sales-dashboard/.env.local")
with open(env_path) as f:
    for line in f:
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            k, v = line.split("=", 1)
            os.environ[k.strip()] = v.strip().strip('"').strip("'")

SUPABASE_KEY = os.environ["SUPABASE_SERVICE_KEY"]
with open("/Users/george-agent/workspace/lowell-migration/scripts/enriched_nj.json") as f:
    records = json.load(f)

url = "https://zjmqssqolcryoyxyonmf.supabase.co/rest/v1/retailer_details"
base_headers = {
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}",
    "Content-Type": "application/json",
}

now = datetime.datetime.utcnow().isoformat()

success = 0
fail = 0
for r in records:
    if not r.get("address") and not r.get("phone") and not r.get("website"):
        continue
    
    entry = json.dumps({
        "customer_name": r["name"],
        "google_address": r.get("address"),
        "phone": r.get("phone"),
        "website": r.get("website"),
        "google_place_id": r.get("google_place_id"),
        "enriched_at": now,
    }).encode()
    
    qname = urllib.parse.quote(r["name"])
    
    # Try PATCH (upsert)
    headers = {**base_headers, "Prefer": "resolution=merge-duplicates"}
    req = urllib.request.Request(f"{url}?customer_name=eq.{qname}", data=entry, headers=headers, method="PATCH")
    try:
        resp = urllib.request.urlopen(req, timeout=10)
        success += 1
    except urllib.request.HTTPError as e:
        body = e.read().decode()[:100]
        fail += 1
        if fail <= 3:
            print(f"  FAIL: {r['name']}: HTTP {e.code}")

print(f"Upserted: {success}, Failed: {fail}")
