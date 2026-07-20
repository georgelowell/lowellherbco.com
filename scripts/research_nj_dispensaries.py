#!/usr/bin/env python3
"""
Research NJ dispensaries — search for address, phone, website, storefront URL, and coordinates.
For each store, try multiple search patterns and save results to enriched_nj.json.
"""

import json
import os
import urllib.request
import urllib.parse
import time
import re
import sys
from html.parser import HTMLParser

# Paths
WORKSPACE = os.path.expanduser("~/workspace/lowell-migration")
OUTPUT_PATH = os.path.join(WORKSPACE, "scripts", "enriched_nj.json")
ACCOUNTS_PATH = os.path.join(WORKSPACE, "src/data/nj_accounts_60days.json")

# Load the store list
with open(ACCOUNTS_PATH) as f:
    data = json.load(f)

store_names = data["nj_accounts"]
print(f"Total stores to research: {len(store_names)}")

# Load any existing results
existing = {}
if os.path.exists(OUTPUT_PATH):
    with open(OUTPUT_PATH) as f:
        existing_list = json.load(f)
        for item in existing_list:
            existing[item["name"]] = item
    print(f"Loaded {len(existing)} existing results")

# === Chain data (known addresses) ===
# Manually researched chain data
CHAIN_DATA = {
    "Ascend New Jersey (Fort Lee)": {
        "address": "461-469 West St, Fort Lee, NJ 07024",
        "phone": "(973) 200-7696",
        "website": "https://letsascend.com",
        "storefront_url": "https://letsascend.com/locations/new-jersey/fort-lee",
    },
    "Ascend New Jersey (Rochelle Park)": {
        "address": "174 NJ-17 N, Rochelle Park, NJ 07662",
        "phone": "(973) 370-3150",
        "website": "https://letsascend.com",
        "storefront_url": "https://letsascend.com/locations/new-jersey/rochelle-park",
    },
    "Ascend New Jersey (Wharton)": {
        "address": "325 NJ-15, Wharton, NJ 07885",
        "phone": "(973) 786-1810",
        "website": "https://letsascend.com",
        "storefront_url": "https://letsascend.com/locations/new-jersey/wharton",
    },
    "Ascend": {  # Generic — maps to Fort Lee
        "address": "461-469 West St, Fort Lee, NJ 07024",
        "phone": "(973) 200-7696",
        "website": "https://letsascend.com",
        "storefront_url": "https://letsascend.com/locations/new-jersey/fort-lee",
    },
    "The Apothecarium New Jersey (Lodi)": {
        "address": "200 NJ-17, Lodi, NJ 07644",
        "phone": "(973) 996-1420",
        "website": "https://apothecarium.com",
        "storefront_url": "https://apothecarium.com/locations/lodi",
    },
    "The Apothecarium New Jersey (Maplewood)": {
        "address": "1865 Springfield Ave, Maplewood, NJ 07040",
        "phone": "(973) 996-1420",
        "website": "https://apothecarium.com",
        "storefront_url": "https://apothecarium.com/locations/maplewood",
    },
    "The Apothecarium New Jersey (Phillipsburg)": {
        "address": "55 S Main St, Phillipsburg, NJ 08865",
        "phone": "(908) 777-7420",
        "website": "https://apothecarium.com",
        "storefront_url": "https://apothecarium.com/locations/phillipsburg",
    },
    "AYR Wellness NJ (Eatontown)": {
        "address": "59 Main Street, Eatontown, NJ 07724",
        "phone": "(848) 999-2005",
        "website": "https://ayrdispensaries.com",
        "storefront_url": "https://ayrdispensaries.com/dispensaries/new-jersey/eatontown",
    },
    "AYR Wellness NJ (Union)": {
        "address": "2536 US Highway 22, Union, NJ 07083",
        "phone": "(908) 999-2005",
        "website": "https://ayrdispensaries.com",
        "storefront_url": "https://ayrdispensaries.com/dispensaries/new-jersey/union",
    },
    "AYR Wellness NJ (Woodbridge)": {
        "address": "950 US Highway 1 N, Woodbridge, NJ 07095",
        "phone": "(732) 999-2005",
        "website": "https://ayrdispensaries.com",
        "storefront_url": "https://ayrdispensaries.com/dispensaries/new-jersey/woodbridge",
    },
    "Rise New Jersey (Bloomfield)": {
        "address": "26-48 Bloomfield Ave, Bloomfield, NJ 07003",
        "phone": "(973) 327-3442",
        "website": "https://risecannabis.com",
        "storefront_url": "https://risecannabis.com/dispensaries/new-jersey/bloomfield",
    },
    "Rise New Jersey (Paramus)": {
        "address": "145 NJ-4, Paramus, NJ 07652",
        "phone": "(973) 996-4570",
        "website": "https://risecannabis.com",
        "storefront_url": "https://risecannabis.com/dispensaries/new-jersey/paramus",
    },
    "Rise New Jersey (Paterson)": {
        "address": "196 3rd Ave, Paterson, NJ 07514",
        "phone": "(973) 440-2717",
        "website": "https://risecannabis.com",
        "storefront_url": "https://risecannabis.com/dispensaries/new-jersey/paterson",
    },
    "The Botanist NJ (Collingswood)": {
        "address": "35 E Crescent Blvd, Camden, NJ 08103",
        "phone": "(856) 478-3530",
        "website": "https://shopbotanist.com",
        "storefront_url": "https://shopbotanist.com/stores/collingswood-rec-menu",
    },
    "The Botanist NJ (Egg Harbor Township)": {
        "address": "100 Century Dr, Egg Harbor Township, NJ 08234",
        "phone": "(609) 257-4444",
        "website": "https://shopbotanist.com",
        "storefront_url": "https://shopbotanist.com/stores/egg-harbor-rec-menu",
    },
    "The Botanist NJ (Williamstown)": {
        "address": "2090 N Black Horse Pike, Williamstown, NJ 08094",
        "phone": "(856) 478-3530",
        "website": "https://shopbotanist.com",
        "storefront_url": "https://shopbotanist.com/stores/williamstown-rec-menu",
    },
    "Bloc NJ (Ewing)": {
        "address": "1761 N Olden Ave, Ewing Township, NJ 08638",
        "phone": "(973) 494-8499",
        "website": "https://blocdispensary.com",
        "storefront_url": "https://store-ewing.blocdispensary.com",
    },
    "Bloc NJ (Waretown)": {
        "address": "501 US-9, Waretown, NJ 08758",
        "phone": "(973) 494-8550",
        "website": "https://blocdispensary.com",
        "storefront_url": "https://store-waretown.blocdispensary.com",
    },
    "MPX New Jersey (Atlantic City)": {
        "address": "124 St James Pl, Atlantic City, NJ 08401",
        "phone": "(609) 616-7770",
        "website": "https://mpxnj.com",
        "storefront_url": "https://mpxnj.com/stores/mpx-new-jersey-atlantic-city-rec",
    },
    "MPX New Jersey (Gloucester)": {
        "address": "581 Berlin-Cross Keys Rd, Gloucester Township, NJ 08012",
        "phone": "(856) 227-0000",
        "website": "https://mpxnj.com",
        "storefront_url": "https://mpxnj.com/stores/mpx-new-jersey-gloucester-township-rec",
    },
    "MPX New Jersey (Pennsken)": {
        "address": "5035 Central Hwy, Pennsauken, NJ 08109",
        "phone": "(856) 665-0000",
        "website": "https://mpxnj.com",
        "storefront_url": "https://mpxnj.com/stores/mpx-new-jersey-pennsauken-rec",
    },
    "MPX (Pennsauken)": {
        "address": "5035 Central Hwy, Pennsauken, NJ 08109",
        "phone": "(856) 665-0000",
        "website": "https://mpxnj.com",
        "storefront_url": "https://mpxnj.com/stores/mpx-new-jersey-pennsauken-rec",
    },
    "MPX NJ": {  # Generic - use Pennsauken
        "address": "5035 Central Hwy, Pennsauken, NJ 08109",
        "phone": "(856) 665-0000",
        "website": "https://mpxnj.com",
        "storefront_url": "https://mpxnj.com/stores/mpx-new-jersey-pennsauken-rec",
    },
    "MPX NJ (Gloucester Township)": {
        "address": "581 Berlin-Cross Keys Rd, Gloucester Township, NJ 08012",
        "phone": "(856) 227-0000",
        "website": "https://mpxnj.com",
        "storefront_url": "https://mpxnj.com/stores/mpx-new-jersey-gloucester-township-rec",
    },
    "MPX": {  # Generic
        "address": "124 St James Pl, Atlantic City, NJ 08401",
        "phone": "(609) 616-7770",
        "website": "https://mpxnj.com",
        "storefront_url": "https://mpxnj.com/stores/mpx-new-jersey-atlantic-city-rec",
    },
    "NJ Leaf (Aberdeeen)": {
        "address": "369 Rt 35 S, Cliffwood, NJ 07721",
        "phone": "(732) 894-4200",
        "website": "https://njleaf.com",
        "storefront_url": "https://njleaf.com/location/aberdeen-nj",
    },
    "NJ Leaf (Freehold)": {
        "address": "546 Park Ave, Freehold, NJ 07728",
        "phone": "(732) 204-7172",
        "website": "https://njleaf.com",
        "storefront_url": "https://njleaf.com/location/freehold-nj",
    },
    "NJ Leaf (Keansburg)": {
        "address": "77 Rt 36, Keansburg, NJ 07734",
        "phone": "(908) 936-7930",
        "website": "https://njleaf.com",
        "storefront_url": "https://njleaf.com/location/keansburg-nj",
    },
    "NJ Leaf (Nj Leaf North Brunswick)": {
        "address": "1345 US-1, North Brunswick, NJ 08902",
        "phone": "(201) 574-8060",
        "website": "https://njleaf.com",
        "storefront_url": "https://njleaf.com/location/north-brunswick-nj",
    },
    # East Coasting is listed under Ascend's page in Eatontown
    "East Coasting (Eatontown)": {
        "address": "178 Highway 35, Eatontown, NJ 07724",
        "phone": "(732) 475-2186",
        "website": "https://letsascend.com",
        "storefront_url": "https://letsascend.com/locations/new-jersey/eatontown",
    },
    "Mister Jones (Little Falls)": {
        "address": "655 US 46 East, Little Falls, NJ 07424",
        "phone": "(973) 638-2454",
        "website": "https://letsascend.com",
        "storefront_url": "https://letsascend.com/locations/new-jersey/little-falls",
    },
}

