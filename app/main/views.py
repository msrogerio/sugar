import email
from . import main
from .. models import Users
from flask import redirect, render_template, request, url_for
from ..cwarler.controller import driver as new_driver
from ..cwarler.crawler import *


@main.route('/')
def index():
    return render_template('home.html')


@main.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    
    if request.method == 'POST':
        
        new_driver.newInstanceDriver()
        driver = new_driver.driver

        usuario = request.form['usuario']
        senha = request.form['senha']

        if openUrl(driver) == False:
            driver.quit()
            return render_template('login.html')

        if informCredentials(driver, usuario, senha) == False:
            driver.quit()
            return render_template('login.html')
        
        if submitForm(driver) == False:
            driver.quit()
            return render_template('login.html')
        
        if returnCheck(driver):
            driver.quit()
            return render_template('login.html')

        if notSaveLoginInformation(driver) == False:
            driver.quit()
            return render_template('login.html')

        if openProfile(driver) == False:
            driver.quit()
            return render_template('login.html')

        username = getMyUserName(driver)
        if not username:
            return render_template('login.html')
        temp = Users.query.filter_by(username=username).first()
        if temp:
            id= temp.id
        else:
            user = Users()
            user.username = username
            user.email = usuario
            db.session.add(user)
            db.session.commit()
            id = Users.query.filter_by(username=username).first().id
        li_followers, li_following = getFollowers(driver, id)
        if not li_following and not li_followers:
            return render_template('login.html') 
        # driver.quit()
        return redirect(url_for('.data_returned', username=username))


@main.route('/data-returned')
def data_returned():
    username=request.args.get('username')
    print(username)
    id = 1
    # id = Users.query.filter_by(username=username).first()
    followers = Folowers.query.filter(Folowers.user_id==id).all()
    following = Following.query.filter(Following.user_id==id).all()
    return render_template('home.html', followers=followers, following=following)