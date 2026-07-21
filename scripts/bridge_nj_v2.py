#!/usr/bin/env python3
"""Final NJ name bridge. Read enriched_nj.json and create alias entries in retailer_details."""
import json, urllib.request, os, datetime, urllib.parse

env_path = os.path.expanduser("~/workspace/lowell-sales-dashboard/.env.local")
with open(env_path) as f:
    for line in f:
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            k, v = line.split("=", 1)
            os.environ[k.strip()] = v.strip().strip('"').strip("'")

KEY = os.environ["SUPABASE_SERVICE_KEY"]
HEADERS = {"apikey": KEY, "Authorization": f"Bearer {KEY}", "Content-Type": "application/json", "Prefer": "resolution=merge-duplicates"}
URL = "https://zjmqssqolcryoyxyonmf.supabase.co/rest/v1/retailer_details"

# Load enriched NJ data
with open(os.path.expanduser("~/workspace/lowell-migration/scripts/enriched_nj.json")) as f:
    enriched = json.load(f)

# Create a lookup by lowercase name
enriched_lookup = {}
for r in enriched:
    name = r["name"]
    addr = r.get("address", "")
    if addr:
        enriched_lookup[name.lower()] = r

# Load stores.json to find unmatched NJ store names
with open(os.path.expanduser("~/workspace/lowell-migration/src/data/stores.json")) as f:
    stores_data = json.load(f)

now = datetime.datetime.utcnow().isoformat()
upserts = []
already_upserted = set()

for s in stores_data["stores"]:
    name = s["name"]
    
    # Only NJ stores
    if not any(st in ("NJ", "nj", "New Jersey") for st in s.get("states", [])):
        continue
    
    # Already enriched?
    if s.get("address"):
        continue
    
    nlow = name.lower()
    
    # 1. Direct match
    match = enriched_lookup.get(nlow)
    
    # 2. Strip parenthetical city and try
    if not match and " (" in nlow:
        base = nlow.split(" (")[0]
        match = enriched_lookup.get(base)
    
    # 3. Base in enriched, city in enriched
    if not match and " (" in nlow:
        base = nlow.split(" (")[0]
        city = nlow.split("(")[1].rstrip(")")
        for en, er in enriched_lookup.items():
            if base in en and city in en:
                match = er
                break
    
    # 4. Just check first word for city-containing names
    if not match and " (" in nlow:
        first_word = nlow.split()[0]
        for en, er in enriched_lookup.items():
            if en.startswith(first_word) and len(en) < 40:
                addr = er.get("address", "")
                if ", NJ" in addr:
                    match = er
                    break
    
    if match and name not in already_upserted:
        upserts.append({
            "customer_name": name,
            "google_address": match.get("address"),
            "phone": match.get("phone"),
            "website": match.get("website"),
            "enriched_at": now,
        })
        already_upserted.add(name)

print(f"Found {len(upserts)} NJ stores needing name bridging")

# Upsert to Supabase
if upserts:
    import urllib.request
    success = 0
    for entry in upserts:
        data = json.dumps(entry).encode()
        qname = urllib.parse.quote(entry["customer_name"])
        req = urllib.request.Request(
            f"{URL}?customer_name=eq.{qname}", data=data, 
            headers=HEADERS, method="PATCH")
        try:
            urllib.request.urlopen(req, timeout=10)
            success += 1
        except:
            # INSERT instead
            req2 = urllib.request.Request(URL, data=data, headers=HEADERS, method="POST")
            try:
                urllib.request.urlopen(req2, timeout=10)
                success += 1
            except Exception as e:
                pass
    
    print(f"Upserted: {success}/{len(upserts)}")
else:
    print("Nothing to upsert")