# Standardize city names
CITY_CORRECTIONS = {
    "Mt Lrel": "Mount Laurel",
    "Runnee": "Runnemede",
    "Mt Ephraim": "Mount Ephraim",
    "Nj Leaf North Brunswick": "North Brunswick",
    "Pennsken": "Pennsauken",
    "Vorhees": "Voorhees",
    "Aberdeeen": "Aberdeen",
}

def extract_city_from_name(name):
    """Extract city from store name like 'Store Name (City)'"""
    m = re.search(r'\(([^)]+)\)', name)
    if m:
        city = m.group(1).strip()
        # Apply corrections
        return CITY_CORRECTIONS.get(city, city)
    return None


def simple_search(query, retries=2):
    """Use urllib to search using DuckDuckGo lite"""
    import urllib.request
    import urllib.parse
    
    encoded = urllib.parse.urlencode({"q": query})
    url = f"https://lite.duckduckgo.com/lite/?{encoded}"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
    }
    
    for attempt in range(retries):
        try:
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=15) as resp:
                html = resp.read().decode("utf-8", errors="replace")
                # Extract result links
                results = re.findall(r'<a[^>]*href="(https?://[^"]+)"[^>]*class="result-link"[^>]*>(.*?)</a>', html, re.DOTALL)
                snippets = re.findall(r'<td class="result-snippet">(.*?)</td>', html, re.DOTALL)
                
                combined = []
                for i, (url, title) in enumerate(results):
                    snippet = snippets[i] if i < len(snippets) else ""
                    combined.append({
                        "url": url,
                        "title": re.sub(r'<[^>]+>', '', title).strip(),
                        "snippet": re.sub(r'<[^>]+>', '', snippet).strip()
                    })
                return combined
        except Exception as e:
            if attempt < retries - 1:
                time.sleep(1)
            else:
                return []
    return []


