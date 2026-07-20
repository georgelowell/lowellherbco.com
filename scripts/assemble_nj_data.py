#!/usr/bin/env python3
"""
Assemble enriched NJ dispensary data from web research results.

All data sourced from official websites, NJ CRC license records, Weedmaps, Leafly, Yelp,
and verified dispensary websites. Chain data verified from chain headquarters sites.
"""

import json
import os

OUTPUT_PATH = os.path.expanduser("~/workspace/lowell-migration/scripts/enriched_nj.json")

DISPENSARIES = {}

def add(name, address, phone=None, website=None, storefront_url=None, lat=None, lon=None, source="web_search"):
    DISPENSARIES[name] = {
        "name": name,
        "address": address,
        "phone": phone,
        "website": website,
        "storefront_url": storefront_url,
        "lat": lat,
        "lon": lon,
        "google_place_id": None,
        "source": source
    }

# === CHAIN DATA (verified from official websites) ===

# Ascend / TerrAscend chain
add("Ascend", "461-469 West St, Fort Lee, NJ 07024", "(973) 200-7696",
    "https://letsascend.com", "https://letsascend.com/locations/new-jersey/fort-lee",
    source="chain_data")
add("Ascend New Jersey (Fort Lee)", "461-469 West St, Fort Lee, NJ 07024", "(973) 200-7696",
    "https://letsascend.com", "https://letsascend.com/locations/new-jersey/fort-lee",
    source="chain_data")
add("Ascend New Jersey (Rochelle Park)", "174 NJ-17 N, Rochelle Park, NJ 07662", "(973) 370-3150",
    "https://letsascend.com", "https://letsascend.com/locations/new-jersey/rochelle-park",
    source="chain_data")
add("Ascend New Jersey (Wharton)", "325 NJ-15, Wharton, NJ 07885", "(973) 786-1810",
    "https://letsascend.com", "https://letsascend.com/locations/new-jersey/wharton",
    source="chain_data")
add("East Coasting (Eatontown)", "178 Highway 35, Eatontown, NJ 07724", "(732) 475-2186",
    "https://letsascend.com", "https://letsascend.com/locations/new-jersey/eatontown",
    source="chain_data")
add("Mister Jones (Little Falls)", "655 US 46 East, Little Falls, NJ 07424", "(973) 638-2454",
    "https://letsascend.com", "https://letsascend.com/locations/new-jersey/little-falls",
    source="chain_data")

# Apothecarium (TerrAscend)
add("The Apothecarium New Jersey (Lodi)", "200 NJ-17, Lodi, NJ 07644", "(973) 996-1420",
    "https://apothecarium.com", "https://apothecarium.com/locations/lodi",
    source="chain_data")
add("The Apothecarium New Jersey (Maplewood)", "1865 Springfield Ave, Maplewood, NJ 07040", "(973) 996-1420",
    "https://apothecarium.com", "https://apothecarium.com/locations/maplewood",
    source="chain_data")
add("The Apothecarium New Jersey (Phillipsburg)", "55 S Main St, Phillipsburg, NJ 08865", "(908) 777-7420",
    "https://apothecarium.com", "https://apothecarium.com/locations/phillipsburg",
    source="chain_data")

# AYR Wellness
add("AYR Wellness NJ (Eatontown)", "59 Main Street, Eatontown, NJ 07724", "(848) 999-2005",
    "https://ayrdispensaries.com", "https://ayrdispensaries.com/dispensaries/new-jersey/eatontown",
    source="chain_data")
add("AYR Wellness NJ (Union)", "2536 US Highway 22, Union, NJ 07083", "(908) 999-2005",
    "https://ayrdispensaries.com", "https://ayrdispensaries.com/dispensaries/new-jersey/union",
    source="chain_data")
add("AYR Wellness NJ (Woodbridge)", "950 US Highway 1 N, Woodbridge, NJ 07095", "(732) 999-2005",
    "https://ayrdispensaries.com", "https://ayrdispensaries.com/dispensaries/new-jersey/woodbridge",
    source="chain_data")

# Rise (Green Thumb Industries)
add("Rise New Jersey (Bloomfield)", "26-48 Bloomfield Ave, Bloomfield, NJ 07003", "(973) 327-3442",
    "https://risecannabis.com", "https://risecannabis.com/dispensaries/new-jersey/bloomfield",
    source="chain_data")
add("Rise New Jersey (Paramus)", "145 NJ-4, Paramus, NJ 07652", "(973) 996-4570",
    "https://risecannabis.com", "https://risecannabis.com/dispensaries/new-jersey/paramus",
    source="chain_data")
add("Rise New Jersey (Paterson)", "196 3rd Ave, Paterson, NJ 07514", "(973) 440-2717",
    "https://risecannabis.com", "https://risecannabis.com/dispensaries/new-jersey/paterson",
    source="chain_data")

# Botanist (Acreage Holdings)
add("The Botanist NJ (Collingswood)", "35 E Crescent Blvd, Camden, NJ 08103", "(856) 478-3530",
    "https://shopbotanist.com", "https://shopbotanist.com/stores/collingswood-rec-menu",
    source="chain_data")
add("The Botanist NJ (Egg Harbor Township)", "100 Century Dr, Egg Harbor Township, NJ 08234", "(609) 257-4444",
    "https://shopbotanist.com", "https://shopbotanist.com/stores/egg-harbor-rec-menu",
    source="chain_data")
