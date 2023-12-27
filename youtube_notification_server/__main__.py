import os
from fastapi import FastAPI
from pyngrok import ngrok #, PyngrokConfig
import uvicorn

HOSTNAME = os.getenv('NGROK_HOSTNAME')
AUTH_TOKEN = os.getenv('NGROK_AUTH_TOKEN')
ngrok.set_auth_token(AUTH_TOKEN)

if __name__ == "__main__":
    # Setup ngrok
    # pyngrokconfig = PyngrokConfig()
    ngrok_tunnel = ngrok.connect(8000, hostname=HOSTNAME)
    print('ngrok tunnel "http://127.0.0.1:8000" ->', ngrok_tunnel.public_url)

    # Run the server
    uvicorn.run('main:app', port=8000, reload=False, reload_delay=5)
