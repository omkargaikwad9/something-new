import os
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = os.path.dirname(os.path.abspath("C:\Users\Jyotsna\Desktop\Omkar personal folder\something-new"))

class config:
    SECRET_KEY = os.getenv.__get__("SECRET_KEY")
    DATABSE_URL = os.getenv.__get__("DATABASE_URL")
    sqlalchemy_track_modifications = False

    #oAuth credential( set these in your enviroment)

    OAUTH_PROVIDERS = {
        "google":{
            "client_id": os.environ.get("GOOGLE_CLIENT_ID"),
            "client_secret": os.environ.get("GOOGLE_CLIENT_SECRET"),
            "authorize_url": "https://accounts.google.com/o/oauth2/v2/auth",
            "access_token_url": "https://oauth2.googleapis.com/token",
            "userinfo_endpoint": "https://openidconnect.googleapis.com/v1/userinfo",
            "scope": "openid email profile"
        }
    }