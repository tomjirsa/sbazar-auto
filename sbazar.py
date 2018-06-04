import urllib.request
import urllib.parse
import json
import db
import hashlib
import seznamclient

search_keys = ["touran","xc90","alhambra","ford s-max", "ford galaxy"]
price_from = 80000
price_to = 250000

advert_record = {"id": "" ,"type": "","create_date": "" ,"price": "","name":"","url_advert": "","url_image":""}

database = db.Database("sbazar-auto.sql")
column_list = ','.join(advert_record.keys())
database.createTable("advertisement", column_list)

message = """
New records:"

"""

for search_phrase in search_keys:
    message = message + "\n" + search_phrase + "\n"
    url = "https://www.sbazar.cz/api/v1/items/search?price_from=" + str(price_from) + "&price_to=" + str(
        price_to) + "&category_id=170&phrase=" + urllib.parse.quote(search_phrase) + "&hide_price_by_agreement=true&limit=200"
    search_result = urllib.request.urlopen(url).read().decode('utf-8')
    search_result_json = json.loads(search_result)
    sorted_array = sorted(search_result_json["results"], key=lambda k: (k["create_date"],k["price"]))

    for advertisement in sorted_array:
        url = "https://www.sbazar.cz/"+ advertisement["user"]["user_service"]["shop_url"] + "/detail/" + advertisement["seo_name"]
        if len( advertisement["images"]) > 0 :
            url_image = "https:" + advertisement["images"][0]["url"] + "?fl=exf|crr,1.33333,2|res,800,600,1|wrm,/watermark/sbazar.png,10,10|jpg,80,,1"
        else:
            url_image = "N/A"

        advert_record["id"] = hashlib.sha256(url.encode()).hexdigest()
        advert_record["type"] = search_phrase
        advert_record["create_date"] = advertisement["create_date"]
        advert_record["price"] = advertisement["price"]
        advert_record["name"] = advertisement["name"]
        advert_record["url_advert"] = url
        advert_record["url_image"] = url_image
        (code, data) = database.insertRecord("advertisement", advert_record)
        if code:
            message = message + str(data["price"]) + "\t\t" + data["name"] + "\t\t url: " + data["url_advert"] + "\n"



table = database.getAllData("advertisement")
table = database.getDataNDaysBack("advertisement", 7)

database.closeConnection()

print(message)

email = seznamclient.Seznam_email()
email.getCredentials()
email.connect()
email.sendEmail(message,"a@a.gmail.com")
email.disconnect()