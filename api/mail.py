
import requests
import uuid

BASE = "https://api.mail.tm"

domain = requests.get(
    BASE+"/domains"
    ).json()['hydra:member'][0]['domain']


async def create_account():
    
    email = f"{uuid.uuid4()}@{domain}"
    password = f"pass_{uuid.uuid4()}"
    
    json={
        "address":email,
        "password":password
    }
    
    response = requests.post(
        BASE+"/accounts",
        json=json
    )
    
    if response.status_code != 201:
        return {
            "status":"Failed",
            "text":f"Failed to create account: {response.text}"
        }
    
    token = requests.post(
        BASE+"/token",
        json=json
    ).json()["token"]
    
    return email,token

def get_messages(token):
    headers = {"Authorization": f"Bearer {token}"}
    messages = requests.get(
        BASE + "/messages",
        headers=headers
        ).json()
    return messages['hydra:member']

def get_message(token, message_id):
    headers = {"Authorization": f"Bearer {token}"}
    return requests.get(
        BASE+"/messages/"+message_id,
        headers=headers
    ).json()