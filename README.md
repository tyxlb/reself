# reself
A decentralized microblog protocol based on IPFS.

"re" representative registry and "self" representative self-host, self-own etc. See [protocol](#protocol) below.

## Getting started
Install IPFS

Clone repository
```
git clone https://github.com/tyxlb/reself.git
cd .\reself\
```
(optional)
```
python -m venv venv
.\venv\Scripts\activate
```
Reself only require Nicegui(include httpx)

Install nicegui
```
pip install nicegui
```
Run
```
python.exe .\main.py
```
First time using it need to configure something.

## Protocol
Inspired by [twtxt](https://twtxt.readthedocs.io/en/latest/user/intro.html), Reself use url(ipns link) as account. A ipns link directs to the user's profile and all of a user's data is centralized in the profile, linked with [IPLD](https://ipld.io). Since only the user can update their ipns link, they can fully control their data.

(inspect [this](https://explore.ipld.io/#/explore/bafyreictlxrz3sobts3xerqiwfj4frjzpoc4mywbwzmwgxvjj375gcdjyu) to see what's the profile look like.)

The profile just stored the user's data. To enable inter-user interoperability features like comments, the registry is introduced. The sole core function of the registry is to store the relationships between data. Because only user can edit data, and all the data is verifiable ,the registry can't be evil.

For example, if Alice wants to post a comment below Bob's item X. First she creates a item:
```
{
    "reply_to":"k51xxxbob/X",
    "context":"balabala",
    "create_at":"isoformat"
}
```
and update her profile. It will be Alice's Yth item. Then Alice query Bob's profile (ipns://k51xxxbob/meta/registry) to know where Bob register at. Finally Alice send message(k51xxxalice/y comment to k51xxxbob/x) to Bob's registry. That's all. Query user's registry to get commments below.

(registry hasn't developed yet.)

In a word, users control the data and registries store the relationships between data.

By using ipfs, reself decouples data storage, allowing anyone to host their profile. IPLD significantly enhances the scalability of the project.