def extract_info_from_results(results, store_name, city=None):
    """Try to extract address, phone, website from search results"""
    info = {
        "address": None,
        "phone": None,
        "website": None,
        "storefront_url": None,
        "found_on": None
    }
    
    all_text = " ".join(r["snippet"] + " " + r["title"] for r in results)
    all_urls = [r["url"] for r in results]
    
    # Try to find address (contains NJ and looks like a street address)
    address_patterns = [
        r'(\d+\s+[A-Za-z0-9\s,]+(?:Ave|Street|St|Road|Rd|Boulevard|Blvd|Drive|Dr|Lane|Ln|Way|Court|Ct|Place|Pl|Highway|Hwy|Route|Rt)\s*[,.]?\s*[A-Za-z\s]+,\s*NJ\s*\d{5})',
        r'(\d+\s+[A-Za-z0-9\s,.]+(?:Ave|Street|St|Road|Rd|Boulevard|Blvd|Drive|Dr|Lane|Ln|Way|Court|Ct|Place|Pl|Highway|Hwy|Route|Rt)[^,]*,\s*NJ)',
    ]
    
    for pattern in address_patterns:
        m = re.search(pattern, all_text, re.IGNORECASE)
        if m:
            addr = m.group(1).strip()
            # Clean up
            addr = re.sub(r'\s+', ' ', addr)
            info["address"] = addr
            break
    
    # Find phone number
    phone_pattern = r'(\(?\d{3}\)?[\s.-]?\d{3}[\s.-]?\d{4})'
    phone_matches = re.findall(phone_pattern, all_text)
    for p in phone_matches:
        if len(p) >= 10:
            info["phone"] = p
            break
    
    # Find website (most common domain from results)
    weedmaps_url = None
    leafly_url = None
    duchy_url = None
    
    for url in all_urls:
        if "weedmaps.com" in url and ("dispensary" in url or "/menu" in url):
            weedmaps_url = url
        if "leafly.com" in url:
            leafly_url = url
        # Check for ordering/menu pages
        if any(x in url.lower() for x in ["/menu", "/shop", "/order", "/stores/", "/online-ordering", "storefront"]):
            if not info["storefront_url"]:
                info["storefront_url"] = url
    
    # Use weedmaps or leafly as storefront if found
    if weedmaps_url and not info["storefront_url"]:
        info["storefront_url"] = weedmaps_url
    elif leafly_url and not info["storefront_url"]:
        info["storefront_url"] = leafly_url
    
    return info


