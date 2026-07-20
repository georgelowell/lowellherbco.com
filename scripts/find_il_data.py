#!/usr/bin/env python3
"""Find IL stores in the right database table."""
import json, urllib.request, os, datetime

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

def headers(key):
    return {"apikey": key, "Authorization": f"Bearer {key}", "Accept": "application/json", "Prefer": "count=exact"}

cutoff = (datetime.date(2026, 7, 19) - datetime.timedelta(days=90)).isoformat()

print(f"Looking for IL data across all tables...")
print()

# 1. fact_sell_in_orders with ALL delivery_state variants
for table_name in ["fact_sell_in_orders"]:
    url = f"{MARKET_URL}/rest/v1/{table_name}"
    
    # Try different IL values
    for state_val in ["IL", "il", "Illinois", "Ill"]:
        q = f"{table_name}?select=account_name,delivery_state,source&delivery_state=eq.{state_val}&delivery_date=gte.{cutoff}&limit=5000"
        full_url = f"{url[:-len(table_name)]}{q}"
        try:
            req = urllib.request.Request(full_url, headers=headers(MARKET_KEY))
            resp = urllib.request.urlopen(req, timeout=15)
            rows = json.loads(resp.read())
            if rows:
                names = set(r.get("account_name") for r in rows if r.get("account_name"))
                print(f"  {table_name} delivery_state={state_val}: {len(names)} unique accounts")
        except:
            pass

# 2. Check mv_store_daily_metrics
table = "mv_store_daily_metrics"
url = f"{MARKET_URL}/rest/v1/{table}?select=retailer_name,retailer_state&retailer_state=eq.IL&limit=5000"
try:
    req = urllib.request.Request(url, headers=headers(MARKET_KEY))
    resp = urllib.request.urlopen(req, timeout=15)
    rows = json.loads(resp.read())
    print(f"\n  mv_store_daily_metrics state=IL: {len(rows)} rows")
    if rows:
        names = set(r.get("retailer_name") for r in rows if r.get("retailer_name"))
        print(f"  Unique retailers: {len(names)}")
except Exception as e:
    print(f"  mv_store_daily_metrics: {e}")

# 3. Check fact_sell_in_orders with a broader date range (maybe date column name is different)
import urllib.parse
for col in ["order_date", "delivery_date"]:
    url = f"{MARKET_URL}/rest/v1/fact_sell_in_orders?select=account_name,delivery_state,{col}&delivery_state=eq.IL&limit=5"
    try:
        req = urllib.request.Request(url, headers=headers(MARKET_KEY))
        resp = urllib.request.urlopen(req, timeout=15)
        rows = json.loads(resp.read())
        if rows:
            print(f"\n  fact_sell_in_orders (IL, {col}): {len(rows)} rows")
            for r in rows:
                print(f"    {r}")
    except:
        pass

# 4. List ALL tables in market DB that might have IL data
print("\n--- Exploring all tables in market DB ---")
tables_to_check = ["fact_sell_in_orders", "mv_store_daily_metrics", "fact_inventory_changes", 
                   "v_lovegrow_inventory", "retailer_territory_mapping"]

for table in tables_to_check:
    url = f"{MARKET_URL}/rest/v1/{table}?limit=1"
    try:
        req = urllib.request.Request(url, headers=headers(MARKET_KEY))
        resp = urllib.request.urlopen(req, timeout=10)
        resp.read()
        count = resp.headers.get("content-range", "0/0").split("/")[-1]
        # Also check if it has IL data
        url2 = f"{MARKET_URL}/rest/v1/{table}?limit=5"
        try:
            req2 = urllib.request.Request(url2, headers=headers(MARKET_KEY))
            resp2 = urllib.request.urlopen(req2, timeout=10)
            rows2 = json.loads(resp2.read())
            if rows2:
                sample_keys = list(rows2[0].keys())[:5]
                print(f"  {table}: {count} rows total | columns: {sample_keys}")
        except:
            print(f"  {table}: {count} rows total")
    except urllib.request.HTTPError as e:
        if e.code == 404:
            pass
        else:
            body = e.read().decode()[:100]
            if "relation" not in body:
                print(f"  {table}: HTTP {e.code}")

# 5. Check main DB sales_out for IL
print("\n--- Main DB check ---")
url = f"{MAIN_URL}/rest/v1/sales_out?select=customer_name,state&state=eq.IL&limit=5000"
try:
    req = urllib.request.Request(url, headers=headers(MAIN_KEY))
    resp = urllib.request.urlopen(req, timeout=15)
    rows = json.loads(resp.read())
    if rows:
        names = set(r.get("customer_name") for r in rows if r.get("customer_name"))
        print(f"  sales_out state=IL: {len(rows)} rows, {len(names)} unique customers")
        for n in sorted(names)[:10]:
            print(f"    {n}")
        if len(names) > 10:
            print(f"    ... and {len(names)-10} more")
    else:
        print(f"  sales_out state=IL: 0 rows")
except Exception as e:
    print(f"  sales_out: {e}")
