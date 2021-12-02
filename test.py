import requests

def __init__():
	url = "http://api.uomg.com/api/rand.music"
	req = requests.get(url, "sort=热歌榜&format=json")
	print(req.text)

if __name__ == "__main__":
	__init__()