import os
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = os.path.dirname(os.path.abspath(r"C:\Users\Jyotsna\Desktop\Omkar personal folder\something-new"))
# SQLALCHEMY_DATABASE_URI = os.e"sqlite:///" + os.path.join(BASE_DIR, "app.db"))

class Config:
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(BASE_DIR, "app.db")
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