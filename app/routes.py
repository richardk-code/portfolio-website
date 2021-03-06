from flask import render_template, flash, redirect, request, url_for, session
from app import app, db
from app.forms import LoginForm, AddingSkillForm, ContactForm
from flask_login import current_user, login_user
from app.models import User, Skills
from flask_login import logout_user
from flask_login import login_required
from flask_mail import Message, Mail

mail = Mail()
mail.init_app(app)

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('about'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        session['logged_in'] = True
        return redirect(url_for('about'))
    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
    logout_user()
    session['logged_in'] = False
    return redirect(url_for('index'))

@app.route('/about', methods=['GET', 'POST'])
def about():
    form = AddingSkillForm()
    skills = Skills.query.all()
    if form.validate_on_submit():
        skills = Skills(skill=form.skill.data, level=form.level.data, skills=current_user)
        db.session.add(skills)
        db.session.commit()
        return redirect(url_for('index'))   
    return render_template('about.html', title="About", form=form, skills=skills)

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    form = ContactForm()
    if request.method == 'POST':
        if form.validate() == False:
            flash('All fields are required.')
            return render_template('contact.html', form=form)
        else:
            msg = Message(form.subject.data, sender='contact@example.com', recipients=app.config['ADMINS'][0].split())
            msg.body = """
            From: %s &lt;%s&gt;
            %s
            """ % (form.name.data, form.email.data, form.message.data)
            mail.send(msg)
 
            return render_template('contact.html', success=True)
 
    elif request.method == 'GET':
        return render_template('contact.html', form=form)