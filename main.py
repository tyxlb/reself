from nicegui import ui
import theme

import datetime
import json
import os

import ipfs

config={'id':'','follows':[]}
if os.path.exists("config.json"):
    with open("config.json", encoding="utf-8") as f:
        config = json.load(f)

#QmUNLLsPACCz1vLxQVkXqqLX5R1X345qqfHbsf67hvA3Nn is empty file
def get_profile(id:str):
    return ipfs.dag.get(config["ipfsapi"],'/ipns/'+id)

def get_post(id:str,index:int):
    return ipfs.dag.get(config["ipfsapi"],'/ipns/'+id+'/items/'+str(index))

def create_post(context:str):
    create_at=datetime.datetime.now(datetime.timezone.utc).isoformat().replace("+00:00", "Z")
    post={"context":context,"create_at":create_at}

    cid=ipfs.dag.put(config["ipfsapi"],post)["Cid"]
    profile=get_profile(config['id'])
    profile['posts'].append(len(profile['items']))
    profile['items'].append(cid)

    cid=ipfs.dag.put(config["ipfsapi"],profile)["Cid"]["/"]
    ipfs.name.publish(config['ipfsapi'],cid,config['keyname'])

def create_comment(context:str,id:str,index:int):
    create_at=datetime.datetime.now(datetime.timezone.utc).isoformat().replace("+00:00", "Z")
    post={"context":context,"create_at":create_at,"reply_to":id+'/'+str(index)}

    cid=ipfs.dag.put(config["ipfsapi"],post)["Cid"]
    profile=get_profile(config['id'])
    profile['comments'].append(len(profile['items']))
    profile['items'].append(cid)

    cid=ipfs.dag.put(config["ipfsapi"],profile)["Cid"]["/"]
    ipfs.name.publish(config['ipfsapi'],cid,config['keyname'])

#set up config(ipfsapi,keyname,profile)
@ui.page('/setup')
def setup():
    def init_config():
        r=ipfs.key.gen(input_ipfsapi.value,input_keyname.value)
        
        profile={"meta":{"version":"0.1.0","url":"ipns://"+r["Id"],"name":input_name.value,"avatar":"","bio":"","registry":[]},"items":[],"posts":[],"comments":[]}
        cid=ipfs.dag.put(input_ipfsapi.value,profile)["Cid"]["/"]
        
        config.update({"ipfsapi":input_ipfsapi.value,"keyname":input_keyname.value,"id":r["Id"]})
        with open("config.json", "w", encoding="utf-8") as f:
            json.dump(config, f, ensure_ascii=False, indent=4)
        
        ui.notify('creating ipfs key...')
        ui.notify('refresh later')
        ipfs.name.publish(config['ipfsapi'],cid,config['keyname'])
        
        ui.navigate.back()
    
    with ui.column().classes('absolute-center items-center flex'):
        ui.label("didn't find config file.")
        ui.label("create config first!")
        input_ipfsapi=ui.input(label='Kubo RPC API', placeholder='url',value='http://127.0.0.1:5001')
        input_keyname=ui.input(label='Key Name', placeholder='stored in local Kubo node to update ipns record',value='reself')
        input_name=ui.input(label='Name', placeholder='your name')
        ui.button('save', on_click=lambda: init_config())

@ui.page('/settings')
def settings():
    with theme.frame(config['id']):
        def save_config():
            config.update({'ipfsapi':input_ipfsapi.value})
            with open("config.json", "w", encoding="utf-8") as f:
                json.dump(config, f, ensure_ascii=False, indent=4)
            ui.notify('success')
        def save_profile():
            profile.update({'name':input_name.value,'bio':input_bio.value})
            cid=ipfs.dag.put(config['ipfsapi'],profile)["Cid"]["/"]
            ipfs.name.publish(config['ipfsapi'],cid,config['keyname'])
            ui.notify('success')
        
        input_ipfsapi=ui.input(label='Kubo RPC API', placeholder='url',value=config["ipfsapi"])
        ui.button('save config', on_click=lambda: save_config())
        profile=get_profile(config['id'])
        input_name=ui.input(label='Name', placeholder='your name',value=profile['meta']['name'])
        input_bio=ui.textarea(label='Bio', placeholder='your bio',value=profile['meta']['bio'])
        ui.button('save profile', on_click=lambda: save_profile())

@ui.page('/user/{id}')
def user(id:str):
    with theme.frame(config['id']):
        profile={}
        try:
            profile=get_profile(id)
        except:
            ui.label("failed to load user's profile")
            return
        with ui.card():
            ui.avatar()
            ui.label(profile['meta']['name'])
            ui.label(f"url:{profile['meta']["url"]}")
            if profile['meta']["url"]!=("ipns://"+id):
                ui.label("warning:url is different")
            ui.label(profile['meta']["bio"])
        if len(profile["posts"]):
            for i in profile["posts"][::-1]:
                post=get_post(id,i)
                with ui.link(target='/post/'+id+'/'+str(i)):
                    with ui.card():
                        ui.label(datetime.datetime.fromisoformat(post["create_at"]))
                        ui.label(post["context"])
        else:
            ui.label("empty post")

@ui.page('/post/{id}/{index}')
def post(id:str,index:int):
    with theme.frame(config['id']):
        post={}
        try:
            post=get_post(id,index)
        except:
            ui.label("failed to load post")
            return
        input_comment=ui.textarea(label='comment something')
        b=ui.button('publish!', on_click=lambda: create_comment(input_comment.value,id,index))
        with ui.card():
            ui.label(datetime.datetime.fromisoformat(post["create_at"]))
            ui.label(post["context"])

@ui.page('/')
def index():
    with theme.frame(config['id']):
        ui.label(f'Hello {config['id']}!')
        input_post=ui.textarea(label='post something')
        ui.button('publish!', on_click=lambda: create_post(input_post.value))

ui.run(port=8008)