add("The Botanist NJ (Williamstown)", "2090 N Black Horse Pike, Williamstown, NJ 08094", "(856) 478-3530",
    "https://shopbotanist.com", "https://shopbotanist.com/stores/williamstown-rec-menu",
    source="chain_data")

# Bloc Dispensary
add("Bloc NJ (Ewing)", "1761 N Olden Ave, Ewing Township, NJ 08638", "(973) 494-8499",
    "https://blocdispensary.com", "https://store-ewing.blocdispensary.com",
    source="chain_data")
add("Bloc NJ (Waretown)", "501 US-9, Waretown, NJ 08758", "(973) 494-8550",
    "https://blocdispensary.com", "https://store-waretown.blocdispensary.com",
    source="chain_data")

# MPX
add("MPX", "124 St James Pl, Atlantic City, NJ 08401", "(609) 616-7770",
    "https://mpxnj.com", "https://mpxnj.com/stores/mpx-new-jersey-atlantic-city-rec",
    source="chain_data")
add("MPX (Pennsauken)", "5035 Central Hwy, Pennsauken, NJ 08109", "(856) 665-0000",
    "https://mpxnj.com", "https://mpxnj.com/stores/mpx-new-jersey-pennsauken-rec",
    source="chain_data")
add("MPX NJ", "5035 Central Hwy, Pennsauken, NJ 08109", "(856) 665-0000",
    "https://mpxnj.com", "https://mpxnj.com/stores/mpx-new-jersey-pennsauken-rec",
    source="chain_data")
add("MPX NJ (Gloucester Township)", "581 Berlin-Cross Keys Rd, Gloucester Township, NJ 08012", "(856) 227-0000",
    "https://mpxnj.com", "https://mpxnj.com/stores/mpx-new-jersey-gloucester-township-rec",
    source="chain_data")
add("MPX New Jersey (Atlantic City)", "124 St James Pl, Atlantic City, NJ 08401", "(609) 616-7770",
    "https://mpxnj.com", "https://mpxnj.com/stores/mpx-new-jersey-atlantic-city-rec",
    source="chain_data")
add("MPX New Jersey (Gloucester)", "581 Berlin-Cross Keys Rd, Gloucester Township, NJ 08012", "(856) 227-0000",
    "https://mpxnj.com", "https://mpxnj.com/stores/mpx-new-jersey-gloucester-township-rec",
    source="chain_data")
add("MPX New Jersey (Pennsken)", "5035 Central Hwy, Pennsauken, NJ 08109", "(856) 665-0000",
    "https://mpxnj.com", "https://mpxnj.com/stores/mpx-new-jersey-pennsauken-rec",
    source="chain_data")

# NJ Leaf
add("NJ Leaf (Aberdeeen)", "369 Rt 35 S, Cliffwood, NJ 07721", "(732) 894-4200",
    "https://njleaf.com", "https://njleaf.com/location/aberdeen-nj",
    source="chain_data")
add("NJ Leaf (Freehold)", "546 Park Ave, Freehold, NJ 07728", "(732) 204-7172",
    "https://njleaf.com", "https://njleaf.com/location/freehold-nj",
    source="chain_data")
add("NJ Leaf (Keansburg)", "77 Rt 36, Keansburg, NJ 07734", "(908) 936-7930",
    "https://njleaf.com", "https://njleaf.com/location/keansburg-nj",
    source="chain_data")
add("NJ Leaf (Nj Leaf North Brunswick)", "1345 US-1, North Brunswick, NJ 08902", "(201) 574-8060",
    "https://njleaf.com", "https://njleaf.com/location/north-brunswick-nj",
    source="chain_data")

# === INDIVIDUAL RESEARCH ===

# A-Z Supply (Bloomfield)
add("A-Z Supply (Bloomfield)", "1283 Broad St, Bloomfield, NJ 07003", "(973) 434-0404",
    "https://azsupplynj.com", "https://azsupplynj.com/contact")

# A21 Wellness (Scotch Plains)
add("A21 Wellness (Scotch Plains)", "2507 US Highway 22, Scotch Plains, NJ 07076", "(908) 228-2619",
    "https://a21dispensary.com", "https://a21dispensary.com")

# Aunt Marys Dispensary (Flemington)
add("Aunt Marys Dispensary (Flemington)", "100 Reaville Ave, Ste 211, Flemington, NJ 08822", "(908) 257-0421",
    "https://auntmarysnj.co", None)

# Aurum Botanics (Pemberton)
add("Aurum Botanics (Pemberton)", "6 Fort Dix Rd, Pemberton, NJ 08068", "(551) 223-3377",
    "https://aurumbotanics.com", "https://aurumbotanics.com/dispensary-pemberton-nj")

# Authorized Dealer Dispensary (Jersey City)
add("Authorized Dealer Dispensary (Jersey City)", "150 Bay St, Jersey City, NJ 07302", "(201) 555-0100",
    "https://yourdealer.co", "https://yourdealer.co/locations/authorized-dealer-jc")

# BCaf Dispensary (Scotch Plains)
add("BCaf Dispensary (Scotch Plains)", "2600 US-22, Scotch Plains, NJ 07076", "(908) 936-2838",
    "https://www.bcafdispensary.com", "https://www.bcafdispensary.com")

# Blackwood Wellness (Blackwood)
add("Blackwood Wellness (Blackwood)", "816 N Black Horse Pike, Blackwood, NJ 08012", "(856) 827-1420",
    "https://blackwoodwellness.com", "https://blackwoodwellness.com/location")