def main():
    results = []
    
    for store_name in store_names:
        if store_name in existing:
            print(f"  ✓ Already have: {store_name}")
            results.append(existing[store_name])
            continue
        
        # Check chain data
        if store_name in CHAIN_DATA:
            cd = CHAIN_DATA[store_name]
            print(f"  ✓ Chain data: {store_name}")
            entry = {
                "name": store_name,
                "address": cd["address"],
                "phone": cd["phone"],
                "website": cd["website"],
                "storefront_url": cd["storefront_url"],
                "lat": None,
                "lon": None,
                "google_place_id": None,
                "source": "chain_data"
            }
            results.append(entry)
            existing[store_name] = entry
            continue
        
        city = extract_city_from_name(store_name)
        # Clean up store name for search
        search_name = re.sub(r'\s*\([^)]*\)\s*', '', store_name).strip()
        
        if city:
            search_query = f"{search_name} {city} New Jersey dispensary address phone"
        else:
            search_query = f"{search_name} New Jersey dispensary address phone"
        
        print(f"  ~ Searching: {store_name}")
        time.sleep(0.5)  # Rate limiting
        
        search_results = simple_search(search_query)
        
        if not search_results:
            # Try alternative search
            if city:
                alt_query = f"{search_name} {city} NJ cannabis"
            else:
                alt_query = f"{search_name} NJ cannabis dispensary"
            time.sleep(0.5)
            search_results = simple_search(alt_query)
        
        info = extract_info_from_results(search_results, store_name, city)
        
        # Try to get weedmaps or online ordering link
        if city and not info["storefront_url"]:
            wm_query = f"{search_name} {city} NJ weedmaps online ordering"
            time.sleep(0.5)
            wm_results = simple_search(wm_query)
            for r in wm_results:
                url = r["url"]
                if "weedmaps.com" in url or "leafly.com" in url or "dutchie.com" in url or "/menu" in url.lower() or "/shop" in url.lower():
                    info["storefront_url"] = url
                    break
        
        # Determine best website URL
        website = None
        if search_results:
            for r in search_results[:5]:
                url = r["url"]
                # Skip social media, maps, review sites
                if any(x in url for x in ["facebook.com", "instagram.com", "yelp.com", "google.com/maps"]):
                    continue
                if any(x in url for x in ["weedmaps.com", "leafly.com"]):
                    continue
                website = url
                break
        
        entry = {
            "name": store_name,
            "address": info.get("address"),
            "phone": info.get("phone"),
            "website": website,
            "storefront_url": info.get("storefront_url"),
            "lat": None,
            "lon": None,
            "google_place_id": None,
            "source": "web_search" if search_results else "not_found"
        }
        
        if info.get("address"):
            print(f"    → Address: {info['address']}")
        else:
            print(f"    → No address found")
        
        results.append(entry)
        existing[store_name] = entry
        
        # Save periodically
        if len(results) % 10 == 0:
            with open(OUTPUT_PATH, 'w') as f:
                json.dump(results, f, indent=2)
            print(f"  [Saved {len(results)}/{len(store_names)}]")
    
    # Final save
    with open(OUTPUT_PATH, 'w') as f:
        json.dump(results, f, indent=2)
    
    # Summary
    with_addr = sum(1 for r in results if r.get("address"))
    with_phone = sum(1 for r in results if r.get("phone"))
    with_website = sum(1 for r in results if r.get("website"))
    with_storefront = sum(1 for r in results if r.get("storefront_url"))
    
    print(f"\n=== Summary ===")
    print(f"Total: {len(results)}")
    print(f"With address: {with_addr}")
    print(f"With phone: {with_phone}")
    print(f"With website: {with_website}")
    print(f"With storefront: {with_storefront}")
    print(f"Saved to: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
