import httpx

def resolve(ipfsapi:str,name:str):
    url = ipfsapi+"/api/v0/name/resolve"

    querystring = {"arg":name,"recursive":"true","nocache":"false","dht-record-count":"16","dht-timeout":"1m0s"}

    response = httpx.post(url, params=querystring)

    return response.json()

#8640h=360day
def publish(ipfsapi:str,cid:str,keyname:str,lifetime:str="8640h0m0s",ttl:str="5m0s",resolve=False):
    url = ipfsapi+"/api/v0/name/publish"

    querystring = {"arg":cid,"key":keyname,"resolve":"true","lifetime":lifetime,"ttl":ttl,"v1compat":"true","ipns-base":"base36","resolve":resolve}

    response = httpx.post(url, params=querystring)

    return response.json()