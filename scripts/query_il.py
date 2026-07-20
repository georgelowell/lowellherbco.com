#!/usr/bin/env python3
"""Query IL stores from fact_sell_in_orders with 90-day date range - all brands."""
import json, urllib.request, os, datetime, urllib.parse

env_path = os.path.expanduser("~/workspace/lowell-sales-dashboard/.env.local")
with open(env_path) as f:
    for line in f:
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            k, v = line.split("=", 1)
            os.environ[k.strip()] = v.strip().strip('"').strip("'")

MARKET_URL = "https://fulswsmkvoasnzbzzbrg.supabase.co"
MARKET_KEY = os.environ.get("SUPABASE_MARKET_SERVICE_KEY") or os.environ.get("SUPABASE_SERVICE_KEY")

cutoff = (datetime.date(2026, 7, 19) - datetime.timedelta(days=90)).isoformat()

# Query IL accounts without is_lowell filter (checking what flag exists)
# First check what brands/data exists
headers = {"apikey": MARKET_KEY, "Authorization": f"Bearer {MARKET_KEY}", "Accept": "application/json", "Prefer": "count=exact"}

# Get IL accounts
url = f"{MARKET_URL}/rest/v1/fact_sell_in_orders?select=account_name,delivery_date,brand_name,is_lowell&delivery_state=eq.IL&delivery_date=gte.{cutoff}&limit=5000"
req = urllib.request.Request(url, headers=headers)
resp = urllib.request.urlopen(req, timeout=30)
rows = json.loads(resp.read())

print(f"IL fact_sell_in_orders (90 days, all brands): {len(rows)} rows")

# Check what brands exist
brands = {}
for r in rows:
    b = r.get("brand_name", "UNKNOWN")
    brands[b] = brands.get(b, 0) + 1

print(f"\nBrands found:")
for b, c in sorted(brands.items(), key=lambda x: -x[1]):
    print(f"  {b}: {c}")

# Check is_lowell if it exists
has_lowell = any("is_lowell" in r for r in rows)
if rows:
    has_lowell = "is_lowell" in rows[0]
    print(f"\nis_lowell column exists: {has_lowell}")
    if has_lowell:
        lowell_true = sum(1 for r in rows if r.get("is_lowell") == True)
        lowell_false = sum(1 for r in rows if r.get("is_lowell") == False)
        lowell_none = sum(1 for r in rows if r.get("is_lowell") is None)
        print(f"  is_lowell=true: {lowell_true}")
        print(f"  is_lowell=false: {lowell_false}")
        print(f"  is_lowell=null: {lowell_none}")

# Get all unique account names (Lowell brands only)
lowell_accounts = set()
for r in rows:
    brand = (r.get("brand_name") or "").upper()
    name = r.get("account_name")
    if name and ("LOWELL" in brand or "LOWELL" in name.upper()):
        lowell_accounts.add(name)

# Also include if is_lowell flag is set
if has_lowell:
    for r in rows:
        if r.get("is_lowell") == True and r.get("account_name"):
            lowell_accounts.add(r.get("account_name"))

print(f"\n=== ILLINOIS: {len(lowell_accounts)} unique Lowell accounts in last 90 days ===")
for name in sorted(lowell_accounts):
    print(f"  {name}")

# Save IL list to compare with George's list
il_list = sorted(lowell_accounts)
project_dir = os.path.expanduser("~/workspace/lowell-migration")
with open(os.path.join(project_dir, "src/data/il_stores_90days.json"), "w") as f:
    json.dump({"illinois": il_list, "count": len(il_list), "updated": "2026-07-19"}, f, indent=2)
print(f"\nSaved to src/data/il_stores_90days.json ({len(il_list)} accounts)")

