import pytest
from program.normalizers import normalizer as nz

#happy path for ram quantity and ram type
def test1():
    description = 'Crucial Pro Overclocking 32GB (2 x 16GB) DDR5 6000 (PC5 48000) Desktop Memory Model CP2K16G60C36U5B'
    price = '$399.99–'
    source = 'Newegg'
    test = nz.normalizer(description, price, source)
    assert test.get('Ram Quantity') == ['32', '16']
    assert test.get('Ram Type') == ['DDR5']

#testing the ram speed section
def test2():
    description_1 = 'DDR5 6000'
    description_2 = '6000MHz'
    description_3 = '6000MT/s'
    description_4 = '6000mm'
    price = '$399.99–'
    source = 'Newegg'

    test1 = nz.normalizer(description_1, price, source)
    test2 = nz.normalizer(description_2, price, source)
    test3 = nz.normalizer(description_3, price, source)
    test4 = nz.normalizer(description_4, price, source)

    assert test1.get('Ram Speed') == ['6000']
    assert test2.get('Ram Speed') == ['6000']
    assert test3.get('Ram Speed') == ['6000']
    assert test4.get('Ram Speed') == []

def test3():
    description = [
        "Corsair", "Kingston","G.Skill","Crucial","TeamGroup","Patriot","ADATA",
        "Thermaltake","PNY","Silicon Power","Samsung",'KingBank'
    ]
    price = '$399.99–'
    source = 'Newegg'

    for i in description:
        test = nz.normalizer(i, price, source)
        assert test.get('Ram Brand') == [i]
    test2 = nz.normalizer('random brand', price, source)
    assert test2.get('Ram Brand') == ['Other Brands']

def test4():
    description = 'Crucial Pro Overclocking 32GB (2 x 16GB) DDR5 6000 (PC5 48000) Desktop Memory Model CP2K16G60C36U5B'
    price = '$399.99–'
    source = 'Newegg'

    test = nz.normalizer(description, price, source)
    assert test == {'Ram Quantity': ['32', '16'], 'Ram Type': ['DDR5'], 'Ram Speed': ['6000'], 'Ram Brand': ['Crucial'], 'Original String': 'Crucial Pro Overclocking 32GB (2 x 16GB) DDR5 6000 (PC5 48000) Desktop Memory Model CP2K16G60C36U5B', 'Price': '$399.99–', 'Source': 'Newegg'}