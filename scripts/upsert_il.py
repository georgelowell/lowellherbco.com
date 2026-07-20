#!/usr/bin/env python3
"""Upsert enriched IL store data to Supabase retailer_details."""
import json, urllib.request, os, datetime

env_path = os.path.expanduser("~/workspace/lowell-sales-dashboard/.env.local")
with open(env_path) as f:
    for line in f:
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            k, v = line.split("=", 1)
            os.environ[k.strip()] = v.strip().strip('"').strip("'")

SUPABASE_KEY = os.environ.get("SUPABASE_SERVICE_KEY")
with open("/Users/george-agent/workspace/lowell-migration/scripts/enriched_il.json") as f:
    records = json.load(f)

headers = {
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}",
    "Content-Type": "application/json",
    "Prefer": "resolution=merge-duplicates",
}

now = datetime.datetime.utcnow().isoformat()
payload = []
for r in records:
    if not r.get("address") and not r.get("phone") and not r.get("website"):
        continue
    payload.append({
        "customer_name": r["name"],
        "google_address": r.get("address"),
        "phone": r.get("phone"),
        "website": r.get("website"),
        "google_place_id": r.get("google_place_id"),
        "enriched_at": now,
    })

print(f"Upserting {len(payload)} IL records to retailer_details...")
data = json.dumps(payload).encode()
url = "https://zjmqssqolcryoyxyonmf.supabase.co/rest/v1/retailer_details"
req = urllib.request.Request(url, data=data, headers=headers, method="POST")
try:
    resp = urllib.request.urlopen(req, timeout=30)
    print(f"  Status: {resp.status}")
    print(f"  Upserted: {len(payload)} records")
except urllib.request.HTTPError as e:
    body = e.read().decode()[:500]
    print(f"  HTTP {e.code}: {body}")
