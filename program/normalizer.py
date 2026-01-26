import web_scrapper as ws
import re 

#data = ws.newegg_scrapper()[0].get('description')
data = 'Team Group 16GB (2 x 8GB) 288-Pin PC RAM DDR5 6000 (PC5 48000) Memory Model FF3D516G6000HC38ADC01'
#print(data, type(data))

reg_ex = r'(\d{1,2})GB'
match = re.findall(reg_ex, data)

print(match)