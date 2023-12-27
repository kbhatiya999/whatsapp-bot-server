from typing import Annotated
from fastapi import Body, FastAPI, Request, Response, HTTPException
import requests
import logging
import xmltodict

app = FastAPI()

# Replace with your actual callback URL
CALLBACK_URL = "http://dinosaur-special-unlikely.ngrok-free.app/notifications"
GOOGLE_HUB_URL = "https://pubsubhubbub.appspot.com/subscribe"

# This should be replaced with a real database or storage system
subscriptions = {}

@app.post("/register")
def register(channel_id: str):
    topic_url = f"https://www.youtube.com/xml/feeds/videos.xml?channel_id={channel_id}"
    response = requests.post(
        GOOGLE_HUB_URL,
        data={
            "hub.mode": "subscribe",
            "hub.topic": topic_url,
            "hub.callback": CALLBACK_URL,
            "hub.verify": "async",  # or 'sync'
        },
    )
    if response.status_code != 202:
        print(response.text)
        raise HTTPException(status_code=400, detail="Subscription request failed")
    subscriptions[channel_id] = topic_url
    return {"message": "Subscription request sent"}

@app.post("/unregister")
def unregister(channel_id: str):
    topic_url = subscriptions.get(channel_id)
    if not topic_url:
        raise HTTPException(status_code=404, detail="Subscription not found")
    response = requests.post(
        GOOGLE_HUB_URL,
        data={
            "hub.mode": "unsubscribe",
            "hub.topic": topic_url,
            "hub.callback": CALLBACK_URL,
            "hub.verify": "async",
        },
    )
    if response.status_code != 202:
        raise HTTPException(status_code=400, detail="Unsubscription request failed")
    del subscriptions[channel_id]
    return {"message": "Unsubscription request sent"}

@app.get("/list-registrations")
def list_registrations():
    return {"subscriptions": subscriptions}

@app.post("/notifications")
async def receive_notifications(request: Request,
                                 body: Annotated[str,Body()]
                                ):
    # body = await request.body()
    logging.info(f"Received notification: {body}")
    # You can process the notification body here
    parsed_xml = xmltodict.parse(body)
    data = parsed_xml['feed']['entry']
    channel_id = data.get('yt:channelId')
    video_id = data.get('yt:videoId')
    print(f'{channel_id=}, {video_id=}')
    return Response(status_code=200)

@app.get("/notifications")
async def receive_notifications_get(request: Request):
    # This method is for handling verification of intent as per PubSubHubbub protocol
    params = request.query_params
    mode = params.get("hub.mode")
    topic = params.get("hub.topic")
    challenge = params.get("hub.challenge")
    lease_seconds = params.get("hub.lease_seconds")

    # Perform any necessary validation here
    # For example, verify that the 'topic' is one you're interested in

    # Respond with the challenge code to confirm the subscription
    return Response(content=challenge)


@app.get("/validate-channel")
def validate_channel(channel: str):
    """
    Validate if a YouTube channel is valid.
    The channel can be in the form of '@VARDAN1' or 'UCeNA8ia-eYKh7JYBfh2esGA'.
    """
    if channel.startswith('@'):
        url = f"https://www.youtube.com/{channel}"
    else:
        url = f"https://www.youtube.com/channel/{channel}"

    response = requests.get(url)
    if response.status_code == 200:
        return {"message": "Valid YouTube channel"}
    else:
        raise HTTPException(status_code=404, detail="YouTube channel not found")

