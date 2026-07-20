#!/usr/bin/env python3
"""
Enrichment pipeline for Lowell store finder.
Upserts enriched store data to Supabase retailer_details table,
then rebuilds stores.json and triggers a site rebuild.
"""
import json, urllib.request, os, datetime, sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(SCRIPT_DIR)
STORES_JSON = os.path.join(PROJECT_DIR, "src/data/stores.json")

ENV_PATH = os.path.expanduser("~/workspace/lowell-sales-dashboard/.env.local")

def load_env():
    with open(ENV_PATH) as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, v = line.split("=", 1)
                os.environ[k.strip()] = v.strip().strip('"').strip("'")

def upsert_to_retailer_details(records):
    """Upsert enriched records to Supabase retailer_details table."""
    url = f"{os.environ['SUPABASE_URL']}/rest/v1/retailer_details"
    key = os.environ["SUPABASE_SERVICE_KEY"]
    headers = {
        "apikey": key,
        "Authorization": f"Bearer {key}",
        "Content-Type": "application/json",
        "Prefer": "resolution=merge-duplicates",
    }
    
    # Build the payload
    payload = []
    for r in records:
        if not r.get("address") and not r.get("phone") and not r.get("website"):
            continue
        payload.append({
            "customer_name": r["name"],
            "google_address": r.get("address"),
            "phone": r.get("phone"),
            "website": r.get("website"),
            "google_place_id": r.get("google_place_id"),
            "enriched_at": datetime.datetime.utcnow().isoformat(),
        })
    
    if not payload:
        print("No records to upsert")
        return 0
    
    # Batch upsert (Supabase can handle up to ~5000 per request)
    data = json.dumps(payload).encode()
    req = urllib.request.Request(url, data=data, headers=headers, method="POST")
    
    try:
        resp = urllib.request.urlopen(req, timeout=30)
        print(f"Upserted {len(payload)} records (status: {resp.status})")
        return len(payload)
    except urllib.request.HTTPError as e:
        body = e.read().decode()[:500]
        print(f"HTTP {e.code} upserting: {body}")
        return -1
    except Exception as e:
        print(f"Error upserting: {e}")
        return -1

def merge_enrichment_files():
    """Read enrichment files from scripts/ dir and merge into stores.json."""
    enrichment_dir = SCRIPT_DIR
    merged = {}
    
    # Find all enriched_*.json files
    import glob
    for fpath in glob.glob(os.path.join(enrichment_dir, "enriched_*.json")):
        fname = os.path.basename(fpath)
        print(f"Reading {fname}...")
        with open(fpath) as f:
            try:
                records = json.load(f)
                for r in records:
                    name = r.get("name", "").strip()
                    if name:
                        merged[name] = r
                print(f"  -> {len(records)} records loaded")
            except json.JSONDecodeError as e:
                print(f"  -> ERROR parsing: {e}")
    
    return list(merged.values())

def main():
    load_env()
    
    import glob
    
    # Check for enrichment files
    enrichment_files = glob.glob(os.path.join(SCRIPT_DIR, "enriched_*.json"))
    if not enrichment_files:
        print("No enrichment files found in scripts/. Run market research agents first.")
        print("Expected files: enriched_ny_co.json, enriched_ca_nm_nj.json")
        sys.exit(1)
    
    print(f"Found {len(enrichment_files)} enrichment files:")
    for f in enrichment_files:
        print(f"  {os.path.basename(f)}")
    
    # Merge all enrichment
    enriched = merge_enrichment_files()
    print(f"\nTotal enriched records: {len(enriched)}")
    
    # Upsert to Supabase
    count = upsert_to_retailer_details(enriched)
    if count > 0:
        print(f"\n✅ Upserted {count} records to retailer_details")
    else:
        print(f"\n⚠️ No records upserted")
    
    print("\nDone. Run fetch_stores.py to rebuild stores.json with enriched data.")

if __name__ == "__main__":
    main()
