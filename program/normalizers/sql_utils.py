#this module is to prepare the data for the sql integration 
#class to organize all data for sql
class RAM_object:
    def __init__(self, brand, ram_type, speed, total_gb, modules, gb_per_module, price, source, raw_listing):
        self.brand = brand
        self.ram_type = ram_type
        self.speed = speed
        self.total_gb = total_gb
        self.modules = modules
        self.gb_per_module = gb_per_module
        self.price = price
        self.source = source
        self.raw_listing = raw_listing

#test = {'Ram Quantity': ['32', '16'], 'Ram Type': ['DDR5'], 'Ram Speed': ['6400'], 'Ram Brand': ['Other Brands'], 'Original String': 'V-COLOR Manta XSky DDR5 32GB (2x16GB) 6400MHz CL32 1.4V SK Hynix IC RGB Gaming Desktop Upgrade Memory Module Black, for AMD EXPO TMXSAL1664832KWK', 'Price': '$499.99–', 'Source': 'Newegg'}

#the last normalizer that gives an object ready for sql
def sql_normalizer(ram_dict):
    brand = ram_dict.get('Ram Brand')[0]
    
    ram_type = ram_dict.get('Ram Type')[0]
    
    speed = int(ram_dict.get('Ram Speed')[0])
    
    Quantity_list = ram_dict.get('Ram Quantity')
    total_gb = int(Quantity_list[0])
    modules = ''
    if len(Quantity_list) == 2:
        modules = int(int(Quantity_list[0])/int(Quantity_list[1])) #here i am dividing these numbers as ram quantity is usualy divisible
    else:
        modules = 1
    if modules == 1:
        gb_per_module = None
    else:
        gb_per_module = int(Quantity_list[1])

    Raw_price = ram_dict.get('Price')
    Temp_price = Raw_price.replace('$', '').replace('–', '').replace(',','') #basically just doing it like this to save code and not make it much complicated
    price = float(Temp_price)

    source = ram_dict.get('Source')

    raw_listing = ram_dict.get('Original String')
    return RAM_object(brand, ram_type, speed, total_gb, modules, gb_per_module, price, source, raw_listing)

#test = sql_normalizer(test)
#print(vars(test))