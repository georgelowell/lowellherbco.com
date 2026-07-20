#!/usr/bin/env python3
"""Query NJ accounts from fact_sell_in_orders using same query as NJA dashboard."""
import json, urllib.request, os, datetime, urllib.parse

env_path = os.path.expanduser("~/workspace/lowell-sales-dashboard/.env.local")
with open(env_path) as f:
    for line in f:
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            k, v = line.split("=", 1)
            os.environ[k.strip()] = v.strip().strip('"').strip("'")

MARKET_URL = "https://fulswsmkvoasnzbzzbrg.supabase.co"
MAIN_URL = "https://zjmqssqolcryoyxyonmf.supabase.co"
MARKET_KEY = os.environ.get("SUPABASE_MARKET_SERVICE_KEY") or os.environ.get("SUPABASE_SERVICE_KEY")
MAIN_KEY = os.environ.get("SUPABASE_SERVICE_KEY")

def hdr(key):
    return {"apikey": key, "Authorization": f"Bearer {key}", "Accept": "application/json"}

def query_safe(url, headers, select, filters, limit=5000):
    q = f"{url}?select={select}&limit={limit}"
    for f in filters:
        q += f"&{f}"
    try:
        resp = urllib.request.urlopen(urllib.request.Request(q, headers={**headers, "Prefer": "count=exact"}), timeout=30)
        return json.loads(resp.read())
    except Exception as e:
        print(f"  ERROR: {e}")
        return []

cutoff = (datetime.date(2026, 7, 20) - datetime.timedelta(days=60)).isoformat()
print(f"=== NJ accounts — last 60 days (matching NJA dashboard) ===")
print(f"Cutoff: {cutoff}")
print()

# Query with brand_name filter (not is_lowell) — the NJA dashboard uses this
all_nj = {}

# NJ from fact_sell_in_orders
for mstate in ["NJ", "nj", "New Jersey"]:
    qstate = urllib.parse.quote(mstate)
    rows = query_safe(f"{MARKET_URL}/rest/v1/fact_sell_in_orders", hdr(MARKET_KEY), 
        "account_name,source,brand_name",
        [f"delivery_state=eq.{qstate}", f"delivery_date=gte.{cutoff}"])
    
    for row in rows:
        brand = (row.get("brand_name") or "").upper()
        name = row.get("account_name")
        if not name:
            continue
        # Only Lowell-branded products (same as dashboard)
        if "LOWELL" not in brand and "LOWELL" not in name.upper():
            continue
        if name not in all_nj:
            all_nj[name] = {"states": set(), "sources": set(), "brands": set()}
        all_nj[name]["states"].add(mstate)
        all_nj[name]["sources"].add(row.get("source", "unknown"))
        all_nj[name]["brands"].add(brand)

# NJ from main DB sales_out
nj_main = query_safe(f"{MAIN_URL}/rest/v1/sales_out", hdr(MAIN_KEY), "customer_name,item_name",
    [f"state=eq.NJ", f"delivery_date=gte.{cutoff}"])
for row in nj_main:
    name = row.get("customer_name")
    if name:
        if name not in all_nj:
            all_nj[name] = {"states": set(), "sources": set(), "brands": set()}
        all_nj[name]["states"].add("NJ")
        all_nj[name]["sources"].add("sales_out (main DB)")

print(f"Total NJ accounts (Lowell, 60 days): {len(all_nj)}")
print()

# Check enrichment status
rd = query_safe(f"{MAIN_URL}/rest/v1/retailer_details", hdr(MAIN_KEY),
    "customer_name,google_address,phone,website", [], limit=5000)
enriched = {r["customer_name"]: r for r in rd}

enriched_count = 0
for name in sorted(all_nj.keys()):
    info = all_nj[name]
    sources = ", ".join(sorted(info["sources"]))
    states = ", ".join(sorted(info["states"]))
    has_addr = "✅" if name in enriched and enriched[name].get("google_address") else "❌"
    phone = enriched[name].get("phone", "")[:15] if name in enriched and enriched[name].get("phone") else ""
    web = "✅" if name in enriched and enriched[name].get("website") else "❌"
    if has_addr == "✅":
        enriched_count += 1
    print(f"  {has_addr} {name:50s} | states: {states:15s} | sources: {sources}")

print(f"\nEnriched with address: {enriched_count}/{len(all_nj)} ({enriched_count/len(all_nj)*100:.0f}%)")
print(f"Need research: {len(all_nj) - enriched_count}")

# Save the full list
project_dir = os.path.expanduser("~/workspace/lowell-migration")
output = {
    "nj_accounts": sorted(all_nj.keys()),
    "count": len(all_nj),
    "enriched": enriched_count,
    "need_research": len(all_nj) - enriched_count,
    "details": {k: {
        "states": list(v["states"]),
        "sources": list(v["sources"]),
        "enriched": k in enriched,
        "has_address": k in enriched and enriched[k].get("google_address") is not None,
    } for k, v in all_nj.items()},
    "updated": "2026-07-20",
}
with open(os.path.join(project_dir, "src/data/nj_accounts_60days.json"), "w") as f:
    json.dump(output, f, indent=2)
print(f"\nSaved to src/data/nj_accounts_60days.json")
