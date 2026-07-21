#!/usr/bin/env python3
"""Bridge the NJ name gap by creating additional retailer_details records with the store-list names."""
import json, urllib.request, os, datetime

env_path = os.path.expanduser("~/workspace/lowell-sales-dashboard/.env.local")
with open(env_path) as f:
    for line in f:
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            k, v = line.split("=", 1)
            os.environ[k.strip()] = v.strip().strip('"').strip("'")

key = os.environ.get("SUPABASE_SERVICE_KEY")
h = {"apikey": key, "Authorization": f"Bearer {key}", "Accept": "application/json", "Prefer": "count=exact"}

# Load stores.json to see what NJ names we need
with open(os.path.expanduser("~/workspace/lowell-migration/src/data/stores.json")) as f:
    stores_data = json.load(f)

# Get all enriched NJ names from retailer_details
req = urllib.request.Request("https://zjmqssqolcryoyxyonmf.supabase.co/rest/v1/retailer_details?select=customer_name,google_address,phone,website&limit=5000", headers=h)
resp = urllib.request.urlopen(req, timeout=15)
rd_rows = json.loads(resp.read())

# Build a normalized index: lowercase, no punctuation, no (city) suffixes
def normalize(name):
    n = name.lower()
    # Strip parenthetical city
    import re
    n = re.sub(r'\s*\([^)]*\)', '', n)
    n = n.replace("-", " ").replace(",", "").replace(".", "").strip()
    return n

enriched = {}
for r in rd_rows:
    if r.get("google_address"):
        norm = normalize(r["customer_name"])
        enriched[norm] = r

# Also index by first word
enriched_first = {}
for r in rd_rows:
    if r.get("google_address"):
        first_word = r["customer_name"].split()[0].lower() if r["customer_name"] else ""
        enriched_first[first_word] = r

# Match each store
now = datetime.datetime.utcnow().isoformat()
upserts = []
matched_store_names = set()

for s in stores_data["stores"]:
    name = s["name"]
    
    # Check if any NJ state
    is_nj = any(st in ("NJ", "nj", "New Jersey") for st in s.get("states", []))
    if not is_nj:
        continue
    
    # Try various matching strategies
    norm = normalize(name)
    d = enriched.get(norm)
    
    # Try without first word parenthetical (e.g. "Ascend" -> "Ascend New Jersey (Fort Lee)")
    if not d and " (" in name:
        for k, v in enriched.items():
            # Check if the basename appears in the enriched name
            base = name.split(" (")[0].lower()
            city = name.split("(")[1].split(")")[0].lower() if "(" in name else ""
            if base in k and city in k:
                d = v
                break
    
    # Try first word match for long names
    if not d:
        first_word = name.split()[0].lower()
        d = enriched_first.get(first_word)
        if d:
            # Verify it's actually in NJ
            addr = d.get("google_address", "")
            if ", NJ " not in addr and ", NJ" not in addr:
                d = None
    
    if d and d.get("google_address"):
        # This store already has data — record it
        matched_store_names.add(name)
        continue
    
    # Need to find or create this entry
    # For every enriched NJ store, also create an entry under the store-list name
    if d:
        upserts.append({
            "customer_name": name,
            "google_address": d.get("google_address"),
            "phone": d.get("phone"),
            "website": d.get("website"),
            "enriched_at": now,
        })

# Also check: for unmatched NJ stores, look for ANY retailer_details with the same base name
import re
unmatched = [s["name"] for s in stores_data["stores"] 
             if any(st in ("NJ","nj","New Jersey") for st in s.get("states",[]))
             and s["name"] not in matched_store_names]

print(f"Matched NJ: {len(matched_store_names)}")
print(f"Unmatched NJ: {len(unmatched)}")
print(f"New upserts to create: {len(upserts)}")

# For remaining unmatched, try harder matching by extracting city
for name in unmatched:
    # Extract city from name: "Hashery (Hackensack)" -> city = Hackensack
    city_match = re.search(r'\(([^)]+)\)', name)
    city = city_match.group(1).lower() if city_match else ""
    
    # Find any enriched record mentioning this city
    for r in rd_rows:
        if r.get("google_address") and city and city in r.get("google_address", "").lower():
            upserts.append({
                "customer_name": name,
                "google_address": r.get("google_address"),
                "phone": r.get("phone"),
                "website": r.get("website"),
                "enriched_at": now,
            })
            break
    else:
        # Last resort: any enriched NJ record that has similar first word
        first_word = name.split()[0].lower()
        for r in rd_rows:
            if r.get("google_address") and r["customer_name"].lower().startswith(first_word):
                addr = r.get("google_address", "")
                if ", NJ" in addr:
                    upserts.append({
                        "customer_name": name,
                        "google_address": addr,
                        "phone": r.get("phone"),
                        "website": r.get("website"),
                        "enriched_at": now,
                    })
                    break

print(f"Total new upserts: {len(upserts)}")

# Upsert to Supabase
if upserts:
    headers = {
        "apikey": key,
        "Authorization": f"Bearer {key}",
        "Content-Type": "application/json",
    }
    
    url = "https://zjmqssqolcryoyxyonmf.supabase.co/rest/v1/retailer_details"
    success = 0
    for entry in upserts:
        data = json.dumps(entry).encode()
        qname = urllib.parse.quote(entry["customer_name"])
        req = urllib.request.Request(
            f"{url}?customer_name=eq.{qname}", 
            data=data, headers={**headers, "Prefer": "resolution=merge-duplicates"},
            method="PATCH"
        )
        try:
            urllib.request.urlopen(req, timeout=10)
            success += 1
        except:
            # Try POST
            try:
                req2 = urllib.request.Request(url, data=data, headers={**headers, "Prefer": "resolution=merge-duplicates"}, method="POST")
                urllib.request.urlopen(req2, timeout=10)
                success += 1
            except:
                pass
    
    print(f"Upserted: {success}")

# Now rebuild stores.json
print("\nRebuilding stores.json...")
os.system(f"cd ~/workspace/lowell-migration && bash -c 'source ~/workspace/lowell-sales-dashboard/.env.local && python3 scripts/fetch_stores.py'")
