import httpx

def gen(ipfsapi:str,keyname:str):
    url = ipfsapi+"/api/v0/key/gen"

    querystring = {"arg": keyname}

    response = httpx.post(url, params=querystring)
    
    return response.json()