# github.com/xyele

import requests,json,sys
from threading import Thread
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

domain = sys.argv[1]
urls = []

def request(req):
	return requests.get(req, verify=False,allow_redirects=False).text
	pass

def fix(url):
	if "?" in url:
		url = url.split("?")[0]
		pass
	if "#" in url:
		url = url.split("#")[0]
		pass
	return url
	pass

def getWayback():
	response = request("https://web.archive.org/cdx/search/cdx?url=*.{}/*&output=json&collapse=urlkey".format(domain))
	response = json.loads(response)
	[urls.append(fix(i[2])) for i in response]
	pass

def getOtx():
	response = request("https://otx.alienvault.com/api/v1/indicators/hostname/*.{}/url_list?page=00".format(domain))
	response = json.loads(response)
	[urls.append(fix(i["url"])) for i in response["url_list"]]
	pass

def getCommoncrawl():
	getDB = json.loads(request("https://index.commoncrawl.org/collinfo.json"))
	getDB = [getDB[0]["cdx-api"],getDB[1]["cdx-api"],getDB[2]["cdx-api"]]
	[[urls.append(fix(json.loads(x)["url"])) for x in request(i+"?url=*.{}/*&output=json".format(domain)).split("\n")[:-1]] for i in getDB]
	pass

myThreads = [Thread(target = getWayback),Thread(target = getOtx),Thread(target = getCommoncrawl)]
[i.start() for i in myThreads]
[i.join() for i in myThreads]
print("\n".join(list(dict.fromkeys(urls))))
