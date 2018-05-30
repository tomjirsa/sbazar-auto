import urllib.request
import json


search_keys = ["touran","xc90"]
price_from = 80000
price_to = 250000


for search_phrase in search_keys:
    url = "https://www.sbazar.cz/api/v1/items/search?price_from=" + str(price_from) + "&price_to=" + str(
        price_to) + "&category_id=170&phrase=" + search_phrase + "&hide_price_by_agreement=true&limit=2000"
    search_result = urllib.request.urlopen(url).read().decode('utf-8')
    search_result_json=json.loads(search_result)
    for advertisement in search_result_json["results"]:
        url = "https://www.sbazar.cz/"+ advertisement["user"]["user_service"]["shop_url"] + "/detail/" + advertisement["seo_name"]
        print(advertisement["create_date"],advertisement["price"], advertisement["name"], url)