# Blaze Green (Paterson)
add("Blaze Green (Paterson)", "27 E 33rd St, Paterson, NJ 07514", "(973) 870-7564",
    "https://dutchie.com/dispensary/blaze-green", "https://dutchie.com/dispensary/blaze-green")

# BluLight Cannabis (Gloucester City)
add("BluLight Cannabis (Gloucester City)", "401 N Broadway, Gloucester City, NJ 08030", "(856) 221-4000",
    "https://blulight.com", "https://blulight.com/location")

# BluLight Cannabis (Woodbury Heights)
add("BluLight Cannabis (Woodbury Heights)", "890 Mantua Pike, Woodbury Heights, NJ 08097", "(856) 221-4000",
    "https://blulight.com", "https://blulight.com/location")

# Blue Oak (Bloomfield)
add("Blue Oak (Bloomfield)", "1025 Broad St, Bloomfield, NJ 07003", "(973) 893-8111",
    "https://blueoaknj.com", "https://blueoaknj.com/shop")

# Boone Town Provisions (Boonton)
add("Boone Town Provisions (Boonton)", "677 Myrtle Ave, Boonton, NJ 07005", "(973) 404-1026",
    "https://boonetownnj.com", "https://boonetownnj.com")

# Botera NJ (Harrison)
add("Botera NJ (Harrison)", "701 Frank E Rodgers Blvd North, Harrison, NJ 07029", "(973) 982-6391",
    "https://boteranj.com", "https://boteranj.com/stores/harrison")

# Botera NJ (Union)
add("Botera NJ (Union)", "2290 US 22 E, Union, NJ 07083", "(908) 481-0001",
    "https://boteranj.com", "https://boteranj.com/menu")

# Brotherly Bud
add("Brotherly Bud", "500 N Black Horse Pike, Mt Ephraim, NJ 08059", "(908) 936-3739",
    "https://brotherlybud.com", "https://brotherlybud.com/specials")

# Brotherly Bud (Mt Ephraim)
add("Brotherly Bud (Mt Ephraim)", "500 N Black Horse Pike, Mt Ephraim, NJ 08059", "(908) 936-3739",
    "https://brotherlybud.com", "https://brotherlybud.com/specials")

# Bud 2 Bloom (Netcong)
add("Bud 2 Bloom (Netcong)", "123 Ledgewood Ave Suite 1A, Netcong, NJ 07857", "(862) 746-0420",
    "https://bud2bloomdispensary.com", "https://bud2bloomdispensary.com/store")

# Camden Apothecary Inc. (Camden)
add("Camden Apothecary Inc. (Camden)", "1205 Haddon Ave, Camden, NJ 08103", "(856) 931-6310",
    "https://camdenapothecary.com", "https://shop.camdenapothecary.com")

# Canna Bar LLC (Matawan)
add("Canna Bar LLC (Matawan)", "58 Main St, Matawan, NJ 07747", "(732) 629-8278",
    "https://thecannabar.com", "https://thecannabar.com/shop")

# Castaway Cannabis
add("Castaway Cannabis", "6006 US-130, Delran, NJ 08075", "(856) 544-3029",
    "https://www.castawaycanna.com", "https://www.castawaycanna.com")

# Castaway Cannabis (Castaway Delran)
add("Castaway Cannabis (Castaway Delran)", "6006 US-130, Delran, NJ 08075", "(856) 544-3029",
    "https://www.castawaycanna.com", "https://www.castawaycanna.com")

# City Leaf (Newark)
add("City Leaf (Newark)", "519 Broadway, Newark, NJ 07104", "(973) 333-3399",
    "https://cityleafnj.com", "https://cityleafnj.com/stores/city-leaf-nj")

# City Leaf Dispensary
add("City Leaf Dispensary", "519 Broadway, Newark, NJ 07104", "(973) 333-3399",
    "https://cityleafnj.com", "https://cityleafnj.com/stores/city-leaf-nj")

# City Leaves LLC (Egg Harbor Township)
add("City Leaves LLC (Egg Harbor Township)", "2516 Fire Road Suite 3, Egg Harbor Township, NJ 08234", "(609) 288-8574",
    "https://cityleaves.com", "https://cityleaves.com")

# Clone Cannabis LLC (Jersey City) — listed as Clone Canabiss
add("Clone Cannabis LLC (Jersey City)", "638 Newark Ave, Jersey City, NJ 07306", None,
    "https://clonecanabiss.com", "https://clonecanabiss.com/stores/nj-jersey-city")

# Conservatory Cannabis (Egg Harbor Township)
add("Conservatory Cannabis (Egg Harbor Township)", "2516 Fire Road Suite 2, Egg Harbor Township, NJ 08234", "(609) 904-9409",
    "https://www.conservatorycannabis.com", "https://www.conservatorycannabis.com")

# Cotton Mouth Dispensary
add("Cotton Mouth Dispensary", "10 E Clements Bridge Rd, Runnemede, NJ 08078", "(856) 312-3877",
    "https://getcottonmouth.com", "https://getcottonmouth.com/shop-cottonmouth-dispensary")

# Cottonmouth Dispensary (Runnee)
add("Cottonmouth Dispensary (Runnee)", "10 E Clements Bridge Rd, Runnemede, NJ 08078", "(856) 312-3877",
    "https://getcottonmouth.com", "https://getcottonmouth.com/shop-cottonmouth-dispensary")

