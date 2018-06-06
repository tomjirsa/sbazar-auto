import datetime
import urllib.request
import urllib.parse
import json

def get_delta_from_now(date_str):

    date_start = datetime.datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%S")
    date_end = datetime.datetime.now()
    delta = date_end - date_start
    return str(delta)


def get_search_result(search_phrase,config):
    url = "https://www.sbazar.cz/api/v1/items/search?price_from=" \
          + str(config["price_from"]) \
          + "&price_to=" + str(config["price_to"]) \
          + "&category_id=170&phrase=" + urllib.parse.quote(search_phrase) \
          + "&hide_price_by_agreement=true&limit=500"
    print(url)
    search_result = urllib.request.urlopen(url).read().decode('utf-8')
    search_result_json = json.loads(search_result)
    sorted_array = sorted(search_result_json["results"], key=lambda k: (k["create_date"],k["price"]))
    return sorted_array