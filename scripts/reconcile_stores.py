#!/usr/bin/env python3
"""Reconcile store names between stores.json and retailer_details for accurate enrichment stats."""
import json, urllib.request, os, datetime

env_path = os.path.expanduser("~/workspace/lowell-sales-dashboard/.env.local")
with open(env_path) as f:
    for line in f:
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            k, v = line.split("=", 1)
            os.environ[k.strip()] = v.strip().strip('"').strip("'")

MAIN_URL = "https://zjmqssqolcryoyxyonmf.supabase.co"
MAIN_KEY = os.environ.get("SUPABASE_SERVICE_KEY")

def hdr(key):
    return {"apikey": key, "Authorization": f"Bearer {key}", "Accept": "application/json"}

def query_safe(url, headers, select, filters, limit=5000):
    q = f"{url}?select={select}&limit={limit}"
    for f in filters:
        q += f"&{f}"
    try:
        resp = urllib.request.urlopen(urllib.request.Request(q, headers={**headers, "Prefer": "count=exact"}), timeout=15)
        return json.loads(resp.read()), resp.headers.get("content-range", "").split("/")[-1]
    except Exception as e:
        print(f"  ERROR: {e}")
        return [], "0"

# Get all retailer_details
print("Fetching all retailer_details...")
rows, total = query_safe(f"{MAIN_URL}/rest/v1/retailer_details", hdr(MAIN_KEY),
    "customer_name,google_address,phone,website", [], limit=5000)
print(f"  Total in DB: {total}")

details_index = {}
for r in rows:
    details_index[r["customer_name"]] = r

# Load stores.json
with open(os.path.expanduser("~/workspace/lowell-migration/src/data/stores.json")) as f:
    stores_data = json.load(f)

stores = stores_data["stores"]
print(f"Total stores in stores.json: {len(stores)}")

# Match each store to its enrichment
enriched = 0
by_state = {}
for s in stores:
    name = s["name"]
    # Try exact match
    details = details_index.get(name)
    
    # If no exact match, try fuzzy: strip parenthetical city suffix
    if not details:
        # "Hashery (Hackensack)" -> try "Hashery"
        base = name.split(" (")[0] if " (" in name else name
        details = details_index.get(base)
    
    # Try containment
    if not details:
        for key in details_index:
            if key in name or name in key:
                details = details_index[key]
                break
    
    if details and details.get("google_address"):
        s["address"] = details["google_address"]
        s["phone"] = details.get("phone") or s.get("phone")
        s["website"] = details.get("website") or s.get("website")
        enriched += 1
    
    # Count by state
    for state in s.get("states", []):
        key = state if state in ("NY", "CA", "CO", "NM", "IL") else "NJ"
        if key not in by_state:
            by_state[key] = {"total": 0, "enriched": 0}
        by_state[key]["total"] += 1
        if details and details.get("google_address"):
            by_state[key]["enriched"] += 1
        break  # count once

print(f"\nAfter reconciliation: {enriched}/{len(stores)} enriched ({enriched*100//len(stores)}%)")
print()
for state, counts in sorted(by_state.items()):
    pct = counts["enriched"] * 100 // counts["total"] if counts["total"] else 0
    print(f"  {state}: {counts['enriched']}/{counts['total']} ({pct}%)")

# Save updated stores.json
output = json.dumps(stores_data, indent=2)
with open(os.path.expanduser("~/workspace/lowell-migration/src/data/stores.json"), "w") as f:
    f.write(output)
print(f"\nSaved updated stores.json with reconciled data")
