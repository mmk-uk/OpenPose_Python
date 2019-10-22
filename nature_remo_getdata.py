import json
import requests

apikey = "v3mO8ahYZLOw7_lWpAPX6XZ3xvUcAgXQmU_HKi8-SEg.Wfzp5gZGCqBYoV8aUIc7b7p5AEBoLHO350a6FSQgePA"

#Get JSON
headers = {
  'accept': 'application/json',
  'Authorization': 'Bearer ' + apikey ,
}

response = requests.get('https://api.nature.global/1/appliances', headers=headers, verify=False)
rjson = response.json()
jsonText = json.dumps(rjson, indent=4)
print(jsonText)
