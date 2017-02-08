from flask import render_template,redirect,flash,request,url_for,session,g,send_from_directory
from flask_login import login_user , logout_user , current_user , login_required
from flask_sqlalchemy import SQLAlchemy
from app import app, lm
from .forms import RegistrationForm, editForm, PostingForm, RemovingForm, FindAccountForm
from .models import db,User,PostData
from sqlalchemy import func
import os
import logging
from werkzeug import secure_filename

UPLOAD_FOLDER = './app/static/uploads'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def hello():
    return redirect('/allPost')

@app.before_request
def before_request():
    g.user = current_user

@lm.user_loader
def load_user(id):
    return User.query.get(int(id))

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)

@app.route('/edit',methods=['GET','POST'])
@login_required
def edit():
    db.create_all()
    form = editForm()
    originalImgPath = g.user.userimg[17:]
    tempImgPath = ""
    if request.method == 'POST':
        if originalImgPath != "":
            tempImgPath = secure_filename(originalImgPath)
            os.remove(os.path.join(app.config['UPLOAD_FOLDER'], tempImgPath))
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            tempImgPath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        else:
            tempImgPath = ""
    if form.validate_on_submit():
        form.imgPath.data = '.'+tempImgPath[5:]
        g.user.userimg = form.imgPath.data
        g.user.email = form.email.data
        g.user.password = form.password.data
        db.session.add(g.user)
        db.session.commit()
        return redirect('/'+g.user.username)
    return render_template('edit.html', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    db.create_all()
    form = RegistrationForm()
    imagePath = ""
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            imagePath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        else:
            imagePath = ""
    if form.validate_on_submit():
        form.imgPath.data = '.'+imagePath[5:]
        user = User(form.username.data, form.email.data,
                    form.password.data,form.imgPath.data)
        db.session.add(user)
        db.session.commit()
        flash('Thanks for registering')
        return redirect('/login')
    return render_template('register.html', form=form)

@app.route('/removeID',methods=['GET','POST'])
@login_required
def removeAcc():
    db.create_all()
    form = RemovingForm()
    if form.validate_on_submit():
        deleteDB = db.session.query(User).filter_by(id=g.user.id).first()
        db.session.delete(deleteDB)
        db.session.commit()
        flash('Removed your account. See you again...')
        return redirect('/login')
    return render_template('removeAccount.html',form=form)

@app.route('/findPW',methods=['GET','POST'])
def findAcc():
    db.create_all()
    form = FindAccountForm()
    if form.validate_on_submit():
        username = form.fusername.data
        email = form.femail.data
        fuser = User.query.filter_by(username = username, email=email).first()
        if fuser == None:
            flash('There is no corresponding username or email.')
            return redirect('/login')
        else:
            pwlength = len(fuser.password)
            restpw = "*"*(pwlength-4)
            showpw = fuser.password[:4]+restpw
            flash('Your username is '+fuser.username+' and your password is '+showpw+'. ')
            return redirect('/login')
    return render_template('findMine.html',form=form)

@app.route('/login',methods=['GET','POST'])
def login():
    db.create_all()
    if request.method == 'GET':
        return render_template('login.html')
    username = request.form['username']
    password = request.form['password']
    registered_user = User.query.filter_by(username=username,password=password).first()
    if registered_user is None:
        flash('Username or Password is invalid')
        return redirect(url_for('login'))
    login_user(registered_user)
    return redirect(request.args.get('next') or '/allPost')

@app.route('/logout')
def logout():
    logout_user()
    return redirect('/allPost')

@app.route('/<username>')
@login_required
def userProfile(username):
    db.create_all()
    user = User.query.filter_by(username=g.user.username,password=g.user.password).first()
    if user == None:
        flash('User <'+username+'> does not found.')
        return redirect('/allPost')
    username = user.username
    email = user.email
    image = user.userimg
    time = user.registered_on
    return render_template('profile.html', img = user.userimg, username = user.username, email = user.email, time = time)

@app.route('/makePost',methods=['GET', 'POST'])
@login_required
def write():
    #db.create_all()
    form = PostingForm()
    user = User.query.filter_by(username=g.user.username,password=g.user.password).first()
    imagePath = ""
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            imagePath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        else:
            imagePath = ""
    if form.validate_on_submit():
        form.imgPath.data = '.'+imagePath[5:]
        usernme = user.username
        p = PostData(form.title.data,form.content.data,usernme,form.imgPath.data)
        db.session.add(p)
        db.session.commit()
        return redirect('/allPost')

    return render_template('uploadPost.html',
                           title='Make a post',
                           form=form)

@app.route('/allPost',methods=['GET','POST'])
def listing():
    db.create_all()
    numOflist = PostData.query.count()
    numOfid = numOflist+1
    titleList = []
    contentList = []
    userList = []
    postTime = []

    if numOflist == 0:
        flash('There is no post. Please create a new post.')

    for order0 in range(1,numOfid):
        dbTitle, dbContent, dbUser, dbtime= db.session.query(PostData.title, PostData.content, PostData.username, PostData.posted_on).filter_by(id=order0).first()
        titleList.append(dbTitle)
        if len(dbContent)>60:
            contentList.append(dbContent[:30]+"....")
        else:
            contentList.append(dbContent)
        userList.append(dbUser)
        postTime.append(dbtime)

    return render_template("allPost.html", item = numOflist,atitle = titleList,acontent = contentList,auser = userList, atime = postTime, title = 'View all posts')

@app.route('/<username>_<title>')
#@login_required
def deep1(username,title):
    db.create_all()
    data = PostData.query.filter_by(username = username, title=title).first()
    if data == None:
        flash('User does not found.')
        return redirect('/allPost')
    username = data.username
    titleDetail = data.title
    contentDetail = data.content
    image = data.userimg
    time = data.posted_on

    return render_template('postDetail.html', img = image, username = username, title = titleDetail,content = contentDetail,time=time)

@app.route('/<username>_<title>_removeIt')
@login_required
def removePost(username,title):
    print( g.user.username)
    if g.user.username == username:
        db.create_all()
        deletepost = db.session.query(PostData).filter_by(title=title,username=username).first()
        db.session.delete(deletepost)
        db.session.commit()
        return redirect('/allPost')
    else:
        flash("You don't have andy permission to delete this post.")
        return redirect('/'+username+'_'+title)

@app.login_manager.unauthorized_handler
def unauth_handler():
    app.logger.error('unauthorized error')
    return render_template('unauthorized.html')

@app.errorhandler(Exception)
def unhandled_exception(e):
    return app.logger.error('Unhandled Exception: %s', (e))