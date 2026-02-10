import logging
def validator(data):
    validate_flag = None
    for i in data:
        validate_flag = None
        if not data.get(i):
            logging.warning(f'Listing skipped as it did not had the {i} data')
            validate_flag = False
            break
        else:
            validate_flag = True
    return validate_flag
        
#test = {'Ram Quantity': ['32'], 'Ram Type': ['DDR5', 'DDR5', 'DDR5'], 'Ram Speed': ['sdsfsd'], 'Ram Brand': ['sdfdsf'], 'Original String': 'Kingston 32GB DDR5 SDRAM Memory Module - For Desktop PC - 32 GB - DDR5-5600/PC5-44800 DDR5 SDRAM - 5600 MHz Dual-rank Memory - CL46 - 1.10 V - Non-ECC - Unbuffered - 288-pin - DIMM- KCP556UD8-32', 'Price': '$438.00–', 'Source': 'Newegg'}
#flag = validator(test)
#print(flag)