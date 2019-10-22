import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

apikey = "v3mO8ahYZLOw7_lWpAPX6XZ3xvUcAgXQmU_HKi8-SEg.Wfzp5gZGCqBYoV8aUIc7b7p5AEBoLHO350a6FSQgePA"

#Get JSON
headers = {
  'accept': 'application/json',
  'Authorization': 'Bearer ' + apikey ,
}

#オンオフ
#response = requests.post('https://api.nature.global/1/signals/c0035911-6e5d-43c5-a965-c11dcebcf924/send', headers=headers, verify=False)

#音量上げる
response = requests.post('https://api.nature.global/1/signals/00db0c08-6677-410a-bb65-4f2edc7d47c8/send', headers=headers, verify=False)

#音量下げる
#response = requests.post('https://api.nature.global/1/signals/9ca9ac8e-8739-4dad-9e75-bf1f8a93b597/send', headers=headers, verify=False)
