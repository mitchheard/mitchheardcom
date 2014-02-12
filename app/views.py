import os
from flask import render_template, request, session, url_for, redirect, send_from_directory
#from werkzeug.utils import secure_filename
from models import Person, Article
from forms import SignupForm, ArticleCreateForm, SigninForm
from app import app, db

# controllers
@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'ico/favicon.ico')

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.route('/')
def index():
    articles = Article.all()
    return render_template('index.html', articles=articles)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm()
    if request.method == 'POST':
        if not form.validate():
            return render_template('signup.html', form=form)
        else:
            newperson = Person(form.firstname.data, form.lastname.data, form.email.data, form.password.data)
            db.session.add(newperson)
            db.session.commit()
            session['email'] = newperson.email
            return redirect(url_for('profile'))

    elif request.method == 'GET':
        return render_template('signup.html', form=form)

@app.route('/profile', methods=['GET', 'POST'])
def profile():
    if 'email' not in session:
        return redirect(url_for('signin'))
    person = Person.query.filter_by(email=session['email']).first()
    if person:
        article = Article()
        form = ArticleCreateForm()
        if request.method == 'POST' and form.validate_on_submit():
            form.populate_obj(article)
            db.session.add(article)
            db.session.commit()
            return redirect(url_for('index'))
        else:
            return render_template('create.html', form=form)
    return render_template('profile.html')

@app.route('/signin', methods=['GET', 'POST'])
def signin():
  form = SigninForm()

  if request.method == 'POST':
    if form.validate() == False:
      return render_template('signin.html', form=form)
    else:
      session['email'] = form.email.data
      return redirect(url_for('profile'))

  elif request.method == 'GET':
    return render_template('signin.html', form=form)

@app.route('/signout')
def signout():
    if 'email' not in session:
        return redirect(url_for('signin'))
    session.pop('email', None)
    return redirect(url_for('index'))

# @app.route('/upload', methods=['GET','POST'])
# def upload_file():
#     if request.method == 'POST':
#         file = request.files['file']
#         if file.filename:
#             filename = secure_filename(file.filename)
#             file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
#             return render_template('index.html', filename=filename)
#     return render_template('index.html')
#
# @app.route('/uploads/')
# def uploaded_file(filename):
#     return send_from_directory(app.config['UPLOAD_FOLDER'],
#                                filename, as_attachment=True)