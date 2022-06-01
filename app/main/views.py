import os
from . import main
from .. models import CheckProgress, StoppedFollowing, Unfollow, Users
from flask import jsonify, redirect, render_template, request, url_for
from ..cwarler.controller import driver as new_driver
from ..cwarler.crawler import *
from sqlalchemy import desc


@main.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template('home.html')
    if request.method == 'POST':
        new_driver.newInstanceDriver()
        driver = new_driver.driver

        usuario = request.form['username']
        senha = request.form['password']

        f = open(usuario + '.temp', 'w+')
        f.write(senha)
        f.close()
        
        user = Users.query.filter_by(login=usuario).first()
        if user:
            id= user.id
        else:
            user = Users()
            user.login = usuario
            db.session.add(user)
            db.session.commit()
            user = Users.query.filter_by(username=usuario).first()
        
        logando = CheckProgress()
        logando.mensage = 'Preparando o acesso ...'
        logando.user_id = user.id
        logando.status = False
        db.session.add(logando)
        db.session.commit()

        logando =  CheckProgress.query.filter(CheckProgress.user_id==user.id).first()

        if openUrl(driver) == False:
            driver.quit()
            return render_template('home.html')
        logando.mensage = f'Acessando o Instagram.'
        db.session.add(logando)
        db.session.commit()

        if informCredentials(driver, usuario, senha) == False:
            driver.quit()
            return render_template('home.html')
        logando.mensage = f'Validando usuário e senha.'
        db.session.add(logando)
        db.session.commit()
        
        if submitForm(driver) == False:
            driver.quit()
            return render_template('home.html')
        
        if returnCheck(driver):
            driver.quit()
            logando.mensage = f'Usuário ou senha incorretos.'
            db.session.add(logando)
            db.session.commit()
            return render_template('home.html')
        logando.mensage = f'Acesso autorizado.'
        db.session.add(logando)
        db.session.commit()

        if notSaveLoginInformation(driver) == False:
            driver.quit()
            return render_template('home.html')

        if openProfile(driver) == False:
            driver.quit()
            return render_template('home.html')

        username = getMyUserName(driver)
        user.username = username
        db.session.add(user)
        db.session.commit()
        
        if not username:
            return render_template('home.html')
        
        logando.mensage = f'Perfil do usuários {username} acesado.'
        db.session.add(logando)
        db.session.commit()
        
        li_followers, li_following = getFollowers(driver, id,  logando)
        if not li_following and not li_followers:
            return render_template('home.html') 
        driver.quit()
        return redirect(url_for('.data_returned', username=username))


@main.route('/followers_following', methods=['GET', 'POST'])
def data_returned():
    username=request.args.get('username')
    if request.method == 'GET':
        id = Users.query.filter_by(username=username).first().id
        followers = Folowers.query.filter(Folowers.user_id==id).all()
        following = Following.query.filter(Following.user_id==id).all()
        return render_template('followers_following.html', followers=followers, following=following, username=username)
    
    if request.method == 'POST':
        if not username:
            username = request.args.get('username')
        id = Users.query.filter_by(username=username).first().id
        logando = CheckProgress.query.filter(CheckProgress.user_id==id).first()
        
        logando.mensage = f'Preparando para consulta de usuários que não te seguem de volta...'
        db.session.add(logando)
        db.session.commit()

        following = Following.query.filter(Following.user_id==id).all()
        new_driver.newInstanceDriver()
        driver = new_driver.driver    
        
        f = open(username + '.temp', 'r')
        password = f.readline()

        openUrl(driver)
        informCredentials(driver=driver, username=username, password=password)
        submitForm(driver)
        returnCheck(driver)

        for a in following:
            if viewFollowing(driver, a.username, username, logando) == True:
                _unfollow = Unfollow()
                _unfollow.user_id = id
                _unfollow.username = a.username
                db.session.add(_unfollow)
                db.session.commit()
        driver.quit()
        return redirect(url_for('.list_unfollow', username=username))


