import time
import datetime
import json
import unirest

word = "apple"

url = "https://montanaflynn-dictionary.p.mashape.com/define?word=" + word 

# These code snippets use an open-source library.
response = unirest.get(url,
    headers={
        "X-Mashape-Key": "j6rDcjfVcVmshxp0Y102O2cL6vDrp16mL1FjsnsgRqpcl6fC3L",
        "Accept": "application/json"
    }
)

resp = word + '\n'

data = json.dumps(response.body, separators=(',',':'))
meanings = (json.loads(data))["definitions"]

for meaning in meanings:
    resp = resp + 'm1 : ' + meaning["text"] + '\n\n'
    
print resp