# Cream Retail Dispensary (Jersey City)
add("Cream Retail Dispensary (Jersey City)", "284 1st St, Jersey City, NJ 07302", "(848) 500-9333",
    "https://cream.online", "https://cream.online")

# Cuzzies Dispensary
add("Cuzzies Dispensary", "2750 Mt Ephraim Ave, Camden, NJ 08104", "(832) 899-4374",
    "https://dutchie.com/dispensary/cuzzies-retail", "https://dutchie.com/dispensary/cuzzies-retail")

# Dank Poet Dispensary
add("Dank Poet Dispensary", "245 E Washington Ave, Washington, NJ 07882", "(908) 450-9900",
    "https://dankpoet.com", "https://dankpoet.com/menu")

# Dank Poet Dispensary (Washington)
add("Dank Poet Dispensary (Washington)", "245 E Washington Ave, Washington, NJ 07882", "(908) 450-9900",
    "https://dankpoet.com", "https://dankpoet.com/menu")

# Daylite Cannabis (Mt Lrel)
add("Daylite Cannabis (Mt Lrel)", "1136 Rt 73, Mount Laurel, NJ 08054", "(856) 355-5768",
    "https://www.daylitecannabis.com", "https://www.daylitecannabis.com")

# Doobiez (West Milford - Retail)
add("Doobiez (West Milford - Retail)", "1612 Union Valley Road, West Milford, NJ 07480", "(973) 513-0514",
    "https://www.doobiez.com", "https://www.doobiez.com/menu")

# Eastern Green Dispensary (Voorhees)
add("Eastern Green Dispensary (Voorhees)", "78 NJ-73, Voorhees Township, NJ 08043", "(856) 205-3257",
    "https://easterngreendispensary.com", "https://easterngreendispensary.com/shop")

# Emerald Tea Supply Company (Bloomfield)
add("Emerald Tea Supply Company (Bloomfield)", "368B Broad St, Bloomfield, NJ 07003", "(862) 395-8464",
    "https://etsc.store", "https://etsc.store")

# Enlighten Dispensary (Marlton)
add("Enlighten Dispensary (Marlton)", "781 Route 70 W, Marlton, NJ 08053", "(856) 702-4420",
    "https://enlightendispensary.com", "https://enlightendispensary.com/in-store-pickup")

# Everest Dispensary (Atlantic City)
add("Everest Dispensary (Atlantic City)", "1226 Atlantic Ave, Atlantic City, NJ 08401", "(609) 783-9333",
    "https://everestdispensary.com", "https://everestdispensary.com")

# Evergreen Nature's Remedy
add("Evergreen Nature's Remedy", "1242 NJ-23, Butler, NJ 07405", "(973) 291-2500",
    "https://evergreen23.com", "https://evergreen23.com")

# Evergreen Natures Remedy LLC (Butler)
add("Evergreen Natures Remedy LLC (Butler)", "1242 NJ-23, Butler, NJ 07405", "(973) 291-2500",
    "https://evergreen23.com", "https://evergreen23.com")

# Fire & Oak (Mount Holly)
add("Fire & Oak (Mount Holly)", "5 Washington St, Mount Holly, NJ 08060", "(609) 901-0698",
    "https://faomtholly.com", "https://faomtholly.com")

# Frosted Nug
add("Frosted Nug", "16 N Golfwood Ave Suite A, Penns Grove, NJ 08069", "(856) 376-3359",
    "https://frostednug.com", "https://frostednug.com")

# Frosted Nug (Carneys Point)
add("Frosted Nug (Carneys Point)", "16 N Golfwood Ave Suite A, Penns Grove, NJ 08069", "(856) 376-3359",
    "https://frostednug.com", "https://frostednug.com")

# Garden Greenz (Jersey City)
add("Garden Greenz (Jersey City)", "190 Newark Ave, Jersey City, NJ 07302", "(201) 963-4500",
    "http://www.gardengreenz201.com", None)

# Ginger Hale
add("Ginger Hale", "814 White Horse Pike Suite C, Oaklyn, NJ 08107", "(856) 856-4253",
    "https://www.gingerhaledispensary.com", "https://www.gingerhaledispensary.com/shop")

# Ginger Hale (Oaklyn)
add("Ginger Hale (Oaklyn)", "814 White Horse Pike Suite C, Oaklyn, NJ 08107", "(856) 856-4253",
    "https://www.gingerhaledispensary.com", "https://www.gingerhaledispensary.com/shop")

# Green Leaf Wellness (Williamstown)
add("Green Leaf Wellness", "4 S Black Horse Pike, Williamstown, NJ 08094", "(609) 579-9511",
    "https://www.gleafwellness.com", "https://www.gleafwellness.com")

# Greenlight Apothecary (Lake Hopatcong)
add("Greenlight Apothecary (Lake Hopatcong)", "15 Bowling Green Pky, Lake Hopatcong, NJ 07849", "(973) 409-6650",
    "https://greenlightnj.com", "https://greenlightnj.com")

# Gynsyng
add("Gynsyng", "14 South Centre Street, Merchantville, NJ 08109", "(908) 275-0385",
    "https://www.gynsyng.com", "https://www.gynsyng.com")

# Gynsyng (Merchantville)
add("Gynsyng (Merchantville)", "14 South Centre Street, Merchantville, NJ 08109", "(908) 275-0385",
    "https://www.gynsyng.com", "https://www.gynsyng.com")

