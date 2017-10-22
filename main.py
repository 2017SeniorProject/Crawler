import urllib.parse
import requests
import json


class PlaceSearch:
    def __init__(self, location, radius):
        self.location = location
        self.radius = radius
        self.query = ''
        self.keyword = ''
        self.url = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json'
        self.language = 'zh-tw'
        self.ptoken = ''
        self.key = 'AIzaSyAoRFbJMEwjmOQlgfOUi_hwGQbw6KH9FSI'

    def payload(self):
        self.query = '%s?location=%s&keyword=%s&radius=%s&language=%s&key=%s&pagetoken=%s' % (
            self.url, self.location, urllib.parse.quote(self.keyword), self.radius, self.language,
            self.key,
            self.ptoken)
        return self.query

    def set_page_token(self, page_token):
        self.ptoken = page_token

    def set_keyword(self, keyword):
        self.keyword = keyword


PlaceQuery = PlaceSearch('24.814168,121.771705', 5000)
PlaceQuery.set_keyword('餐廳')

# response = requests.get(PlaceQuery.payload())
print(">>>>>>>>>>Debug>>>>>>>>>>")
print(PlaceQuery.payload())
print(">>>>>>>>>>>>>>>>>>>>>>>>>")
# print(response.text)

f = open("data.json")
# print(f.read())
x = json.load(f)  # get json obj

print(x['next_page_token'])
print(len(x['results']))
for index in range(0, len(x['results'])):
    print(x['results'][index])

# x['next_page_token'].test()
# for num in range(1, 10):
#     PlaceQuery.set_page_token(num)
#     print(PlaceQuery.payload())
