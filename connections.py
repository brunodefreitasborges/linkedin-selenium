from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium_stealth import stealth
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

import keyboard
import time
import random

def scrape(maxResults, query_input, user, password):
    # WebDriver setup
    options = webdriver.ChromeOptions()
    options.add_argument('start-maximized')
    options.add_argument("--window-size=1920,1080")
    options.add_argument('--no-sandbox')
    # options.add_argument('--headless')
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)

    browser = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
    stealth(browser,
            languages=["en-US", "en"],
            vendor="Google Inc.",
            platform="Win32",
            webgl_vendor="Intel Inc.",
            renderer="Intel Iris OpenGL Engine",
            fix_hairline=True
            )

    results = 0
    authwall = 0

    browser.get('https://linkedin.com')
    time.sleep(2)
    # Authwall
    try:
        browser.find_element('xpath','/html/body/div/main/div/form/p/button').click()
        time.sleep(1)
        browser.find_element('xpath','//*[@id="session_key"]').click()
        keyboard.write(user)
        time.sleep(1)
        browser.find_element('xpath','//*[@id="session_password"]').click()
        keyboard.write(password)
        time.sleep(1)
        browser.find_element('xpath','/html/body/div/main/div/div/form[1]/div[2]/button').click()
        time.sleep(2)
        print('Authwall bypassed')
        authwall = 1
    except:
        pass
    if(authwall == 0):
        try:  
            browser.find_element('xpath','//*[@id="session_key"]').click()
        except:
            print('Error logging in')
            browser.quit()
            quit()
        keyboard.write(user)
        time.sleep(1)
        browser.find_element('xpath','//*[@id="session_password"]').click()
        keyboard.write(password)
        time.sleep(1)
        browser.find_element('xpath','//*[@id="main-content"]/section[1]/div/div/form/div[2]/button').click()
        time.sleep(2)

    for i in range(1,101):
            try:
                query  = query_input.replace(' ', '%20')
                browser.get('https://www.linkedin.com/search/results/people/?keywords='+ query +'&page='+ str(i) +'')
                time.sleep(3)

                try:
                    for j in range(1,11):
                        print('Getting user at: ' + str(j))                     
                        try:                                                              
                            connect = browser.find_element(By.XPATH, '/html/body/div[4]/div[3]/div[2]/div/div[1]/main/div/div/div[2]/div/ul/li[' + str(j) + ']/div/div/div[3]/div/button').text
                            if(connect == 'Connect' or connect == 'Conectar'):
                                print('Connection available')
                                browser.find_element(By.XPATH, '/html/body/div[4]/div[3]/div[2]/div/div[1]/main/div/div/div[2]/div/ul/li[' + str(j) + ']/div/div/div[3]/div/button').click()
                                time.sleep(random.uniform(1, 2))
                                browser.find_element(By.XPATH, '/html/body/div[3]/div/div/div[3]/button[2]').click()
                                results+=1   
                                if (results >= maxResults):
                                    print('Maximum number of results reached. Finishing the program.')
                                    browser.quit()
                                    return results
                            else:
                                print('User does not accept connections')
                        except:
                                print('Already connected')
                        
                except:
                    print('Error in user at: ' + str(j))
                    pass
            except:
                print('Error in page at: ' + str(i))
                pass
    
    browser.quit()
    return results

user = input('Email: ')
password = input('Password: ')
query_input = input('Query: ')
maxResults = int(input('Max results: '))

results = scrape(maxResults, query_input, user, password)
print('Added '+ str(results) + ' connections.')