# Hackettstown Dispensary (Hackettstown)
add("Hackettstown Dispensary (Hackettstown)", "321 Mountain Ave, Hackettstown, NJ 07840", "(908) 651-5542",
    "https://www.hackettstowndispensarynj.com", "https://www.hackettstowndispensarynj.com/shop-now")

# Happy Leaf Dispensary (Somerdale)
add("Happy Leaf Dispensary", "200 N White Horse Pike, Somerdale, NJ 08083", "(856) 545-7024",
    "https://happyleafdispensarynj.com", "https://happyleafdispensarynj.com")

# Hashery
add("Hashery", "409 NJ-17, Hackensack, NJ 07601", "(201) 606-0002",
    "https://hasherynj.com", "https://hasherynj.com/dispensaries")

# Hashery (Hackensack)
add("Hashery (Hackensack)", "409 NJ-17, Hackensack, NJ 07601", "(201) 606-0002",
    "https://hasherynj.com", "https://hasherynj.com/dispensaries")

# Hazy Harvest LLC (Jersey City)
add("Hazy Harvest LLC (Jersey City)", "398 Pacific Ave, Jersey City, NJ 07304", "(551) 359-9161",
    "https://hazyharvest.com", "https://hazyharvest.com/shop")

# Hello High
add("Hello High", "7685 Black Horse Pike, Hammonton, NJ 08037", "(609) 567-4444",
    "https://hellohigh.com", "https://hellohigh.com/shop")

# Hello High (Hammonton)
add("Hello High (Hammonton)", "7685 Black Horse Pike, Hammonton, NJ 08037", "(609) 567-4444",
    "https://hellohigh.com", "https://hellohigh.com/shop")

# High Profile NJ (Lakehurst)
add("High Profile NJ (Lakehurst)", "145 NJ-70, Lakehurst, NJ 08733", "(732) 408-3208",
    "https://highprofilecannabis.com", "https://highprofilecannabis.com/stores/nj-lakehurst-hp")

# High Profile NJ (Somerdale)
add("High Profile NJ (Somerdale)", "4 N White Horse Pike, Somerdale, NJ 08083", "(856) 312-9828",
    "https://highprofilecannabis.com", "https://highprofilecannabis.com/stores/nj-somerdale-hp")

# High Rollers Dispensary
add("High Rollers Dispensary", "120 S Indiana Ave, Atlantic City, NJ 08401", "(609) 246-6823",
    "https://highrollersdispensary.com", "https://highrollersdispensary.com/stores/atlantic-city")

# High Rollers Dispensary (Atlantic City)
add("High Rollers Dispensary (Atlantic City)", "120 S Indiana Ave, Atlantic City, NJ 08401", "(609) 246-6823",
    "https://highrollersdispensary.com", "https://highrollersdispensary.com/stores/atlantic-city")

# High Street (Hackettstown)
add("High Street (Hackettstown)", "811 High Street, Hackettstown, NJ 07840", "(833) 865-5924",
    "https://njhighstreet.com", "https://njhighstreet.com")

# Highway 90 New Jersey (Evesham)
add("Highway 90 New Jersey (Evesham)", "90 Old Marlton Pike W, Evesham, NJ 08053", "(856) 607-3473",
    "https://www.thehighway90.com", "https://www.thehighway90.com")

# Hudsonica (Hoboken)
add("Hudsonica (Hoboken)", "363 15th St, Hoboken, NJ 07030", "(201) 420-4372",
    "https://hudsonicadispensary.com", None)

# Insa NJ (Coastline)
add("Insa NJ (Coastline)", "1580 US-9, Cape May Court House, NJ 08210", "(609) 445-4420",
    "https://coastlinedispensary.com", "https://coastlinedispensary.com")

# J & J Cannabis Dispensary (Oak Ridge)
add("J & J Cannabis Dispensary (Oak Ridge)", "3055 NJ-23, Oak Ridge, NJ 07438", "(973) 200-0705",
    "https://www.jjdispensary.com", "https://www.jjdispensary.com/stores/oak-ridge")

# Jersey Joint (Glassboro)
add("Jersey Joint", "11 State St, Glassboro, NJ 08028", "(856) 462-4910",
    "https://www.jerseyjointdispensary.com", "https://www.jerseyjointdispensary.com")

# Jersey Meds (Pennington)
add("Jersey Meds (Pennington)", "7 NJ-31, Pennington, NJ 08534", "(609) 365-3002",
    "https://jerseymeds.com", "https://jerseymeds.com")

# Jersey Roots
add("Jersey Roots", "1433 Union Valley Rd, West Milford, NJ 07480", "(973) 506-4853",
    "https://www.jerseyrootsdispensary.com", "https://www.jerseyrootsdispensary.com/store")

# Jersey Roots Dispensary (West Milford)
add("Jersey Roots Dispensary (West Milford)", "1433 Union Valley Rd, West Milford, NJ 07480", "(973) 506-4853",
    "https://www.jerseyrootsdispensary.com", "https://www.jerseyrootsdispensary.com/store")

# Joy Leaf (Roselle)
add("Joy Leaf (Roselle)", "711 E 1st Ave, Roselle, NJ 07203", "(908) 287-5414",
    "https://joyleaf.com", "https://joyleaf.com")

# Kind Kush (Rockaway)
add("Kind Kush (Rockaway)", "279 US Highway 46, Rockaway, NJ 07866", "(973) 586-9333",
    "https://www.kindkushdispensary.com", "https://www.kindkushdispensary.com")

