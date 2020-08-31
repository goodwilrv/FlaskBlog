

from flask import render_template, url_for, flash, redirect
from FlaskBlog.model import User, Post
from FlaskBlog.forms import RegistrationForm, LoginForm
from FlaskBlog import app,db, bcrypt
from flask_login import UserMixin, login_user, current_user, logout_user


posts = [
      {
      'author':'Gautam Kumar',
      'title':'Blog Post 1',
      'content':'First Post content',
      'date_posted':'May 28, 2020'
      },

      {
      'author':'Manisha Bhagat',
      'title':'Blog Post 2',
      'content':'second Post content',
      'date_posted':'May 29, 2020'
      }
]




  


@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html',posts=posts)


@app.route('/about')
def about():
    return render_template('about.html',title = 'About Flask Title')


@app.route('/register',methods=['GET','POST'])
def register():

  if current_user.is_authenticated:
    return redirect(url_for('home'))

    form = RegistrationForm()
    if form.validate_on_submit():
      hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
      user = User(username = form.username.data, email =form.email.data,password=hashed_password)
      db.session.add(user)
      db.session.commit()
      flash('Your account has been Created, you can now login','success')

      #flash(f'Account Created for {form.username.data}!','success')
      return redirect(url_for('login'))
    return render_template('register.html', title='Register',form=form)


@app.route('/login',methods=['GET','POST'])
def login():

  if current_user.is_authenticated:
    return redirect(url_for('home'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password,form.password.data):
          login_user(user,remember=form.remember.data)
          return redirect(url_for('home'))
        else:
          flash('Login Unsuccessful, Please check UserName and Password','danger')

    return render_template('login.html', title='Login',form=form)

@app.route('/logout')
def logout():
  logout_user()
  return redirect(url_for('home'))