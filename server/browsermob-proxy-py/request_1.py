import requests
import json
r = requests.get('https://github.com/timeline.json')
r2 = requests.post("http://httpbin.org/post")
r3 = requests.head("http://httpbin.org/get")

url = 'https://api.github.com/some/endpoint'
payload = {'some': 'data'}
headers = {'content-type': 'application/json'}
r = requests.post(url, data=json.dumps(payload), headers=headers)
r.content
r.headers

url = 'http://httpbin.org/cookies'
cookies = dict(cookies_are='working')
r = requests.get(url, cookies=cookies)
r.text
#r.cookies['example_cookie_name']
r3.status_code ==requests.codes.ok
print(r.text)
pass