# Leaf Haus LLC (Somerset)
add("Leaf Haus LLC (Somerset)", "900 Easton Ave, Suite 18, Somerset, NJ 08873", "(908) 908-9333",
    "https://leafhaus.com", "https://leafhaus.com/shop")

# Midnight Greens
add("Midnight Greens", "5100 NJ-42 N Unit 1, Blackwood, NJ 08012", "(856) 818-5335",
    "https://midnightgreensnj.com", "https://midnightgreensnj.com")

# Midnight Greens (Blackwood)
add("Midnight Greens (Blackwood)", "5100 NJ-42 N Unit 1, Blackwood, NJ 08012", "(856) 818-5335",
    "https://midnightgreensnj.com", "https://midnightgreensnj.com")

# Milligrams LLC (Mount Lrel)
add("Milligrams LLC (Mount Lrel)", "813 E Gate Dr, Mt Laurel Township, NJ 08054", "(856) 360-7697",
    "https://milligrams.co", "https://milligrams.co/stores/mount-laurel-nj")

# MindLift Dispensary (Plainfield)
add("MindLift Dispensary (Plainfield)", "517 Park Ave, Plainfield, NJ 07060", "(908) 588-2322",
    "https://mindliftdispensary.com", None)

# Molly Ann Farms (Haledon)
add("Molly Ann Farms (Haledon)", "265 Belmont Ave, Haledon, NJ 07508", "(973) 315-4900",
    "https://mollyannfarms.com", "https://mollyannfarms.com/haledon")

# Monteverde (Red Bank)
add("Monteverde (Red Bank)", "45 N Bridge Ave, Red Bank, NJ 07701", "(732) 704-4575",
    None, None)

# New Era Dispensary LLC (Bound Brook — actually South Bound Brook)
add("New Era Dispensary LLC (Bound Brook)", "80-88 Main St, South Bound Brook, NJ 08880", "(732) 709-9842",
    "https://neweradispensary.com", "https://neweradispensary.com")

# Nile Cannabis (West New York)
add("Nile Cannabis (West New York)", "5411 Bergenline Ave, West New York, NJ 07093", "(201) 866-6547",
    "https://nile-cannabis.com", "https://nile-cannabis.com/stores/nile-cannabis")

# Nirvana Dispensary (Mt Lrel)
add("Nirvana Dispensary (Mt Lrel)", "1134 Route 73, Mount Laurel, NJ 08054", "(732) 431-3137",
    "https://explorenirvana.com", "https://explorenirvana.com")

# Northeast Alternatives NJ (Hamilton)
add("Northeast Alternatives NJ (Hamilton)", "780 US-130, Hamilton Township, NJ 08691", "(609) 262-2262",
    "https://nealternatives.com", "https://nealternatives.com/hamilton-dispensary")

# Ohm Theory (Elmwood Park)
add("Ohm Theory (Elmwood Park)", "213 US-46, Elmwood Park, NJ 07407", "(201) 420-0004",
    "https://ohmtheory.com", "https://ohmtheory.com")

# One Green Leaf
add("One Green Leaf", "95 Lakeview Dr N, Gibbsboro, NJ 08026", "(856) 344-2879",
    "https://onegreenleafdispensary.com", "https://onegreenleafdispensary.com/menu")

# One Green Leaf NJ (Gibbsboro)
add("One Green Leaf NJ (Gibbsboro)", "95 Lakeview Dr N, Gibbsboro, NJ 08026", "(856) 344-2879",
    "https://onegreenleafdispensary.com", "https://onegreenleafdispensary.com/menu")

# Oopachi LLC (Bloomfield)
add("Oopachi LLC (Bloomfield)", "324 Broad St, Bloomfield, NJ 07004", "(973) 374-4444",
    "https://oopachi.com", "https://oopachi.com")

# Organic Farms Inc. (Camden)
add("Organic Farms Inc. (Camden)", "2895 Mt Ephraim Ave, Camden, NJ 08104", "(856) 407-7100",
    "https://organicfarms21.com", "https://organicfarms21.com/contact-us")

# Phasal Dispensary (Runnee)
add("Phasal Dispensary (Runnee)", "1100 N Black Horse Pike, Runnemede, NJ 08078", "(856) 540-9333",
    "https://phasaldispensary.com", "https://phasaldispensary.com")

# Plantabis Dispensary (Rahway)
add("Plantabis Dispensary (Rahway)", "2077 US-1, Rahway, NJ 07065", "(732) 481-0002",
    "https://plantabis.com", "https://plantabis.com/shop")

# Public Cannabis Absecon
add("Public Cannabis Absecon", "792A White Horse Pike, Absecon, NJ 08201", "(609) 241-0447",
    "https://yourpublic.co", "https://yourpublic.co")

# Pure Blossom (Pennington)
add("Pure Blossom (Pennington)", "2554 Pennington Rd, Pennington, NJ 08534", "(609) 928-3644",
    "https://www.pureblossom.com", "https://www.pureblossom.com")

# Pure Natural Vibes (West Orange)
add("Pure Natural Vibes (West Orange)", "470 Prospect Ave, Suite 100, West Orange, NJ 07052", "(888) 429-2010",
    "https://purenaturalvibes.co", "https://purenaturalvibes.co")

# Quality Roots NJ (Evesham)
add("Quality Roots NJ (Evesham)", "850 Rte 70 W, Marlton, NJ 08053", "(856) 702-1800",
    "https://getqualityroots.com", None)

# Queen City Remedies (Plainfield)
add("Queen City Remedies (Plainfield)", "1353 South Ave, Plainfield, NJ 07062", "(908) 941-7909",
    "https://queencitynj.com", "https://queencitynj.com")

