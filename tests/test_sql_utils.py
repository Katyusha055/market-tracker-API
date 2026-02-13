from program.normalizers import sql_utils as squ

#happy path/1 module case
def test1():
    data = {'Ram Quantity': ['16'], 'Ram Type': ['DDR4'], 'Ram Speed': ['3200'], 'Ram Brand': ['G.Skill'], 'Original String': 'G.SKILL Ripjaws V Series 16GB 288-Pin PC RAM DDR4 3200 (PC4 25600) Desktop Memory Model F4-3200C16S-16GVK', 'Price': '$129.99–', 'Source': 'Newegg'}
    result = squ.sql_normalizer(data)
    assert result == squ.RamProduct(brand='G.Skill', ram_type='DDR4', speed=3200, total_gb=16, modules=1, gb_per_module=None, price=129.99, source='Newegg', raw_listing='G.SKILL Ripjaws V Series 16GB 288-Pin PC RAM DDR4 3200 (PC4 25600) Desktop Memory Model F4-3200C16S-16GVK')

# 2 modules case
def test2():
    data = {'Ram Quantity': ['32', '16'], 'Ram Type': ['DDR5'], 'Ram Speed': ['6000'], 'Ram Brand': ['Corsair'], 'Original String': 'CORSAIR Vengeance RGB 32GB (2 x 16GB) 288-Pin PC RAM DDR5 6000 (PC5 48000) Desktop Memory Model CMH32GX5M2E6000C36W', 'Price': '$439.99–', 'Source': 'Newegg'}
    result = squ.sql_normalizer(data)
    assert result == squ.RamProduct(brand='Corsair', ram_type='DDR5', speed=6000, total_gb=32, modules=2, gb_per_module=16, price=439.99, source='Newegg', raw_listing='CORSAIR Vengeance RGB 32GB (2 x 16GB) 288-Pin PC RAM DDR5 6000 (PC5 48000) Desktop Memory Model CMH32GX5M2E6000C36W')
