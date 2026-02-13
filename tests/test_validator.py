from program.normalizers import validator as va

#happy path
def test1():
    data = {'Ram Quantity': ['16'], 'Ram Type': ['DDR4'], 'Ram Speed': ['3200'], 'Ram Brand': ['G.Skill'], 'Original String': 'G.SKILL Ripjaws V Series 16GB 288-Pin PC RAM DDR4 3200 (PC4 25600) Desktop Memory Model F4-3200C16S-16GVK', 'Price': '$129.99–', 'Source': 'Newegg'}
    result = va.validator(data)
    assert result == True

#wrong case
def test2():
    data = {'Ram Quantity': ['16'], 'Ram Type': ['DDR4'], 'Ram Speed': [], 'Ram Brand': ['G.Skill'], 'Original String': 'G.SKILL Ripjaws V Series 16GB 288-Pin PC RAM DDR4 3200 (PC4 25600) Desktop Memory Model F4-3200C16S-16GVK', 'Price': '$129.99–', 'Source': 'Newegg'}
    result = va.validator(data)
    assert result == False