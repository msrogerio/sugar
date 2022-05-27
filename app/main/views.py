import email
from lib2to3.pgen2 import driver
from . import main
from .. models import Users
from flask import redirect, render_template, request, url_for
from ..cwarler.controller import driver as new_driver
from ..cwarler.crawler import *


@main.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template('home.html')
    if request.method == 'POST':
        new_driver.newInstanceDriver()
        driver = new_driver.driver

        usuario = request.form['username']
        senha = request.form['password']

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
        driver.quit()
        return redirect(url_for('.data_returned', username=username))


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
        driver.quit()
        return redirect(url_for('.data_returned', username=username))


@main.route('/data-returned', methods=['GET'])
def data_returned():
    username=request.args.get('username')
    id = Users.query.filter_by(username=username).first().id
    followers = Folowers.query.filter(Folowers.user_id==id).all()
    following = Following.query.filter(Following.user_id==id).all()
    return render_template('data-returned.html', followers=followers, following=following, username=username)


@main.route('/data-user-clean', methods=['GET'])
def data_user_clean():
    username=request.args.get('username')
    id = Users.query.filter_by(username=username).first().id
    db.engine.execute(f'DELETE FROM following WHERE user_id = {id}')
    db.engine.execute(f'DELETE FROM folowers WHERE user_id = {id}')
    db.session.commit()
    return redirect(url_for('.login'))


@main.route('/check-unfollow', methods=['GET', 'POST'])
def check_unfollow():
    if request.method == 'GET':
        username = request.args.get('username')
        id = Users.query.filter_by(username=username).first().id
        following = Following.query.filter(Following.user_id==id).all()
        unfollow = []
        new_driver.newInstanceDriver()
        driver = new_driver.driver    
        for a in following:
            if viewFollowing(driver, a) == True:
                unfollow.append(username)

