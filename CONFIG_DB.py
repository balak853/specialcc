import pymongo
import dns.resolver

# DNS resolver set (Google DNS)
dns.resolver.default_resolver = dns.resolver.Resolver(configure=False)
dns.resolver.default_resolver.nameservers = ["8.8.8.8"]

try:
    client = pymongo.MongoClient(
        "mongodb+srv://balak:Balak12345@cluster0.fdc3y.mongodb.net/?retryWrites=true&w=majority"
    )

    client.admin.command("ping")
    print("✅ CONFIG DB CONNECTED SUCCESSFULLY!")

except pymongo.errors.ConnectionFailure as e:
    print("❌ CONFIG DB CONNECTION FAILED:", e)

except Exception as e:
    print("❌ ERROR:", e)
