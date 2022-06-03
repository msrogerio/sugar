import time
from config import ENDC, WARNING
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from ..models import Following, Folowers
from .. import db


def openUrl(driver):
    try:
        driver.get('https://www.instagram.com/accounts/login/')
        driver.implicitly_wait(6)
        print(f'[INFO] Abriu a url.')
        return True
    except Exception as ex:
        print(f'{WARNING}[Erro] Não conseguiu abrir a url. {ex} {ENDC}')
        return False


def informCredentials(driver, username, password):
    try:
        WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/section/main/div/div/div[1]/div[2]/form/div/div[1]/div/label/input'))).send_keys(username)
        WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/section/main/div/div/div[1]/div[2]/form/div/div[2]/div/label/input'))).send_keys(password)
        print(f'[INFO] Informou as credencias de acesso.')
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
        print(f'[Erro] Usuário ou senha incorretos.')
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


def openMenuProfile(driver):
    try:
        WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div/div[1]/div/div[1]/div/div/div[1]/div[1]/section/nav/div[2]/div/div/div[3]/div/div[6]/div[1]/span'))).click()
        print(f'[INFO] Clicou no span para chamar o menu do perfil de usuário.')
        return True
    except Exception as ex:
        print(f'{WARNING}[ERRO] Não clicou no botão.{ex}{ENDC}')
        return False


def hrefProfile(driver):
    try:
        href = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div/div[1]/div/div[1]/div/div/div[1]/div[1]/section/nav/div[2]/div/div/div[3]/div/div[6]/div[2]/div[2]/div[2]/a[1]'))).get_attribute('href')
        print('[INFO] Conseguiu capturar o href para acessar o perfil')
        return href if href else None
    except Exception as ex:
        print(f'{WARNING}[ERRO] Não conseguiu capturar o href para acessar o perfil.{ex}{ENDC}')
        return None


def srcProfile(driver):
    try:
        src = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div/div[1]/div/div[1]/div/div/div[1]/div[1]/section/nav/div[2]/div/div/div[3]/div/div[6]/div[1]/span/img'))).get_attribute('src')
        print(f'[INFO] Conseguiu capturar o scr da imagem de perfil.')
        return src if src else None
    except Exception as ex:
        print(f'{WARNING}[ERRO] Não conseguiu capturar o scr da imagem de perfil.{ex}{ENDC}')
        return None


def getFollowingFollwers(driver):
    try:
        followers = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div/div[1]/div/div[1]/div/div/div[1]/div[1]/section/main/div/header/section/ul/li[2]/a/div/span'))).text
        following = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div/div[1]/div/div[1]/div/div/div[1]/div[1]/section/main/div/header/section/ul/li[3]/a/div/span'))).text
        print(f'[INFO] Folowers: {followers}, seguindo: {following}')
        return followers, following
    except Exception as ex:
        print(f'{WARNING}[ERRO] Não conseguiu capturar a quantidade de seguidores e seguindo.{ex}{ENDC}')
        return None, None


def getMyUserName(driver):
    try:
        username = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div/div[1]/div/div[1]/div/div/div[1]/div[1]/section/main/div/header/section/div[1]/h2'))).text
        print(f'[INFO] Username: {username}')
        return username
    except Exception as ex:
        print(f'{WARNING}[ERRO] Não conseguiu o nome de usuário.{ex}{ENDC}')
        return None


def openFollowers(driver, username):
    try:
        driver.get(f'https://www.instagram.com/{username}/followers/')
        print(f'[INFO] Abriu o modal de Folowers')
        return True
    except Exception as ex:
        print(f'{WARNING}[ERRO] Não conseguiu abrir o modal de Folowers{ex}{ENDC}')
        return False


def closeModalFollowers(driver):
    try:
        WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div/div[1]/div/div[2]/div/div/div[1]/div/div[2]/div/div/div/div/div/div/div/div[1]/div/div[3]/div/button'))).click()
        print(f'[INFO] Fechou o modal de Folowers')
        return True
    except Exception as ex:
        print(f'{WARNING}[ERRO] Não conseguiu fechar o modal de Folowers{ex}{ENDC}')
        return False


def openFollowing(driver, username):
    try:
        driver.get(f'https://www.instagram.com/{username}/following/')
        print(f'[INFO] Abriu o modal de Following')
        return True
    except Exception as ex:
        print(f'{WARNING}[ERRO] Não conseguiu abrir o modal de Following{ex}{ENDC}')
        return False


