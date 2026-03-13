import os
import json
import pika
from fastapi import FastAPI, HTTPException, Depends, Header
from pydantic import BaseModel
import requests

app = FastAPI(title="Note Service")

AUTH_SERVICE_URL = os.getenv("AUTH_SERVICE_URL", "http://auth-service:8000")
RABBITMQ_HOST = os.getenv("RABBITMQ_HOST", "rabbitmq")

class Note(BaseModel):
    title: str
    content: str

def get_current_user(authorization: str = Header(None)):
    if not authorization:
        raise HTTPException(status_code=401, detail="Missing authorization header")
    
    token = authorization.replace("Bearer ", "")
    response = requests.get(f"{AUTH_SERVICE_URL}/verify", params={"token": token})
    if response.status_code != 200:
        raise HTTPException(status_code=401, detail="Invalid token")
    return response.json()["username"]

@app.post("/notes")
async def create_note(note: Note, username: str = Depends(get_current_user)):
    # Business logic: save note (omitted for brevity)
    
    # Notify
    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST))
        channel = connection.channel()
        channel.queue_declare(queue='notifications')
        
        message = {
            "username": username,
            "action": "create_note",
            "title": note.title,
            "timestamp": "now"
        }
        channel.basic_publish(exchange='', routing_key='notifications', body=json.dumps(message))
        connection.close()
    except Exception as e:
        print(f"Failed to send notification: {e}")

    return {"message": "Note created", "note": note}

@app.get("/health")
def health():
    return {"status": "ok"}
