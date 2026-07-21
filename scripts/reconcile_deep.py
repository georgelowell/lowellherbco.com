#!/usr/bin/env python3
"""Deep reconciliation: match enriched names to store list names."""
import json, urllib.request, os

env_path = os.path.expanduser("~/workspace/lowell-sales-dashboard/.env.local")
with open(env_path) as f:
    for line in f:
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            k, v = line.split("=", 1)
            os.environ[k.strip()] = v.strip().strip('"').strip("'")

key = os.environ.get("SUPABASE_SERVICE_KEY")
h = {"apikey": key, "Authorization": f"Bearer {key}", "Accept": "application/json", "Prefer": "count=exact"}

# Get all retailer_details
req = urllib.request.Request("https://zjmqssqolcryoyxyonmf.supabase.co/rest/v1/retailer_details?select=customer_name,google_address,phone,website&limit=5000", headers=h)
resp = urllib.request.urlopen(req, timeout=15)
rd_rows = json.loads(resp.read())
details = {r["customer_name"]: r for r in rd_rows if r.get("google_address")}

print(f"retailer_details with addresses: {len(details)}")

with open(os.path.expanduser("~/workspace/lowell-migration/src/data/stores.json")) as f:
    stores_data = json.load(f)

stores = stores_data["stores"]
matched = 0
by_state = {}

for s in stores:
    name = s["name"]
    d = details.get(name)
    
    # Try stripping parenthetical city
    if not d and " (" in name:
        base = name.split(" (")[0]
        d = details.get(base)
    
    # Try the full name without parentheses at all
    if not d:
        for k, v in details.items():
            k_clean = k.lower().replace("(", "").replace(")", "").strip()
            name_clean = name.lower().replace("(", "").replace(")", "").strip()
            if k_clean == name_clean:
                d = v
                break
    
    if d and d.get("google_address"):
        s["address"] = d["google_address"]
        s["phone"] = d.get("phone") or s.get("phone")
        s["website"] = d.get("website") or s.get("website")
        matched += 1
    
    for state in s.get("states", []):
        key_s = state if state in ("NY","CA","CO","NM","IL") else "NJ"
        if key_s not in by_state:
            by_state[key_s] = {"total": 0, "matched": 0}
        by_state[key_s]["total"] += 1
        if d and d.get("google_address"):
            by_state[key_s]["matched"] += 1
        break

print(f"\nTotal matched: {matched}/{len(stores)}")
for k, v in sorted(by_state.items()):
    pct = v["matched"]*100//v["total"] if v["total"] else 0
    print(f"  {k}: {v['matched']}/{v['total']} ({pct}%)")

# List unmatched NJ to analyze the gap
nj_unmatched = [s["name"] for s in stores 
                if any(st in ("NJ","nj","New Jersey") for st in s.get("states",[]))
                and not s.get("address")]
print(f"\nUnmatched NJ stores ({len(nj_unmatched)}):")
for n in nj_unmatched[:40]:
    print(f"  {n}")
if len(nj_unmatched) > 40:
    print(f"  ... and {len(nj_unmatched)-40} more")

# Check: are these names in retailer_details under a different key?
print(f"\nRetailer_details names containing 'Bloc' or 'MPX' or 'Ascend':")
for k in sorted(details.keys()):
    if any(x in k.lower() for x in ['bloc ', 'mpx ', 'ascend', 'rise ', 'botera', 'botanist', 'apothecarium']):
        addr = details[k].get("google_address","")
        phone = details[k].get("phone","")[:15]
        print(f"  {k}: {addr[:60]}")