def getFollowersAndFollowing(driver, my_id, username, logando):
    if openFollowers(driver, username) == False:
        return None, None
    followers, following = getFollowingFollwers(driver)
    
    logando.mensage = f'Capturou. Seguidores: {followers}, Seguindo {following}'
    db.session.add(logando)
    db.session.commit()
    
    if not followers:
        return None, None
    li_followers = []
    logando.mensage = f'Iniciando captura de seguidores ...'
    db.session.add(logando)
    db.session.commit()
    while True:
        try:
            driver.implicitly_wait(5)
            driver.execute_script(
                """
                var element = document.getElementsByClassName("_aano")[0];
                element.scrollTop = element.scrollHeight
                """
            )
        except Exception as ex:
            print(f'{WARNING}[INFO] Chegou ao fim da barra {ex}.{ENDC}')
        try: 
            li_followers = driver.find_elements_by_class_name('_aad7')
            print('[INFO] Tamanho do vetor', len(li_followers))
            logando.mensage = f'{len(li_followers)} usuários capturados até o momento'
            db.session.add(logando)
            db.session.commit()
            if len(li_followers) >= int(followers):
                break
            else:
                continue
        except Exception as ex:
            pass

    for i in li_followers:
        if ' ' in i.text or '\n' in i.text:
            continue
        follower = Folowers()
        follower.username = i.text
        follower.user_id = my_id
        db.session.add(follower)
        db.session.commit()
        print('[INFO] Registro adicionado no banco.')


    #### > > > < < < ####
    # driver.refresh()
    closeModalFollowers(driver)
    time.sleep(5)

    if openFollowing(driver, username) == False:
        return None, None
    time.sleep(5)
    
    if not following:
        return None, None
    logando.mensage = f'Iniciando captura daqueles que você segue ...'
    db.session.add(logando)
    db.session.commit()
    li_following = []
    while True:
        try:
            driver.implicitly_wait(5)
            driver.execute_script(
                """
                var element = document.getElementsByClassName("_aano")[0];
                element.scrollTop = element.scrollHeight
                """
            )
        except Exception as ex:
            print(f'{WARNING}[INFO] Chegou ao fim da barra {ex}.{ENDC}')
            break
        
        try: 
            li_following = driver.find_elements_by_class_name('_aad7')
            print('[INFO] Tamanho do vetor', len(li_following))
            logando.mensage = f'{len(li_following)} usuários capturados até o momento'
            db.session.add(logando)
            db.session.commit()
            if len(li_following) >= int(following):
                break
            else:
                continue
        except Exception as ex:
            pass

    for i in li_following:
        if ' ' in i.text or '\n' in i.text or 'Seguindo' in i.text:
            continue
        following = Following()
        following.username = i.text
        following.user_id = my_id
        db.session.add(following)
        db.session.commit()
        print('[INFO] Registro adicionado no banco.')

    return li_followers, li_followers


def viewFollowing(driver, username, actual_user, logando):
    logando.mensage = f'Preparando acesso ao perfil.'
    db.session.add(logando)
    db.session.commit()
    try:
        driver.get(f'https://www.instagram.com/{username}')
    except Exception as ex:
        print(f'{WARNING}[Erro] Não conseguiu abrir a url. {ex} {ENDC}')
        return False
    logando.mensage = f'Acessou a urls para o perfil {username}'
    db.session.add(logando)
    db.session.commit()
    if openFollowing(driver, username) == False:
        return False
    try:
        my_username = WebDriverWait(driver, 1).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[6]/div/div/div/div[3]/ul/div/li[1]/div/div[2]/div[1]/div/div/span/a/span'))).text
        print(f'[INFO] primeiro usuário {my_username} eu: {actual_user}')
        if my_username == actual_user:
            logando.mensage = f'{username} te segue de volta.'
            db.session.add(logando)
            db.session.commit()
            return False
        logando.mensage = f'{username} não te segue de volta.'
        db.session.add(logando)
        db.session.commit()
        return True
    except Exception as ex:
        print(f'{WARNING}[Erro] Não conseguiu exetuar a rotina de intereção com o selenium. {ex} {ENDC}')
        return False
        

def IStoppedFollowing(driver, username, logando):
    logando.mensage = f'Preparando acesso ao perfil.'
    db.session.add(logando)
    db.session.commit()
    
    try:
        driver.get(f'https://www.instagram.com/{username}')
    except Exception as ex:
        print(f'{WARNING}[Erro] Não conseguiu abrir a url. {ex} {ENDC}')
        return False
    
    logando.mensage = f'Acessou a urls para o perfil {username}'
    db.session.add(logando)
    db.session.commit()

    step1 = False
    step2 = False
    try:
        driver.execute_script(
                """
                $('._6VtSN').click();
                """
            )
        logando.mensage = f'Clicou no botão de "deixar de seguir"'
        db.session.add(logando)
        db.session.commit()
        print('[INFO] Clicou no botão de "deixar de seguir"')
        step1 = True
    except Exception as ex:
        print(f'{WARNING}[Erro] Não conseguiu exetuar a rotina de intereção com o selenium. {ex} {ENDC}')
        return False

    try:
        driver.execute_script(
                """
                $('.-Cab_').click();
                """
            )
        logando.mensage = f'Encontrou um perfil privado. Validado a ação de deixar de seguir para perfil privado.'
        db.session.add(logando)
        db.session.commit()
        print('[INFO] Encontrou um perfil privado. Validado a ação de deixar de seguir para perfil privado.')
        step2 = True
    except Exception as ex:
        print(f'{WARNING}[Erro] Não conseguiu exetuar a rotina de intereção com o selenium. {ex} {ENDC}')
        return False
    
    if step1 == True or step2 == True:
        logando.mensage = f'Deixou de seguir {username}'
        db.session.add(logando)
        db.session.commit()
        print(f'[INFO] Deixou de seguir {username}')
        return True
    return False

        