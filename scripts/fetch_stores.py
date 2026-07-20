#!/usr/bin/env python3
"""Fetch stores that bought Lowell in last 90 days and save to src/data/stores.json"""
import json, urllib.request, os, datetime
from urllib.parse import quote

env_path = os.path.expanduser("~/workspace/lowell-sales-dashboard/.env.local")
with open(env_path) as f:
    for line in f:
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            k, v = line.split("=", 1)
            os.environ[k.strip()] = v.strip().strip('"').strip("'")

MAIN_URL = "https://zjmqssqolcryoyxyonmf.supabase.co"
MARKET_URL = "https://fulswsmkvoasnzbzzbrg.supabase.co"
MAIN_KEY = os.environ.get("SUPABASE_SERVICE_KEY")
MARKET_KEY = os.environ.get("SUPABASE_MARKET_SERVICE_KEY")

def hdr(key):
    return {"apikey": key, "Authorization": f"Bearer {key}", "Accept": "application/json", "Content-Type": "application/json"}

def query_safe(url, headers, select, filters, limit=5000):
    q = f"{url}?select={select}&limit={limit}"
    for f in filters:
        q += f"&{f}"
    h = {**headers}
    h["Prefer"] = "count=exact"
    try:
        resp = urllib.request.urlopen(urllib.request.Request(q, headers=h), timeout=30)
        return json.loads(resp.read())
    except Exception as e:
        print(f"  ERROR: {e}")
        return []

cutoff = (datetime.date(2026, 7, 19) - datetime.timedelta(days=90)).isoformat()
all_customers = {}

print("Querying main DB...")
for state in ["CA", "NY", "CO", "NM"]:
    rows = query_safe(f"{MAIN_URL}/rest/v1/sales_out", hdr(MAIN_KEY), "customer_name,state",
        [f"is_lowell=eq.true", f"state=eq.{state}", f"delivery_date=gte.{cutoff}"])
    print(f"  {state}: {len(rows)} rows")
    for row in rows:
        n = row.get("customer_name")
        if n:
            if n not in all_customers:
                all_customers[n] = {"states": []}
            if state not in all_customers[n]["states"]:
                all_customers[n]["states"].append(state)

print("Querying market DB...")
for mstate in ["NJ", "nj", "New Jersey"]:
    qstate = quote(mstate)
    rows = query_safe(f"{MARKET_URL}/rest/v1/fact_sell_in_orders", hdr(MARKET_KEY), "account_name",
        [f"is_lowell=eq.true", f"delivery_state=eq.{qstate}", f"delivery_date=gte.{cutoff}"])
    print(f"  {mstate}: {len(rows)} rows")
    for row in rows:
        n = row.get("account_name")
        if n:
            if n not in all_customers:
                all_customers[n] = {"states": []}
            if mstate not in all_customers[n]["states"]:
                all_customers[n]["states"].append(mstate)

print(f"\nTotal unique: {len(all_customers)}")

print("Fetching retailer_details...")
rd = query_safe(f"{MAIN_URL}/rest/v1/retailer_details", hdr(MAIN_KEY),
    "customer_name,google_place_id,phone,website,google_address,enriched_at", [], limit=5000)
details = {}
for row in rd:
    details[row["customer_name"]] = {
        "google_place_id": row.get("google_place_id"),
        "phone": row.get("phone"),
        "website": row.get("website"),
        "address": row.get("google_address"),
        "enriched_at": row.get("enriched_at"),
    }

stores = []
for name in sorted(all_customers.keys()):
    info = all_customers[name]
    d = details.get(name, {})
    store = {
        "name": name,
        "states": info["states"],
        "address": d.get("address"),
        "phone": d.get("phone"),
        "website": d.get("website"),
        "google_place_id": d.get("google_place_id"),
    }
    stores.append(store)

project_dir = os.path.expanduser("~/workspace/lowell-migration")
output_path = os.path.join(project_dir, "src/data/stores.json")
output = json.dumps({"stores": stores, "updated": "2026-07-19", "count": len(stores)}, indent=2)
with open(output_path, "w") as f:
    f.write(output)
print(f"\nSaved {len(stores)} stores to {output_path}")

# Count by coverage
covered = sum(1 for s in stores if s["address"])
uncovered = sum(1 for s in stores if not s["address"])
print(f"With address: {covered}, Without: {uncovered}")