@main.route('/list-unfollow', methods=['GET', 'POST'])
def list_unfollow():
    username=request.args.get('username')
    id = Users.query.filter_by(username=username).first().id
    if request.method == 'GET':
        followers = Folowers.query.filter(Folowers.user_id==id).all()
        unfollow = Unfollow.query.filter(Unfollow.user_id==id).all()
        following = Following.query.filter(Following.user_id==id).all()
        return render_template('data-returned.html', followers=followers, following=following, username=username, unfollow=unfollow) 
    if request.method == 'POST':
        unfollows = request.form.getlist('unfollow')
        new_driver.newInstanceDriver()
        driver = new_driver.driver 
        f = open(username + '.temp', 'r')
        password = f.readline()
        openUrl(driver)
        informCredentials(driver=driver, username=username, password=password)
        submitForm(driver)
        returnCheck(driver)  
        logando = CheckProgress.query.filter(CheckProgress.user_id==id).first()
        for i in unfollows:
            if IStoppedFollowing(driver, i, logando) == True:
                db.engine.execute(f'DELETE FROM following WHERE username = {i}')
                stopped_following = StoppedFollowing()
                stopped_following.username = i
                stopped_following.user_id = id
                db.session.add(stopped_following)
                db.session.commit()
        return redirect(url_for('.unfollow', username=username))


@main.route('/unfollow', methods=['GET', 'POST'])
def unfollow():
    if request.method == 'GET':
        username = request.args.get('username')
        id = Users.query.filter_by(username=username).first().id
        following = Following.query.filter(Following.user_id==id).all()
        unfollow = Unfollow.query.filter(Unfollow.user_id==id).all()
        stopped_following = StoppedFollowing.query.filter(StoppedFollowing.user_id==id).all()
        return render_template('unfollows.html', stopped_following=stopped_following, following=following, username=username, unfollow=unfollow) 


@main.route('/data-user-clean', methods=['GET'])
def data_user_clean():
    username=request.args.get('username')
    id = Users.query.filter_by(username=username).first().id
    db.engine.execute(f'DELETE FROM following WHERE user_id = {id}')
    db.engine.execute(f'DELETE FROM folowers WHERE user_id = {id}')
    db.engine.execute(f'DELETE FROM unfollow WHERE user_id = {id}')
    db.engine.execute(f'DELETE FROM check_progress WHERE user_id = {id}')
    db.engine.execute(f'DELETE FROM users WHERE id = {id}')
    db.session.commit()
    os.remove(username + '.temp')
    return redirect(url_for('.index'))


@main.route('/check-progress', methods=['GET'])
def checkProgress1():
    username = None
    login = None
    try:
        username=request.args.get('username')
    except:
        pass
    try:
        login=request.args.get('login')
    except:
        pass
    if username:
        return queryForUsername(username)
    if login:
        return queryForLogin(login)


def queryForUsername(username):
    user = Users.query.filter(Users.username==username).first()
    logando = CheckProgress.query.filter(CheckProgress.user_id==user.id).first()
    return jsonify(logando.mensage)
    

def queryForLogin(login):
    user = Users.query.filter(Users.login==login).first()
    if user:
        logando = CheckProgress.query.filter(CheckProgress.user_id==user.id).first()
        if not logando:
            logando = CheckProgress()
            logando.mensage = 'Startando a aplicação.'
            logando.user_id = user.id
            db.session.add(logando)
            db.session.commit()
            logando = CheckProgress.query.filter(CheckProgress.user_id==user.id).first()
        return jsonify(logando.mensage)
    else:
        user = Users()
        user.login = login
        db.session.add(user)
        db.session.commit()
        user = Users.query.filter(Users.login==login).first()
        logando = CheckProgress()
        logando.mensage = 'Startando a aplicação.'
        logando.user_id = user.id
        db.session.add(logando)
        db.session.commit()
        logando = CheckProgress.query.filter(CheckProgress.user_id==user.id).first()
        return jsonify(logando.mensage)