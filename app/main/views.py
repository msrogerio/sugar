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

        logando = CheckProgress()
        logando.mensage = 'Preparando o acesso ...'
        logando.status = False
        logando.total_records = 0
        logando.treated_records = 0
        db.session.add(logando)
        db.session.commit()

        logando =  CheckProgress.query.order_by(desc(CheckProgress.id)).first()

        if openUrl(driver) == False:
            driver.quit()
            return render_template('home.html')
        logando.mensage = f'Acessando ao Instagram'
        db.session.add(logando)
        db.session.commit()

        if informCredentials(driver, usuario, senha) == False:
            driver.quit()
            return render_template('home.html')
        logando.mensage = f'Validando usuário e senha'
        db.session.add(logando)
        db.session.commit()
        
        if submitForm(driver) == False:
            driver.quit()
            return render_template('home.html')
        
        if returnCheck(driver):
            driver.quit()
            logando.mensage = f'Usuários e senhas não aceitos.'
            db.session.add(logando)
            db.session.commit()
            return render_template('home.html')
        logando.mensage = f'Usuários e senhas aceitos'
        db.session.add(logando)
        db.session.commit()

        if notSaveLoginInformation(driver) == False:
            driver.quit()
            return render_template('home.html')

        if openProfile(driver) == False:
            driver.quit()
            return render_template('home.html')

        username = getMyUserName(driver)
        if not username:
            return render_template('home.html')
        logando.mensage = f'Perfil do usuários {username} acesado.'
        db.session.add(logando)
        db.session.commit()
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
        li_followers, li_following = getFollowers(driver, id,  logando)
        if not li_following and not li_followers:
            return render_template('home.html') 
        driver.quit()
        return redirect(url_for('.data_returned', username=username, acao_id=logando.id))

@main.route('/data-returned', methods=['GET'])
def data_returned():
    username=request.args.get('username')
    logando=request.args.get('acao_id')
    id = Users.query.filter_by(username=username).first().id
    followers = Folowers.query.filter(Folowers.user_id==id).all()
    following = Following.query.filter(Following.user_id==id).all()
    global PASSWORD
    password = PASSWORD
    PASSWORD = password
    return render_template('data-returned.html', followers=followers, following=following, username=username, acao_id=logando)


@main.route('/data-user-clean', methods=['GET'])
def data_user_clean():
    username=request.args.get('username')
    id = Users.query.filter_by(username=username).first().id
    db.engine.execute(f'DELETE FROM following WHERE user_id = {id}')
    db.engine.execute(f'DELETE FROM folowers WHERE user_id = {id}')
    db.engine.execute(f'DELETE FROM unfollow WHERE user_id = {id}')
    db.session.commit()
    global PASSWORD
    password = PASSWORD
    PASSWORD = password
    return redirect(url_for('.index'))


@main.route('/check-unfollow', methods=['GET', 'POST'])
def check_unfollow():
    if request.method == 'GET':
        username = request.args.get('username')
        logando=request.args.get('acao_id')
        id = Users.query.filter_by(username=username).first().id
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
        return render_template('data-returned.html', followers=followers, following=following, username=username, unfollow=unfollow, acao_id=logando) 


@main.route('/check-progress', methods=['GET'])
def checkProgress():
    logando =  CheckProgress.query.order_by(desc(CheckProgress.id)).first()
    return jsonify(logando.mensage)


@main.route('/check-progress1', methods=['GET'])
def checkProgress1():
    logando=request.args.get('acao_id')
    logando =  CheckProgress.query.get(logando)
    return jsonify(logando.mensage)