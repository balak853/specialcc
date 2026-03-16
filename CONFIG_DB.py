import pymongo
import dns.resolver

# DNS Resolver set to Google DNS 8.8.8.8
dns.resolver.default_resolver = dns.resolver.Resolver(configure=False)
dns.resolver.default_resolver.nameservers = ["8.8.8.8"]

client = pymongo.MongoClient("mongodb+srv://balak:Balak12345@cluster0.fdc3y.mongodb.net/?retryWrites=true&w=majority")

try:
    client.admin.command("ping")
    print("MONGODB CONNECTED SUCCESSFULLY")
except Exception as e:
    print("MONGODB CONNECTION FAILED", e)
