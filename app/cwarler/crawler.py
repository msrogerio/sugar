from config import ENDC, WARNING
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from ..models import Folowers
from .. import db


def openUrl(driver):
    try:
        driver.get('https://www.instagram.com/accounts/login/')
        driver.implicitly_wait(6)
        return True
    except Exception as ex:
        print(f'{WARNING}[Erro] Não conseguiu abrir a url. {ex} {ENDC}')
        return False


def informCredentials(driver, username, password):
    try:
        WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/section/main/div/div/div[1]/div[2]/form/div/div[1]/div/label/input'))).send_keys(username)
        WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/section/main/div/div/div[1]/div[2]/form/div/div[2]/div/label/input'))).send_keys(password)
        return True
    except Exception as ex:
        print(f'{WARNING}[ERRO] Erro ao informar as credencias de acesso. {ex}{ENDC}')
        return False


def submitForm(driver):
    try:
        WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/section/main/div/div/div[1]/div[2]/form/div/div[3]/button/div'))).click()
        print(f'[INFO] Submeteu o formulário.')
        return True
    except Exception as ex:
        print(f'{WARNING}[ERRO] Não submeteu o formulário.{ex}{ENDC}')
        return False
    


def returnCheck(driver):
    try:
        # se encontrar... usuário ou senha incorretos
        return WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, '//*[@id="slfErrorAlert"]'))).text
    except Exception as ex:
        print(f'[INFO] Usuários e senhas validados.')
        return None


def notSaveLoginInformation(driver):
    try:
        WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/section/main/div/div/div/div/button'))).click()
        print(f'[INFO] Não salvou as informações de login.')
        return True
    except Exception as ex:
        print(f'{WARNING}[ERRO] Não clicou no botão.{ex}{ENDC}')
        return False
    

def openProfile(driver):
    try:
        WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/section/nav/div[2]/div/div/div[3]/div/div[6]/div[1]/span/img'))).click()
        WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/section/nav/div[2]/div/div/div[3]/div/div[6]/div[2]/div[2]/div[2]/a[1]/div/div[2]/div/div/div/div'))).click()
        print(f'[INFO] Abriu o perfil do usuário.')
        return True
    except Exception as ex:
        print(f'{WARNING}[ERRO] Não conseguiu abrir o perfil do usuário.{ex}{ENDC}')
        return False


def getFollowingFollwers(driver):
    try:
        followers = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/section/main/div/header/section/ul/li[2]/a/div/span'))).text
        following = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/section/main/div/header/section/ul/li[3]/a/div/span'))).text
        print(f'[INFO] Folowers: {followers}, seguindo: {following}')
        return followers, following
    except Exception as ex:
        print(f'{WARNING}[ERRO] Não conseguiu abrir o perfil do usuário.{ex}{ENDC}')
        return None, None


def openFollowers(driver):
    try:
        WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/section/main/div/header/section/ul/li[2]/a/div/span'))).click()
        print(f'[INFO] Abriu o modal de Folowers')
        return True
    except Exception as ex:
        print(f'{WARNING}[ERRO] Não conseguiu abrir o modal de Folowers{ex}{ENDC}')
        return False


def getFollowers(driver):
        if openFollowers(driver) == False:
            return False
        followers, _ = getFollowingFollwers(driver)
        if not followers:
            return False
        cont = 1
        div = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[6]/div/div/div/div[2]/ul')))
        while True:
            if cont == int(followers):
                break
            while True:
                try:
                    username = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, f'/html/body/div[6]/div/div/div/div[2]/ul/div/li[{cont}]/div/div[2]/div[1]/div/div/span/a/span'))).text
                    name = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, f'/html/body/div[6]/div/div/div/div[2]/ul/div/li[{cont}]/div/div[1]/div[2]/div[2]'))).text
                    print(f'[INFO] Nome de usuário: {username}, usuário {name}.')
                    fl = Folowers()
                    fl.username = username
                    fl.name = name
                    db.session.add(fl)
                    db.session.commit()
                    cont +=1 
                except Exception as ex:
                    print(f'[INFO] Não encontrou mais elementos nesta unidade carregada. {ex}')
                    break
            try:
                driver.execute_script('arguments[0].scrollTop = arguments[0].scrollTop + arguments[0].offsetHeight;', div)
                driver.implicitly_wait(5)
            except Exception as ex:
                print(f'{WARNING}[INFO] Chegou ao fim da barra.{ENDC}')
                break
