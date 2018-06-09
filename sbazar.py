import db
import seznamclient
import sbazar_auto
import json

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




table = database.getDataNDaysBack("advertisement",1)

# list = ""
# for record in table:
#     list = list + json.dumps(record) + ","
#
# html_table = """
# <!DOCTYPE html>
# <html>
# <head>
#     <title>Convert JSON Data to HTML Table</title>
#     <style>
#         table, th, td
#         {
#             margin:10px 0;
#             border:solid 1px #333;
#             padding:2px 4px;
#             font:15px Verdana;
#         }
#         th {
#             font-weight:bold;
#         }
#     </style>
# </head>
# <body>
#     <input type="button" onclick="CreateTableFromJSON()" value="Create Table From JSON" />
#     <div id="showData"></div>
# </body>
#
# <script>
#     function CreateTableFromJSON() {
#         var myBooks = [""" + list + """
#         ]
#
#         // EXTRACT VALUE FOR HTML HEADER.
#         // ('Book ID', 'Book Name', 'Category' and 'Price')
#         var col = [];
#         for (var i = 0; i < myBooks.length; i++) {
#             for (var key in myBooks[i]) {
#                 if (col.indexOf(key) === -1) {
#                     col.push(key);
#                 }
#             }
#         }
#
#         // CREATE DYNAMIC TABLE.
#         var table = document.createElement("table");
#
#         // CREATE HTML TABLE HEADER ROW USING THE EXTRACTED HEADERS ABOVE.
#
#         var tr = table.insertRow(-1);                   // TABLE ROW.
#
#         for (var i = 0; i < col.length; i++) {
#             var th = document.createElement("th");      // TABLE HEADER.
#             th.innerHTML = col[i];
#             tr.appendChild(th);
#         }
#
#         // ADD JSON DATA TO THE TABLE AS ROWS.
#         for (var i = 0; i < myBooks.length; i++) {
#
#             tr = table.insertRow(-1);
#
#             for (var j = 0; j < col.length; j++) {
#                 var tabCell = tr.insertCell(-1);
#                 tabCell.innerHTML = myBooks[i][col[j]];
#             }
#         }
#
#         // FINALLY ADD THE NEWLY CREATED TABLE WITH JSON DATA TO A CONTAINER.
#         var divContainer = document.getElementById("showData");
#         divContainer.innerHTML = "";
#         divContainer.appendChild(table);
#     }
# </script>
# </html>
# """
#
# print(html_table,file=open("output.html", "a"))


database.closeConnection()

#print(message)

#seznamclient.send_email_with_records(message,"a@a.com")