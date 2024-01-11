from pydantic_settings import BaseSettings

class ConfigSettings(BaseSettings):
    ngrok_hostname: str
    ngrok_auth_token: str
    app_id: str
    app_secret: str
    recipient_waid: str
    version: str
    phone_number_id: str
    access_token: str

    class Config:
        env_prefix = ''  # Prefix for environment variables
        env_file = '.env.local'  # Name of the dotenv file to load

# Example of using the settings
config = ConfigSettings()
print("NGROK Hostname:", config.ngrok_hostname)
