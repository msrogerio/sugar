from . import main
from .. models import CheckProgress, Unfollow, Users
from flask import jsonify, redirect, render_template, request, url_for
from ..cwarler.controller import driver as new_driver
from ..cwarler.crawler import *
from sqlalchemy import desc


PASSWORD = ''

@main.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template('home.html')
    if request.method == 'POST':
        new_driver.newInstanceDriver()
        driver = new_driver.driver

        usuario = request.form['username']
        senha = request.form['password']
        
        global PASSWORD
        PASSWORD = senha
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


@main.route('/data-returned', methods=['GET'])
def data_returned():
    username=request.args.get('username')
    id = Users.query.filter_by(username=username).first().id
    followers = Folowers.query.filter(Folowers.user_id==id).all()
    print(len(followers))
    following = Following.query.filter(Following.user_id==id).all()
    print(len(following))
    global PASSWORD
    password = PASSWORD
    PASSWORD = password
    return render_template('data-returned.html', followers=followers, following=following, username=username)


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
    global PASSWORD
    password = PASSWORD
    PASSWORD = password
    return redirect(url_for('.index'))


@main.route('/check-unfollow', methods=['GET', 'POST'])
def check_unfollow():
    if request.method == 'GET':
        username = request.args.get('username')
        id = Users.query.filter_by(username=username).first().id
        logando = CheckProgress.query.filter(CheckProgress.user_id==id).first()
        following = Following.query.filter(Following.user_id==id).all()
        new_driver.newInstanceDriver()
        driver = new_driver.driver    
        global PASSWORD
        password = PASSWORD
        PASSWORD = password
        
        print(password)
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
        followers = Folowers.query.filter(Folowers.user_id==id).all()
        unfollow = Unfollow.query.filter(Unfollow.user_id==id).all()
        return render_template('data-returned.html', followers=followers, following=following, username=username, unfollow=unfollow) 


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