import requests
import os

def setup() :
    auth = requests.auth.HTTPBasicAuth('id','token')
    data = {'grant_type': 'password',
            'username': 'username',
            'password': 'password'}
    headers = {'User-Agent': 'apiname'}
    res = requests.post('https://www.reddit.com/api/v1/access_token',
                        auth=auth, data=data, headers=headers)
    TOKEN = res.json()['access_token']
    headers = {**headers, **{'Authorization': f"bearer {TOKEN}"}}
    requests.get('https://oauth.reddit.com/api/v1/me', headers=headers)
    return headers

headers = setup()

#possible periods hour, day, week, month, year, all

def pull(target,pullAmount,period):
    urls = []
    res = requests.get(f"https://oauth.reddit.com/r/{target}/top",headers=headers,params={'t':period,'limit':pullAmount})
    for p in res.json()['data']['children']:
        try:
            url = p['data']['url']
            title = p['data']['title']
            if(os.path.splitext(url)[1] == ''):
                url = p['data']['media']['reddit_video']['fallback_url'] 
            urls.append((url,title))
        except:
            print("Pull failure")
    return urls
