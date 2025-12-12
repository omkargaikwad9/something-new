from flask import Flask, render_template, redirect, url_for, request, flash
from config import Config
from models import db, user
from auth import init_oauth, oauth, handle_oauth_callback, create_local_user, verify_local_user
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Length

import os



def create_app():

    app = Flask(__name__)
    app.config["SECRET_KEY"] = "a1f9c27b8e3d44ffbd2e91c917fbb496"



    app.config.from_object(Config)
    db.init_app(app)
    login_manager = LoginManager()
    login_manager.login_view = 'login'
    login_manager.init_app(app)
    init_oauth(app)

    @login_manager.user_loader
    def load_user(user_id):
        return user.query.get(int(user_id))
    
    #forms
    class RegistrationForm(FlaskForm):
        email = StringField("Email",validators=[DataRequired(),Email()])
        name = StringField("Name",validators = [DataRequired(),Length(min=2,max=100)])
        password = PasswordField("password",validators=[DataRequired(),Length(min=6)])
        confirm_password = PasswordField("confirm Password",validators=[DataRequired(),EqualTo("password")])
        submit = SubmitField("Register")


    class LoginForm(FlaskForm):
        email = StringField("Email",validators=[DataRequired(),Email()])
        password = PasswordField("Password",validators=[DataRequired()])
        submit = SubmitField("Login")

    @app.route("/")
    def home():
        return render_template("home.html")
    
    @app.route("/register", methods=["GET","POST"])
    def register():
        form = RegistrationForm()
        if form.validate_on_submit():
            user = create_local_user(form.email.data,form.password.data,form.name.data)
            if user:
                login_user(user)
                flash("Registration successful! Please log in.","success")
                return redirect(url_for("profile"))
            else:
                flash("Email already registered. Please log in.","danger")
                return redirect(url_for("register"))
        return render_template("register.html",form=form)
    
    @app.route("/login", methods=["GET","POST"])
    def login():
        form = LoginForm()
        if form.validate_on_submit():
            user = verify_local_user(form.email.data,form.password.data)
            if user:
                login_user(user)
                flash("Login successful!","success")
                return redirect(url_for("profile"))
            else:
                flash("Invalid email or password.","danger")
        return render_template("login.html",form=form)
    
    @app.route("/logout")
    @login_required
    def logout():
        logout_user()
        flash("You have been logged out.","info")
        return redirect(url_for("home"))
    
    @app.route("/profile")
    @login_required
    def profile():
        return render_template("profile.html",user = current_user,name=current_user.name,email=current_user.email)
    

    #-------------------
    # OAuth routes
    #-------------------


    @app.route("/login/<provider>")
    def oauth_login(provider):
        if provider not in oauth._registry:
            flash("Unsupported OAuth provider.","danger")
            return redirect(url_for("login"))

        redirect_uri = url_for("oauth_callback",provider = provider,_external = True)
        return oauth.create_client(provider).authorize_redirect(redirect_uri)
    
    @app.route("/auth/<provider>/callback")
    def oauth_callback(provider):
        if provider not in oauth._registry:
            flash("Unsupported OAuth provider.","danger")
            return redirect(url_for("login"))
        client = oauth.create_client(provider)

        #toker
        token = client.authorize_access_token()

        # For Google Authlib returns id_token via parse_id_token for OIDC, but above helper handles provider specifics
        user = handle_oauth_callback(provider, token)
        if not user:
            flash("Could not log in via OAuth (email missing?)", "danger")
            return redirect(url_for("login"))
        flash("Logged in via " + provider.capitalize(), "success")
        return redirect(url_for("profile"))

    return app


if __name__ == "__main__":
    app = create_app()
    with app.app_context():
        db.create_all()
    app.run(debug=True)

