from flask import render_template, redirect, url_for, flash, request, Blueprint
from flaskblog import db, bcrypt
from flaskblog.users.forms import (RegisterForm, LoginForm, UpdateAccountForm, 
                            RequestToken, ResetPasswordForm)
from flaskblog.models import User
from flask_login import login_user, current_user, logout_user, login_required
from flaskblog.users.utils import save_image, send_mail

users = Blueprint('users', __name__)

@users.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RegisterForm()
    if form.validate_on_submit():
        user1 = User.query.filter_by(username=form.username.data).first()
        user2 = User.query.filter_by(email=form.email.data).first()
        if user1 is not None:
            flash(f'This username is taken, Please choose another', 'danger')
        elif user2 is not None:
            flash(f'This mail id is taken, Please choose another', 'danger')
        else:
            hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
            user = User(username=form.username.data, email=form.email.data, password = hashed_password)
            db.session.add(user)
            db.session.commit()
            flash(f'Account created successfully', 'success')
            return redirect(url_for('users.login'))
    return render_template('register.html', form=form)

@users.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            flash(f'Login successfully', 'success')
            return redirect(url_for('main.home'))
        else:
            flash(f'Invalid Credintials!', 'danger')
    return render_template('login.html', form=form)

@users.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('users.login'))

@users.route('/about', methods=['GET', 'POST'])
@login_required
def about():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            file_name = save_image(form.picture.data, form.username.data)
            current_user.image_file = file_name
        user1 = User.query.filter_by(username=form.username.data).first()
        user2 = User.query.filter_by(email=form.email.data).first()
        if user1 and form.username.data != current_user.username:
            flash(f'This username is taken, Please choose another', 'danger')
        elif user2 and form.email.data != current_user.email:
            flash(f'This email id is taken, Please choose another', 'danger')
        else:
            current_user.username = form.username.data
            current_user.email = form.email.data
            db.session.commit()
            flash(f'Account details updated', 'success')
            return redirect(url_for('users.about'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='profile_pic/' + current_user.image_file)
    return render_template('about.html', image_file=image_file, form = form)

@users.route('/reset-password', methods=['GET', 'POST'])
def request_reset():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RequestToken()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None:
            flash('This email id is not yet registered, sign-up required.', 'warning')
        else:
            send_mail(user)
            flash('A varification mail is send to your mail, reset password through the link in mail.', 'info')
            return redirect(url_for('users.login'))
    return render_template('request_token.html', form=form)

@users.route('/reset-password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = ResetPasswordForm()
    user = User.varify_token(token)
    if user is None:
        flash('your link is incorrect, or token expired, resend varification mail', 'warning')
        return redirect(url_for('users.request_reset'))
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        return redirect(url_for('users.login'))
    return render_template('reset_password.html', form=form)