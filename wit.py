import requests
import json 
from urllib.parse import quote

def wit_question(q):
    auth =  {'Authorization' : 'Bearer SV3M5BWQB6L3HQO65HLSTE6SB5DAN7QE'}
    uri = 'https://api.wit.ai/message?v=20220329&q=' + quote(q,safe='/:?=&')

    res = requests.get(uri,headers = auth)
    response = json.loads(res.text)

    return response

wit_question('When was released "Billie Jean" by Michael Jackson ?')