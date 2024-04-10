from flask import Blueprint, render_template, redirect, url_for, request, flash
from .models import User
from . import db
from flask_login import login_user, login_required, current_user, logout_user, LoginManager
from .forms import LoginForm, RegisterForm

auth=Blueprint('auth', __name__)

login_manager = LoginManager()

@auth.route('/login')
def login():
    return render_template('login.html')

@auth.route('/login', methods=['POST'])
def login_post():
    email = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    user = User.query.filter_by(email=email).first()

    if not user:
        flash('Please check your login details and try again.11')
        return redirect(url_for('auth.login'))
    
    if not check_password_hash(user.password, password):
        flash('Please check your login details and try again.22')
        return redirect(url_for('auth.login'))

    login_user(user, remember=remember)

    return redirect(url_for('views.profile'))


@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        flash("You are already registered.", "info")
        return redirect(url_for("views.profile"))

    form = RegisterForm(request.form)

    if request.method == 'POST' and form.validate():
        email=form.email.data
        
        user = User.query.filter_by(email=email).first()

        if user:
            flash('Email address already exists')
            return redirect(url_for('auth.signup'))
            
        new_user = User(form.username.data, form.email.data,
                    form.password.data)
        db.session.add(new_user)
        db.session.commit()
        flash('Thanks for registering')
        return redirect(url_for('auth.login'))
    return render_template('signup.html', form=form)
    

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('views.index'))


