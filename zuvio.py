from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains
import time

def zuvio_check():
    PATH = './chromedriver'

    
 #建立chrome設定
    chromeOption = webdriver.ChromeOptions()

    from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
    capabilities = DesiredCapabilities().CHROME
    chromeOption.add_argument("--incognito")
    chromeOption.add_argument("--disable-infobars")
    chromeOption.add_argument("start-maximized")
    chromeOption.add_argument("--disable-extensions")
    chromeOption.add_argument("--disable-popup-blocking")
    prefs = {
        'profile.default_content_setting_values':
        {
            'notifications': 1,
            'geolocation': 1
        },

        'profile.managed_default_content_settings':
        {
            'geolocation': 1
        },
    }
    chromeOption.add_experimental_option('prefs', prefs)
    capabilities.update(chromeOption.to_capabilities())

    # chromeOption.add_experimental_option("prefs", {
    #     "profile.default_content_setting_values.notifications":1,
    #     "profile.default_content_setting_values.geolocation": 1,
    # })
    #設定瀏覽器的user agent 
    chromeOption.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; WOW64; rv:53.0) Gecko/20100101 Firefox/53.0')
    chromeOption.add_argument("start-maximized")
    chromeOption.add_argument('--headless')
    chromeOption.add_argument('--no-sandbox')
    chromeOption.add_argument('--disable-dev-shm-usage')
    chromeOption.add_argument('--acceptable-permission-prompts')
    chromeOption.add_argument('--lang=zh-TW.UTF-8')

    chromeOption.add_argument('--disable-gpu')  # 規避google bug


    #開啟Chrome瀏覽器
    driver = webdriver.Chrome(options=chromeOption)
    #driver = webdriver.Chrome(PATH)
    #driver = webdriver.Chrome()




    
    #調整瀏覽器視窗大小
    driver.set_window_size(1024, 960)
    time.sleep(2)



    driver.get('https://irs.zuvio.com.tw/')
    print(driver.title)
            #Chrome Devtools Protocol
    params = {
        "latitude": 24.746554621101463,
        "longitude": 121.74578811577562,
        "accuracy": 100
    }
    driver.execute_cdp_cmd("Page.setGeolocationOverride", params)

    Account = 'b1041080@ms.niu.edu.tw'
    Password = 'a1700000'

    #search = driver.find_element(By.XPATH, '/html/body/div/div[3]/div[3]/div[2]')
    #actions = ActionChains(driver)
    #actions.click(search)
    #actions.perform()
    #sleep(10)

    account = driver.find_element(By.XPATH, '//*[@id="email"]')
    password = driver.find_element(By.ID, 'password')
    account.send_keys(Account)
    password.send_keys(Password)

    #登入
    search = driver.find_element(By.ID, 'login-btn')
    search.click()

    element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="content"]/div[1]/div[1]/div[2]/div[6]'))
    )
    #選擇課程
    print('選擇課程')
    search = driver.find_element(By.XPATH, '//*[@id="content"]/div[1]/div[1]/div[2]/div[3]/div[2]/div[1]')
    search.click()

    #點名簽到
    element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="footer"]/div/div[2]/div[1]'))
    )
    bottom = driver.find_element(By.XPATH, '//*[@id="footer"]/div/div[2]/div[1]')
    bottom.click()

    #簽到
    try:
        for i in range(10):
            driver.refresh()
            try:
                element = WebDriverWait(driver, 3).until(
                    EC.presence_of_element_located((By.XPATH, '//*[@id="submit-make-rollcall"]'))
                )
                print('find')
                bottom = driver.find_element(By.XPATH, '//*[@id="submit-make-rollcall"]')
                bottom.click()
                try:
                    print('test_pass')
                    bottom = driver.find_element(By.XPATH, '//*[@id="submit-make-rollcall"]')
                    bottom.click()
                    #將目前的頁面截圖儲存至暫存圖片路徑
                    driver.save_screenshot('./static/tmp/test.png')
                    print('save')
                    try:
                        success = driver.find_element(By.XPATH, '//*[@id="answer-finish-fcbx"]/div[1]/div')
                        print('簽到成功')

                        break
                    except:
                        print('error')
                except:
                    pass

            except:
                bottom = driver.find_element(By.XPATH, '// *[ @ id = "footer"] / div / div[2] / div[1]')
                bottom.click()
                print('失敗'+str(i+1))
    except:
        print('簽到失敗')



    # actions = ActionChains(driver)
    # actions.click(search)
    # actions.perform()
    #search.send_keys()
    #search.send_keys('1234567890 123gjfjkdjwljl')
    #search.send_keys(Keys.RETURN)

    #time.sleep(30)

    driver.quit()

