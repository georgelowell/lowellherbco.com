#!/usr/bin/env python3
"""Query NJ and IL stores active in last 90 days."""
import json, urllib.request, os, datetime, urllib.parse

env_path = os.path.expanduser("~/workspace/lowell-sales-dashboard/.env.local")
with open(env_path) as f:
    for line in f:
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            k, v = line.split("=", 1)
            os.environ[k.strip()] = v.strip().strip('"').strip("'")

MAIN_URL = "https://zjmqssqolcryoyxyonmf.supabase.co"
MARKET_URL = "https://fulswsmkvoasnzbzzbrg.supabase.co"
MAIN_KEY = os.environ["SUPABASE_SERVICE_KEY"]
MARKET_KEY = os.environ["SUPABASE_MARKET_SERVICE_KEY"]

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

cutoff = (datetime.date(2026, 7, 19) - datetime.timedelta(days=90)).isoformat()
print(f"Cutoff: {cutoff}")
print()

# ===== NEW JERSEY =====
nj_accounts = {}
for mstate in ["NJ", "nj", "New Jersey"]:
    qstate = urllib.parse.quote(mstate)
    rows = query_safe(f"{MARKET_URL}/rest/v1/fact_sell_in_orders", hdr(MARKET_KEY), "account_name,delivery_state,source",
        [f"is_lowell=eq.true", f"delivery_state=eq.{qstate}", f"delivery_date=gte.{cutoff}"])
    for row in rows:
        n = row.get("account_name")
        if n:
            if n not in nj_accounts:
                nj_accounts[n] = {"delivery_states": set(), "source": None}
            nj_accounts[n]["delivery_states"].add(row.get("delivery_state"))
            if row.get("source"):
                nj_accounts[n]["source"] = row.get("source")

print(f"=== NEW JERSEY: {len(nj_accounts)} unique accounts in last 90 days ===")
for name in sorted(nj_accounts.keys()):
    info = nj_accounts[name]
    states = ", ".join(sorted(info["delivery_states"]))
    print(f"  {name} | delivery_state: {states} | source: {info['source']}")

# ===== ILLINOIS =====
il_accounts = {}
rows = query_safe(f"{MARKET_URL}/rest/v1/fact_sell_in_orders", hdr(MARKET_KEY), "account_name,delivery_state,source",
    [f"is_lowell=eq.true", f"delivery_state=eq.IL", f"delivery_date=gte.{cutoff}"])
for row in rows:
    n = row.get("account_name")
    if n:
        if n not in il_accounts:
            il_accounts[n] = {"delivery_states": set(), "source": None}
        il_accounts[n]["delivery_states"].add(row.get("delivery_state"))
        if row.get("source"):
            il_accounts[n]["source"] = row.get("source")

print(f"\n=== ILLINOIS: {len(il_accounts)} unique accounts in last 90 days ===")
for name in sorted(il_accounts.keys()):
    info = il_accounts[name]
    print(f"  {name} | source: {info['source']}")

# Also check main DB for NJ and IL
for state in ["NJ", "IL"]:
    rows = query_safe(f"{MAIN_URL}/rest/v1/sales_out", hdr(MAIN_KEY), "customer_name",
        [f"is_lowell=eq.true", f"state=eq.{state}", f"delivery_date=gte.{cutoff}"])
    names = set(row.get("customer_name") for row in rows if row.get("customer_name"))
    if names:
        print(f"\n  Also in Main DB state={state}: {len(names)} customer(s)")
        for n in sorted(names):
            print(f"    {n}")
    else:
        print(f"\n  Main DB state={state}: 0 rows")

# ===== SUMMARY =====
print(f"\n{'='*60}")
print(f"TOTAL: NJ={len(nj_accounts)}, IL={len(il_accounts)}")
print(f"{'='*60}")

# Save NJ and IL lists
output = {
    "new_jersey": sorted(nj_accounts.keys()),
    "illinois": sorted(il_accounts.keys()),
    "nj_details": {k: {"delivery_states": list(v["delivery_states"]), "source": v["source"]} for k, v in nj_accounts.items()},
    "il_details": {k: {"delivery_states": list(v["delivery_states"]), "source": v["source"]} for k, v in il_accounts.items()},
    "updated": "2026-07-19",
}

project_dir = os.path.expanduser("~/workspace/lowell-migration")
with open(os.path.join(project_dir, "src/data/nj_il_stores.json"), "w") as f:
    json.dump(output, f, indent=2)
print(f"\nSaved to src/data/nj_il_stores.json")