# Also check what accounts were NOT captured vs George's dashboard list
dashboard_accounts = [
    "Karma Club Chicago (Chicago)", "Ascend IL (Logan Square)", "Dutchess IL (Oak Park)",
    "Ivy Hall (Bucktown)", "Ascend IL (River North)", "Sway Dispensary (Chicago)",
    "Ascend IL (Fairview Heights)", "Terrabis IL (Grayville)", "Dutchess IL (Lynwood)",
    "Dutchess IL (Morton Grove)", "Ivy Hall (Logan Square)", "Bisa Lina (Carol Stream)",
    "Rise Illinois (Mundelein)", "Dispensary 33 (D33 5001 - N. Clark)", "UMI (Chicago)",
    "Snap Canna (Elk Grove Village)", "Ascend IL (Chicago Ridge)", "Bisa Lina (Joliet)",
    "Sparkd (Winthrop Harbor)", "Stash IL (Orland Hills)", "Rise Illinois (Village of Lake in the Hills)",
    "Guaranteed Dispensary IL (Chicago)", "Village Dispensary (Godfrey)", "NuEra (Pekin)",
    "NuEra (Urbana)", "Bridge City Collective (East Dubuque)", "Ascend IL (Ascend - Tinley Park)",
    "Rise Illinois (Joliet - Colorado Ave)", "Ivy Hall (Crystal Lake)", "Ivy Hall (Wkegan)",
    "Stash IL (Peru)", "Ascend IL (Midway Chicago)", "Rise Illinois (Effingham)",
    "Ascend IL (Collinsville)", "Dutchess IL (North Riverside)", "Ascend IL (Horizon Drive)",
    "Ivy Hall (Bolingbrook)", "NuEra (East Peoria)", "Ascend IL (Adams Street)",
    "Sparkd (Wabash)", "EarthMed (Addison)", "Dispensary 33 (D33 1152 - W. Randolph)",
    "Sunnyside Illinois (Wrigleyville)", "Ivy Hall (Montgomery)", "Sparkd (Richmond)",
    "Sparkd (Wicker Park)", "Terrabis IL (Dixon)", "Lyfe (Rockford)",
    "Natures Treatment of Illinois (Galesburg)", "EarthMed (Rosemont)", "Rise Illinois (Naperville)",
    "Ascend IL (Ascend Outlet - Northlake)", "Seven Point (Danville)", "Hatch (Addison)",
    "Lux Leaf IL (Matteson)", "Sociale Dispensary (Park Ridge)", "EarthMed (McHenry)",
    "VeriLife IL (60 W Superior)", "Herb Social (Lawrenceville)", "Sunnyside Illinois (South Beloit)",
    "Sunnyside Illinois (Rockford)", "Green Releaf IL (Villa Park)", "Dutchess IL (Batavia)",
    "Rise Illinois (Joliet - Rock Creek Blvd)", "Rise Illinois (Niles)", "Hatch (Wheeling)",
    "Mystic Greenz (Decatur)", "Green Temple (Troy)", "Parkway Dispensary (Tilton)",
    "Terrabis IL (Woodstock)", "VeriLife IL (Romeoville)", "VeriLife IL (Rosemont)",
    "Rise Illinois (Canton)", "Bloom Wellness Dispensary (Normal (Bradford Lane))",
    "Bloom Wellness Dispensary (Quincy West (1837))", "Rise Illinois (Charleston - IL)",
    "Bloom Wellness Dispensary (Hometown)", "Curaleaf IL (Northbrook)", "Smokehouse (Fox Lake)",
    "Mystic Greenz (Lincoln)", "Snap Canna (Pontiac)", "Kush21 (Jacksonville)",
    "Cloud 9 Cannabis (Edwardsville)", "NuEra (East Dubuque)", "VeriLife IL (North rora)",
    "VeriLife IL (Arlington Heights)", "Sunnyside Illinois (Elmwood Park)", "Sunnyside Illinois (Buffalo Grove)",
    "Rise Illinois (Quincy)", "Bloom Wellness Dispensary (Normal (Northbrook Drive))",
    "Bloom Wellness Dispensary (Quincy EAST (4440))", "Sunnyside Illinois (River North)",
    "Curaleaf IL (Deerfield)", "Curaleaf IL (New Lenox)", "Excelleaf (Dekalb)",
    "Terrace Cannabis (Moline)", "Windy City Cannabis (Carpentersville)", "Windy City Cannabis (Highwood)",
    "VeriLife IL (Ottawa)", "Cannabist IL (Villa Park)", "VeriLife IL (Galena)",
    "Sunnyside Illinois (Schmburg)", "High Haven IL (Darien)", "NuEra (Chicago)",
    "Thrive Dispensary (Mount Vernon)", "NuEra (Dekalb)", "Mystic Greenz (Belleville)",
    "Cloud 9 Cannabis (Champaign)", "Windy City Cannabis (Homewood)", "NuEra (rora)",
    "Terrabis IL (Plainfield)", "Sunnyside Illinois (Champaign)", "Sunnyside Illinois (Danville)",
    "Curaleaf IL (Skokie)", "Thrive Dispensary (Harrisburg)", "High Haven IL (Normal)",
    "Curaleaf IL (Worth)", "Curaleaf IL (Westmont)", "High Haven IL (Elgin)",
    "Cannabist IL (Chicago)", "Consume IL (Marion)", "Supergood Store (Des Plaines)",
    "Cloud 9 Cannabis (East Peoria)", "Terrabis IL (Mundelein)", "Tru Essence (Arlington Heights)",
    "Thrive Dispensary (Anna)", "Prairie Cannabis (South Loop)", "Sunnyside Illinois (Naperville)",
    "River Bluff Cannabis Inc (Roselle)", "Cloud 9 Cannabis (Schmburg)", "Perception Cannabis (Chicago)",
    "Curaleaf IL (Weed Street)", "Curaleaf IL (Justice)", "Consume IL (Antioch)",
    "Consume IL (Oakbrook Terrace)", "Consume IL (St. Charles)", "Consume IL (Chicago)",
    "Consume IL (Carbondale)", "The Dispensary IL (Fulton)", "Windy City Cannabis (Posen)",
    "VeriLife IL (Schmburg)", "Cloud 9 Cannabis (Oswego)", "Ivy Hall (Peoria)",
    "Ivy Hall (Streamwood)", "Ivy Hall (Edwardsville)", "Ivy Hall (Glendale Heights)",
]

dashboard_set = set(dashboard_accounts)
captured = lowell_accounts & dashboard_set
missing = dashboard_set - lowell_accounts
extra = lowell_accounts - dashboard_set

print(f"\n=== Match vs Dashboard List ===")
print(f"Dashboard list: {len(dashboard_accounts)} accounts")
print(f"Captured by is_lowell/brand filter: {len(captured)}")
print(f"Missing from query: {len(missing)}")
print(f"Extra (in DB but not in dashboard): {len(extra)}")
if missing:
    print(f"\nMissing accounts:")
    for n in sorted(missing):
        print(f"  {n}")
