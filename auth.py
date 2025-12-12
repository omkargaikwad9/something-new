from authlib.integrations.flask_client import OAuth
from flask import url_for,current_app,session
from models import db,user
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

def create_local_user(email,password,name):
    #check if user already exists
    existing_user = user.query.filter_by(email = email).first()
    if existing_user:
        return None
    #create new user
    password_hash = generate_password_hash(password)
    new_user = user(email = email, passward_hash = password_hash, name = name)
    db.session.add(new_user)
    db.session.commit()
    return new_user


def verify_local_user(email,password):
    u = user.query.filter_by(email = email).first()
    if u and check_password_hash(u.passward_hash,password):
        return u