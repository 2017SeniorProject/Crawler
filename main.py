import urllib.parse
import requests
import time
import json


class Search:
    def __init__(self):
        self.nearby_url = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json'
        self.detail_url = 'https://maps.googleapis.com/maps/api/place/details/json'
        self.key = 'AIzaSyAoRFbJMEwjmOQlgfOUi_hwGQbw6KH9FSI'
        self.language = 'zh-tw'

    @staticmethod
    def merge(a, b):
        a.update(b)
        print(a)


class NearbySearch(Search):
    def __init__(self, location, radius, keyword):
        super().__init__()
        self.location = location
        self.radius = radius
        self.query = ''
        self.keyword = keyword
        self.page_token = ''

    def set_page_token(self, page_token):
        self.page_token = '&pagetoken=%s' % page_token

    def payload(self):
        self.query = '%s?location=%s&keyword=%s&radius=%s&language=%s&key=%s%s' % (
            self.nearby_url, self.location, urllib.parse.quote(self.keyword), self.radius, self.language,
            self.key,
            self.page_token)
        print('Payload :', self.query)
        return self.query

    # return nearby search json data
    def search(self):
        all_id_list = []
        while True:
            time.sleep(2.5)
            response = requests.get(self.payload())
            data = response.json()
            # print(data)
            if data['status'] == 'OK':
                # Analyze(data).dump_id()
                all_id_list.extend(Analyze(data).dump_id())
                if 'next_page_token' not in data:
                    print('Reached the End')
                    break
                else:
                    print('Page Token >>', data['next_page_token'])
                    self.set_page_token(data['next_page_token'])
                    # return data
            else:
                print(data['status'])
                break
        return all_id_list


class DetailSearch(Search):
    def __init__(self, input_id_list):
        super().__init__()
        self.query = ''
        self.input_id_list = input_id_list
        self.place_id = ''

    def payload(self):
        self.query = '%s?placeid=%s&key=%s&language=%s' % (
            self.detail_url, self.place_id, self.key, self.language)
        print('Payload :', self.query)
        return self.query

    # return detail search json data
    def search(self):
        for self.place_id in self.input_id_list:
            time.sleep(2.5)
            response = requests.get(self.payload())
            json_data = response.json()
            result = json_data['result']
            print(result)
        # return self.output_id_list


# analyze json data
class Analyze:
    def __init__(self, data):
        self.id_list = []
        self.data = data

    # return dict
    def dump_id(self):
        for self._id in self.data['results']:
            print('ID >>', self._id['place_id'])
            self.id_list.append(self._id['place_id'])
        # print('id >>', self.id_list)
        return self.id_list


API_KEY = 'AIzaSyAoRFbJMEwjmOQlgfOUi_hwGQbw6KH9FSI'

print(">>>>>>>>>>Debug>>>>>>>>>>")
#
# nbs = NearbySearch('24.814168,121.771705', 5000, '餐廳').search()
nbs = NearbySearch('24.822370,121.729531', 500, '餐廳').search()

print(DetailSearch(nbs).search())
