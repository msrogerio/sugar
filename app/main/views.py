from crypt import methods
from . import main
from flask import render_template, request
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

        getFollowers(driver)
        
        driver.quit()
        return render_template('home.html')
