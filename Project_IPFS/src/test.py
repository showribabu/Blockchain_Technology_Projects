import ipfsapi

client = ipfsapi.Client('127.0.0.1',5001)
print(client)


response = client.add('./src/images/one.png')
print(response)