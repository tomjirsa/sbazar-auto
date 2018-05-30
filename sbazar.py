import urllib.request
import json


search_keys = ["touran","xc90"]
price_from = 80000
price_to = 250000


for search_phrase in search_keys:
    url = "https://www.sbazar.cz/api/v1/items/search?price_from=" + str(price_from) + "&price_to=" + str(
        price_to) + "&category_id=170&phrase=" + search_phrase + "&hide_price_by_agreement=true&limit=2000"
    search_result = urllib.request.urlopen(url).read().decode('utf-8')
    search_result_json = json.loads(search_result)
    sorted_array = sorted(search_result_json["results"], key=lambda k: (k["price"],k["create_date"],))

    for advertisement in sorted_array:
        url = "https://www.sbazar.cz/"+ advertisement["user"]["user_service"]["shop_url"] + "/detail/" + advertisement["seo_name"]
        if len( advertisement["images"]) > 0 :
            url_image = "https:" + advertisement["images"][0]["url"] + "?fl=exf|crr,1.33333,2|res,800,600,1|wrm,/watermark/sbazar.png,10,10|jpg,80,,1"
        else:
            url_image = "N/A"
        print(advertisement["create_date"],advertisement["price"], advertisement["name"], url, url_image)


