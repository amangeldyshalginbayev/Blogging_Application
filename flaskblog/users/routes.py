from flask import render_template, url_for, flash, redirect, request, session, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from flaskblog import db, bcrypt
from flaskblog.models import User, Post
from flaskblog.users.forms import (RegistrationForm, LoginForm,UpdateAccountForm,
                                   RequestResetForm, ResetPasswordForm, MobilePhoneEntryForm,
                                   ConfirmMobilePhoneForm)
from flaskblog.users.utils import (save_picture, remove_picture, send_reset_email, 
                                   send_activation_email)
from flaskblog.users.messente_messaging import send_sms_pin



users = Blueprint('users', __name__)


@users.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        send_activation_email(user)
        flash('Your account has been created! Account activation link is sent to your email', 'success')
        return redirect(url_for('users.login'))
    return render_template("users/register.html", title = "Register", form = form)


@users.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data) and user.is_activated:
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main.home'))
        elif user and bcrypt.check_password_hash(user.password, form.password.data) and not user.is_activated:
            send_activation_email(user)
            flash('You need to activate your account to login. Activation link has been sent to your email', 'danger')
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template("users/login.html", title = "Login", form = form)


@users.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.home'))


@users.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            if current_user.image_file != "default.jpg":
                old_picture = current_user.image_file
                remove_picture(old_picture)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('users.account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template("users/account.html", title = "Account", 
                            image_file = image_file, form = form)


@users.route('/user/<string:username>')
def user_posts(username):
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    posts = Post.query.filter_by(author=user)\
        .order_by(Post.date_posted.desc())\
        .paginate(page=page, per_page=5)
    return render_template("posts/user_posts.html", posts = posts, user = user)


@users.route('/reset_password', methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('An email has been sent with instructions to reset your password.', 'info')
        return redirect(url_for('users.login'))
    return render_template("users/reset_request.html", title = "Reset Password", form = form)


@users.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    user = User.verify_token(token)
    if user is None:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('users.reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash('Your password has been updated! You are now able to log in', 'success')
        return redirect(url_for('users.login'))
    return render_template("users/reset_token.html", title = "Reset Password", form = form)


@users.route('/activate_account/<token>', methods=['GET', 'POST'])
def activate_account(token):
    user = User.verify_token(token)
    if user is None:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('users.login'))
    elif user:
        user.is_activated = True
        db.session.commit()
        flash('Your account has been activated. You can now login.', 'success')
        return redirect(url_for('users.login'))


@users.route('/link_mobile_phone', methods=['GET', 'POST'])
@login_required
def link_mobile_phone():
    form = MobilePhoneEntryForm()
    if form.validate_on_submit():
        full_number = form.country_code.data + form.phone_number.data
        pin_code = send_sms_pin(full_number)
        if pin_code:
            session['pin_code'] = pin_code
            session['phone_number'] = full_number
            flash('We have sent PIN code to your number', 'success')
            return redirect(url_for('users.confirm_mobile_phone'))
        else:
            flash('We were not able to deliver sms to you. Please try again later.', 'danger')
    return render_template("users/link_mobile_number.html", form = form)


@users.route('/confirm_mobile_phone', methods=['GET', 'POST'])
@login_required
def confirm_mobile_phone():
    form = ConfirmMobilePhoneForm()
    pin_code = session.get('pin_code', None)
    phone_number = session.get('phone_number', None)
    if pin_code and phone_number and form.validate_on_submit():
        if pin_code == int(form.pin_code.data):
            current_user.mobile_phone = phone_number
            db.session.commit()
            flash('Your mobile phone number is confirmed', 'success')
            return redirect(url_for('users.account'))
        else:
            flash('You entered incorrect PIN, try again.', 'danger')
            return redirect(url_for('users.link_mobile_phone'))
    return render_template("users/confirm_mobile_phone.html", form = form)


@users.route('/like/<int:post_id>/<action>')
@login_required
def like_action(post_id, action):
    post = Post.query.filter_by(id=post_id).first_or_404()
    if action == 'like':
        current_user.like_post(post)
        db.session.commit()
        flash('You liked the post!', 'alert alert-primary')
    elif action == 'dislike':
        current_user.unlike_post(post)
        db.session.commit()
        flash('You disliked the post!', 'alert alert-warning')
    return redirect(request.referrer)












