import re 
#data = ws.newegg_scrapper()[5].get('description')
#data = 'G.SKILL Flare X Series 64GB (2 x 32GB) 288-Pin PC RAM DDR5 6000 (PC5 48000) Desktop Memory Model F5-6000J3040G32GX2-FX5'
#print(data) all this was for testing
def normalizer(data, price, source):
    #ram quantity
    reg_ex = r'(\d{1,3})GB'
    ram_quantity = re.findall(reg_ex, data)

    #type of ram 
    reg_ex2 = r'DDR[45]'
    ram_type = re.findall(reg_ex2, data)

    #speed of ram 
    reg_ex3 = r'DDR[45]\s(\d{4})'
    ram_speed = re.findall(reg_ex3, data)
    if not ram_speed:
        reg_ex3_1 = r'(\d{4})MHz'
        ram_speed = re.findall(reg_ex3_1, data)
    if not ram_speed:
        reg_ex3_2 = r'(\d{4})MT/s'
        ram_speed = re.findall(reg_ex3_2, data)

    #ram brand
    RAM_BRANDS = {
        "Corsair": [
            r"corsair"
        ],
        "Kingston": [
            r"kingston"
        ],
        "G.Skill": [
            r"g\.?skill",
            r"g\s*skill"
        ],
        "Crucial": [
            r"crucial"
        ],
        "TeamGroup": [
            r"team\s*group",
            r"teamgroup"
        ],
        "Patriot": [
            r"patriot"
        ],
        "ADATA": [
            r"adata"
        ],
        "Thermaltake": [
            r"thermaltake"
        ],
        "PNY": [
            r"\bpny\b"
        ],
        "Silicon Power": [
            r"silicon\s*power"
        ],
        "Samsung": [
            r"samsung"
        ],
        'KingBank': [
            r'KingBank',
            r'King\s*Bank'
        ]
    }
    ram_brand = []
    for i in RAM_BRANDS: 
        ram_lists = RAM_BRANDS.get(i) #getting the lists that contain the regex expressions for the brands
        for x in ram_lists:
            brand = x
            result = re.search(brand, data, flags=re.IGNORECASE) #we search while iterating through the lists
            if result == None:
                continue
            else:
                ram_brand = [i]
                break
        if ram_brand:
            break #only if there is something inside the match it breaks
    if not ram_brand:
        ram_brand.append('Other Brands') #in case the brand in the listing does not appear on the list of brands
    return {'Ram Quantity':ram_quantity, 'Ram Type':ram_type, 'Ram Speed':ram_speed, 'Ram Brand':ram_brand, 'Original String': data, 'Price':price, 'Source': source}

