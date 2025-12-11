from authlib.integrations.flask_client import OAuth
from flask import url_for,current_app,session
from model import db,user
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import login_user


oauth = OAuth()

def init_oauth(app):
    oauth.init_app(app)
    #Register providers using config values
    cfg = app.config['OAUTH_PROVIDERS']
    if cfg.get("google") and cfg["google"]["client_id"]:
        oauth.register(
            name='google',
            client_id=cfg["google"]["client_id"],
            client_secret=cfg["google"]["client_secret"],
            server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
            client_kwargs={'scope': cfg["google"]["scope"]}
        )




def handle_oauth_callback(provider_name,token):
    # fetch userinfo depending on providers
    if provider_name == "google":
        user_info = oauth.google.parse_id_token(token)
        email = user_info.get("email")
        oauth_id = user_info.get("sub")
        name = user_info.get("name")
    else:
        return None
    if not email:
        return None
    # Find or create user
    user = user.query.filter_by(email=email).first()
    if not user:
        # create new user
        user = user(email=email, name=name, oauth_provider=provider_name, oauth_id=oauth_id)
        db.session.add(user)
        db.session.commit()

    # Login the user
    login_user(user)
    return user