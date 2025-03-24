import httpx
import io
import json

def put(ipfsapi:str,data:dict):
    url = ipfsapi+"/api/v0/dag/put"

    #querystring = {"store-codec":"dag-cbor","input-codec":"dag-json","pin":"<value>","hash":"<value>","allow-big-block":"false"}

    #json in virtual binary file
    f = io.BytesIO(json.dumps(data, ensure_ascii=False).encode('utf-8'))
    files = { "file": f }

    #response = httpx.post(url, files=files, params=querystring)
    response = httpx.post(url, files=files)

    f.close()

    return response.json()

def get(ipfsapi:str,cid:str):
    url = ipfsapi+"/api/v0/dag/get"

    querystring = {"arg":cid,"output-codec":"dag-json"}

    response = httpx.post(url, params=querystring)

    return response.json()