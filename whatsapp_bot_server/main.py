from typing import Annotated
from fastapi import FastAPI, Form, Query, Request, HTTPException, Response
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
import pathlib
from config import config
from whatsapp_bot_server.flights import get_flights
from whatsapp_bot_server.message_helper import get_templated_message_input, get_text_message_input, send_message

print(pathlib.Path.cwd())
static_dir = (pathlib.Path(__file__).parent / 'static')
templates_dir = (pathlib.Path(__file__).parent / 'templates')
print(static_dir)
app = FastAPI()
app.mount("/static", StaticFiles(directory=static_dir), name="static")


templates = Jinja2Templates(directory=templates_dir)
class WhatsAppMessage(BaseModel):
    # Define the structure of the message you expect from WhatsApp
    # This is a placeholder structure. Adjust it according to the actual API's specifications.
    message: str
    sender: str


@app.get("/webhook")
async def verify_webhook(
    hub_mode: Annotated[str, Query(alias='hub.mode')],
    hub_challenge: Annotated[str, Query(alias='hub.challenge')],
    hub_verify_token: Annotated[str, Query(alias='hub.verify_token')]
        ):
    # Verify the token
    if hub_mode == "subscribe" and hub_verify_token == 'happy':
        # Respond with the challenge token from the request
        return Response(content=hub_challenge)
    else:
        # Respond with an error if the verification token is wrong
        raise HTTPException(status_code=403, detail="Verification token mismatch")


@app.post("/webhook")
async def receive_message(
    data: dict
    # request: Request
    ):
    try:
        top_level_data = data["entry"][0]['changes'][0]["value"]

        if 'messages' in top_level_data:
            message = top_level_data['messages'][0]

            if message['type'] == 'text':
                message_id = message['id']
                message_text = message['text']['body']
                message_from = message['from']
                # print(message)
                print(message_id, message_from, message_text)
                
                data_send = get_text_message_input(message_from, message_text, message_id)
                await send_message(data_send)
            elif message['type'] == 'document':
                print(message)

            return {"response": f"Echo: {data}"}
        else:
            print('It was some normal event - ignore')

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
   

@app.get('/', response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse(
       name="index.html", context={'request':request}
    )

@app.post('/welcome')
async def welcome():
    data = get_text_message_input(config.recipient_waid, 'Welcome to the Flight Confirmation Demo App for Python!')

    await send_message(data)
    return RedirectResponse(url="/catalog", status_code=303)

@app.get("/catalog", response_class=HTMLResponse)
async def catalog(request: Request):
    flights = get_flights()  # Call your function to get flights data
    return templates.TemplateResponse('catalog.html', {"request": request, "title": "Flight Confirmation Demo for Python", "flights": flights})

@app.post("/buy-ticket")
async def buy_ticket(flight_id: int = Form(..., alias='id')):
    flights = get_flights()
    flight = next(filter(lambda f: f['flight_id'] == flight_id, flights), None)

    if not flight:
        # Handle the case where the flight is not found
        return RedirectResponse(url="/catalog", status_code=303)

    # Assuming RECIPIENT_WAID is a configuration variable, you need to set it up
    recipient_waid = "your_recipient_waid"
    data = get_templated_message_input(config.recipient_waid, flight)

    await send_message(data)
    return RedirectResponse(url="/catalog", status_code=303)



if __name__ == "__main__":
    import uvicorn
    # uvicorn.run('main:app', host="0.0.0.0", port=8000, reload=True)
    uvicorn.run(app, host="0.0.0.0", port=8000)