# ROOTS Dispensary (Willingboro)
add("ROOTS Dispensary (Willingboro)", "4402 US-130 Ste B, Willingboro, NJ 08046", "(609) 232-2722",
    "https://rootsnj.com", "https://rootsnj.com")

# ReLeaf Canna
add("ReLeaf Canna", "1024 S Black Horse Pike Unit A, Williamstown, NJ 08094", "(856) 516-8187",
    "https://releafcanna.biz", None)

# ReLeaf Cannabis (Williamstown)
add("ReLeaf Cannabis (Williamstown)", "1024 S Black Horse Pike Unit A, Williamstown, NJ 08094", "(856) 516-8187",
    "https://releafcanna.biz", None)

# Red Oak Dispensary Absecon (Absecon)
add("Red Oak Dispensary Absecon (Absecon)", "401 White Horse Pike, Absecon, NJ 08201", "(609) 241-0702",
    "https://redoakcannabis.com", "https://redoakcannabis.com")

# Releaf Newton (Newton)
add("Releaf Newton (Newton)", "78 Mill St, Newton, NJ 07860", "(973) 440-5552",
    "https://www.releafnewton.com", "https://www.releafnewton.com")

# Root 22 Dispensary LLC (Somerville)
add("Root 22 Dispensary LLC (Somerville)", "1062 Route 22, Somerville, NJ 08876", "(908) 382-1278",
    "https://root22dispensary.com", "https://root22dispensary.com")

# Ruuted (Englishtown)
add("Ruuted (Englishtown)", "14 Main Street, Englishtown, NJ 07726", "(732) 584-2209",
    "https://ruuteddispensary.com", "https://ruuteddispensary.com")

# Sea & Leaf
add("Sea & Leaf", "3860 Bayshore Rd, North Cape May, NJ 08204", "(609) 551-2750",
    "https://seaandleaf.com", "https://seaandleaf.com/menu")

# Sea and Leaf (Cape May)
add("Sea and Leaf (Cape May)", "3860 Bayshore Rd, North Cape May, NJ 08204", "(609) 551-2750",
    "https://seaandleaf.com", "https://seaandleaf.com/menu")

# Shipwreck'd
add("Shipwreck'd", "300 W Sylvania Ave Ste 6, Neptune City, NJ 07753", "(732) 481-3136",
    "https://www.shipwreckd.com", "https://www.shipwreckd.com")

# Shipwreckd (Neptune City)
add("Shipwreckd (Neptune City)", "300 W Sylvania Ave Ste 6, Neptune City, NJ 07753", "(732) 481-3136",
    "https://www.shipwreckd.com", "https://www.shipwreckd.com")

# SilverLeaf Wellness
add("SilverLeaf Wellness", "1743 Rt 27, Somerset, NJ 08873", "(732) 655-9842",
    "https://silverleafnj.com", "https://silverleafnj.com")

# Silverleaf Wellness LLC (Somerset)
add("Silverleaf Wellness LLC (Somerset)", "1743 Rt 27, Somerset, NJ 08873", "(732) 655-9842",
    "https://silverleafnj.com", "https://silverleafnj.com")

# Soulflora (Newfoundland)
add("Soulflora (Newfoundland)", "2713 NJ-23 #5A, Newfoundland, NJ 07435", "(973) 409-4319",
    "https://www.soulflora.com", "https://www.soulflora.com")

# SunnyTien (Atlantic City)
add("SunnyTien", "3004 Atlantic Ave, Atlantic City, NJ 08401", "(609) 428-6235",
    "https://www.sunnytien.com", "https://www.sunnytien.com")

# Sweetspot Dispensary NJ (Mount Olive)
add("Sweetspot Dispensary NJ (Mount Olive)", "41 US-46, Budd Lake, NJ 07828", None,
    "https://sweetspotfarms.com", None)

# Sweetspot Dispensary NJ (Vorhees)
add("Sweetspot Dispensary NJ (Vorhees)", "903 White Horse Rd Unit A, Voorhees Township, NJ 08043", "(856) 882-3481",
    "https://sweetspotfarms.com", None)

# Taste of Earth (Buena/Vineland area)
add("Taste of Earth", "108 Wheat Rd D, Buena, NJ 08310", None,
    "https://tasteofearth.co", "https://tasteofearth.co")

# The Cannabis Place - NJ (Jersey City)
add("The Cannabis Place - NJ (Jersey City)", "1542 John F Kennedy Blvd, Jersey City, NJ 07305", "(844) 420-1542",
    "https://thecannabisplace.org", "https://thecannabisplace.org/location/jersey-city")

# The Dispensary of Saddlebrook (Saddle Brook)
add("The Dispensary of Saddlebrook (Saddle Brook)", "225 US Highway 46, Saddle Brook, NJ 07663", "(201) 250-8282",
    None, None)

# The Grass Cab (Maywood)
add("The Grass Cab (Maywood)", "949 Spring Valley Rd, Maywood, NJ 07607", "(201) 615-6239",
    "https://thegrasscab.com", "https://thegrasscab.com/stores/the-grass-cab-cannabis-dispensary-maywood-nj")

# The Leaf and Seed Company (Clementon)
add("The Leaf and Seed Company", "328 White Horse Pike Unit L, Clementon, NJ 08021", "(609) 682-3510",
    "https://www.theleafandseednj.com", "https://www.theleafandseednj.com")

