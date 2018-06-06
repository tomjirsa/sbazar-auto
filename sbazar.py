import db
import seznamclient
import sbazar_auto

config = {}
config["search_keys"] = ["Touran","Volvo XC90","Seat Alhambra","Ford S-max", "Ford Galaxy", "Peugot 5008", "Opel Zafira"]
#config["search_keys"] = ["xc90"]
config["price_from"] = 80000
config["price_to"] = 250000


database = db.Database("sbazar-auto.sql")
database.createTable("advertisement")

message = """
New records:
"""

for search_phrase in config["search_keys"]:
    message = message + "\n" + search_phrase + "\n"
    sorted_array = sbazar_auto.get_search_result(search_phrase,config)

    for advertisement in sorted_array:
        advert_record = database.create_db_record(advertisement,search_phrase)
        (code, data) = database.insertRecord("advertisement", advert_record)
        if code:
             message = message + str(data["price"]) + "\t" \
                               + data["create_date"] + "\t" \
                               + sbazar_auto.get_delta_from_now(data["create_date"]) + "\t" \
                               + sbazar_auto.get_delta_from_now(data["edit_date"]) + "\t" \
                               + data["name"] + "\t" \
                               + data["url_advert"] + "\n"




table = database.getNewData("advertisement")

print(table)

for record in table:
    print(record)


database.closeConnection()

#print(message)

#seznamclient.send_email_with_records(message,"a@a.com")