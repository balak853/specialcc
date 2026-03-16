import pymongo

client = pymongo.MongoClient(
"mongodb+srv://balak:Balak12345@cluster0.fdc3y.mongodb.net/?retryWrites=true&w=majority"
)

try:
    client.admin.command("ping")
    print("MONGODB CONNECTED SUCCESSFULLY ✅")
except Exception as e:
    print("MONGODB CONNECTION FAILED ❌", e)

folder = client["BALAK_DATABASE"]

usersdb = folder["USERSDB"]
chats_auth = folder["CHATS_AUTH"]
gcdb = folder["GCDB"]

sksdb = client["SKS_DATABASE"]["SKS"]
confdb = client["SKS_DATABASE"]["CONF_DATABASE"]