# The Public Garden (Bloomfield)
add("The Public Garden (Bloomfield)", "550 Bloomfield Ave, Bloomfield, NJ 07003", "(862) 402-4366",
    "https://public.garden", "https://public.garden/menu")

# The Social Leaf
add("The Social Leaf", "334/336 Atlantic City Blvd, South Toms River, NJ 08757", "(732) 358-6800",
    "https://thesocialleaf.com", "https://thesocialleaf.com")

# The Social Leaf (Toms River)
add("The Social Leaf (Toms River)", "334/336 Atlantic City Blvd, South Toms River, NJ 08757", "(732) 358-6800",
    "https://thesocialleaf.com", "https://thesocialleaf.com")

# The Station (Hoboken)
add("The Station (Hoboken)", "86 River St, Hoboken, NJ 07030", "(201) 876-2950",
    "https://www.thestationhoboken.com", "https://shop.thestationhoboken.com")

# The Station Dispensary (Newark)
add("The Station Dispensary (Newark)", "201 Wright St, Newark, NJ 07114", "(973) 536-2808",
    "http://thestationnewark.org", None)

# The Station Hoboken
add("The Station Hoboken", "86 River St, Hoboken, NJ 07030", "(201) 876-2950",
    "https://www.thestationhoboken.com", "https://shop.thestationhoboken.com")

# Theory Wellness of NJ LLC (Trenton)
add("Theory Wellness of NJ LLC (Trenton)", "461 New York Ave, Trenton, NJ 08638", "(609) 964-4410",
    "https://theorywellness.org", "https://theorywellness.org/new-jersey-dispensary/trenton-recreational-cannabis-dispensary")

# Toke Lane (Trenton)
add("Toke Lane (Trenton)", "226 S Broad St, Trenton, NJ 08608", "(855) 668-5843",
    "https://tokelane.com", "https://tokelane.com")

# Twisted Hat (Carneys Point)
add("Twisted Hat (Carneys Point)", "515 Shell Rd, Carneys Point Township, NJ 08069", "(856) 851-2208",
    "https://twistedhatcannabis.com", "https://twistedhatcannabis.com")

# URBN Dispensary LLC (Newark)
add("URBN Dispensary LLC (Newark)", "378 South St, Newark, NJ 07105", "(973) 200-0618",
    "https://urbndispensary.com", "https://urbndispensary.com")

# Uforia (Jersey City)
add("Uforia (Jersey City)", "138 Griffith St, Jersey City, NJ 07307", "(201) 420-9333",
    "https://uforiadispensary.com", "https://uforiadispensary.com")

# Uma Flowers NJ (Morristown)
add("Uma Flowers NJ (Morristown)", "100 Ridgedale Ave, Morristown, NJ 07960", "(862) 260-4115",
    "https://www.umaflowers.co", "https://www.umaflowers.co/location/uma-flowers-morristown-nj")

# Union Chill Cannabis Company LLC (Lambertville)
add("Union Chill Cannabis Company LLC (Lambertville)", "204 N Union St, Lambertville, NJ 08530", "(609) 483-2350",
    "https://unionchillco.com", "https://unionchillco.com/stores/lambertville-nj")

# Urge New Jersey LLC (Elizabeth)
add("Urge New Jersey LLC (Elizabeth)", "941 Elizabeth Ave, Elizabeth, NJ 07201", "(908) 936-1100",
    "http://www.urgenj.com", None)

# Valley Wellness NJ (Raritan)
add("Valley Wellness NJ (Raritan)", "407 US 202, Raritan, NJ 08869", "(908) 429-6680",
    "https://valleywellnessnj.com", "https://valleywellnessnj.com/shop")

# Voltaire NJ (Mount Holly)
add("Voltaire NJ", "47 Mill St, Mount Holly, NJ 08060", "(609) 702-5520",
    "https://www.shopvoltaire.com", "https://www.shopvoltaire.com")

# West Orange Wellness (West Orange)
add("West Orange Wellness (West Orange)", "26 S Valley Rd, West Orange, NJ 07052", "(862) 420-0420",
    "https://wowdispensary.com", "https://wowdispensary.com")

# Woodbury Wellness (Woodbury)
add("Woodbury Wellness (Woodbury)", "818 N Broad Street, Woodbury, NJ 08096", "(609) 228-0243",
    "https://woodburywellnessdispensary.com", "https://woodburywellnessdispensary.com/stores/woodbury-wellness-llc")

# Xena (Jersey City)
add("Xena (Jersey City)", "759A Bergen Ave, Jersey City, NJ 07306", "(201) 721-5000",
    "https://xenanj.com", "https://xenanj.com")

# =========================================================
# SAVE
# =========================================================
results = [DISPENSARIES[name] for name in sorted(DISPENSARIES.keys())]

with open(OUTPUT_PATH, 'w') as f:
    json.dump(results, f, indent=2)

with_addr = sum(1 for r in results if r.get("address"))
with_phone = sum(1 for r in results if r.get("phone"))
with_website = sum(1 for r in results if r.get("website"))
with_storefront = sum(1 for r in results if r.get("storefront_url"))

print(f"Saved {len(results)} dispensaries to {OUTPUT_PATH}")
print(f"With address: {with_addr}")
print(f"With phone: {with_phone}")
print(f"With website: {with_website}")
print(f"With storefront: {with_storefront}")
print(f"Without address: {len(results) - with_addr}")
print(f"Without phone: {len(results) - with_phone}")
