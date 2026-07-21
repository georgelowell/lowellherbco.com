#!/usr/bin/env python3
"""Verify what NJ names were stored and cross-reference."""
import json, urllib.request, os, urllib.parse

env_path = os.path.expanduser("~/workspace/lowell-sales-dashboard/.env.local")
with open(env_path) as f:
    for line in f:
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            k, v = line.split("=", 1)
            os.environ[k.strip()] = v.strip().strip('"').strip("'")

key = os.environ["SUPABASE_SERVICE_KEY"]
h = {"apikey": key, "Authorization": f"Bearer {key}", "Accept": "application/json", "Prefer": "count=exact"}

# Get ALL retailer_details
req = urllib.request.Request("https://zjmqssqolcryoyxyonmf.supabase.co/rest/v1/retailer_details?select=customer_name,google_address,phone,website&limit=5000", headers=h)
resp = urllib.request.urlopen(req, timeout=15)
rows = json.loads(resp.read())
total = resp.headers.get("content-range", "").split("/")[-1]
print(f"Total retailer_details rows: {total}")

# Build index
details = {}
for r in rows:
    details[r["customer_name"]] = r

# Load stores.json
with open(os.path.expanduser("~/workspace/lowell-migration/src/data/stores.json")) as f:
    sd = json.load(f)

# Check NJ stores
nj_matched = 0
nj_total = 0
for s in sd["stores"]:
    if not any(st in ("NJ","nj","New Jersey") for st in s.get("states",[])):
        continue
    nj_total += 1
    name = s["name"]
    d = details.get(name)
    if d and d.get("google_address"):
        nj_matched += 1
        s["address"] = d["google_address"]
        s["phone"] = d.get("phone") or s.get("phone")
        s["website"] = d.get("website") or s.get("website")

print(f"\nNJ stores: {nj_matched}/{nj_total} matched")

# Also check if the names exist in retailer_details
names_in_store = set()
for s in sd["stores"]:
    if any(st in ("NJ","nj","New Jersey") for st in s.get("states",[])):
        names_in_store.add(s["name"])

names_in_rd = set(details.keys())
store_not_in_rd = names_in_store - names_in_rd
rd_not_in_store = names_in_rd - names_in_store

print(f"\nNames in stores.json but NOT in retailer_details ({len(store_not_in_rd)}):")
for n in sorted(list(store_not_in_rd))[:10]:
    print(f"  {n}")

print(f"\nNames in retailer_details but NOT in stores.json ({len(rd_not_in_store)}):")
for n in sorted(list(rd_not_in_store))[:10]:
    addr = details[n].get("google_address", "")[:50]
    print(f"  {n}: {addr}")

# Save updated stores.json
sd["updated"] = "2026-07-20"
with open(os.path.expanduser("~/workspace/lowell-migration/src/data/stores.json"), "w") as f:
    json.dump(sd, f, indent=2)

# Final count
final_addr = sum(1 for s in sd["stores"] if s["address"])
final_phone = sum(1 for s in sd["stores"] if s["phone"])
final_web = sum(1 for s in sd["stores"] if s["website"])
print(f"\nFinal counts:")
print(f"  With address: {final_addr}")
print(f"  With phone: {final_phone}")
print(f"  With website: {final_web}")
