from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

from bs4 import BeautifulSoup
import time
from datetime import datetime
import pytz
import numpy

from stock import database, income_statement as IS


class stock():
    def __init__(self, STOCK_NUMBER = "8039"):
        self.get_url(STOCK_NUMBER)
        self.YEAR = 2022
        self.MONTH = 12
        self.times = 3
        Taiwan_time = datetime.now(pytz.timezone("Asia/Taipei"))
        self.YEAR = int(Taiwan_time.year)
        self.MONTH = int(Taiwan_time.month)
        self.options = Options()
        self.options.add_argument("--disable-notifications")
        self.options.add_argument('--headless')  # 啟動Headless 無頭
        self.options.add_argument('--disable-gpu') #關閉GPU 避免某些系統或是網頁出錯

        ########################################################
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
        # 設定瀏覽器的user agent
        chromeOption.add_argument(
            'user-agent=Mozilla/5.0 (Windows NT 10.0; WOW64; rv:53.0) Gecko/20100101 Firefox/53.0')
        chromeOption.add_argument("start-maximized")
        chromeOption.add_argument('--headless')
        chromeOption.add_argument('--no-sandbox')
        chromeOption.add_argument('--disable-dev-shm-usage')
        chromeOption.add_argument('--acceptable-permission-prompts')
        chromeOption.add_argument('--lang=zh-TW.UTF-8')

        chromeOption.add_argument('--disable-gpu')  # 規避google bug
        # self.options = chromeOption
        ########################################################

    def browser_wait(self, XPATH='//*[@id="showTable9"]/tbody/tr/th[1]/a/img'):
        try:
            WebDriverWait(self.browser, 10).until(
                EC.presence_of_element_located((By.XPATH, XPATH)))
            print("browser wait successfully..")
        except:
            print("Error! browser wait Error!")
            self.browser.refresh()
            time.sleep(3)
    def get_url(self, STOCK_NUMBER = "8039"):
        self.STOCK_NUMBER = STOCK_NUMBER
        self.FINANCIAL_RATE_ADDRESS = "https://mops.twse.com.tw/mops/web/t05st10_ifrs"
        self.INCOME_STATEMENT_ADDRESS = "https://goodinfo.tw/tw/StockFinDetail.asp?RPT_CAT=IS_M_QUAR_ACC&STOCK_ID=" + self.STOCK_NUMBER
        self.FINANCIAL_RATIOS_ADDRESS = "https://goodinfo.tw/tw/StockFinDetail.asp?RPT_CAT=XX_M_QUAR_ACC&STOCK_ID=" + self.STOCK_NUMBER
        self.BALANCE_STATEMENT = "https://goodinfo.tw/tw/StockFinDetail.asp?RPT_CAT=BS_M_QUAR&STOCK_ID=" + self.STOCK_NUMBER
        self.PERFORMANCE = "https://goodinfo.tw/tw/StockBzPerformance.asp?STOCK_ID=" + self.STOCK_NUMBER
    # #最新營收表
    def get_revenue(self):
    # ########################################################################################################
        self.browser = webdriver.Chrome("chromedriver", chrome_options=self.options)

    #     self.browser = webdriver.Chrome(r"/workspace/chromedriver.exe", chrome_options=self.options)
    #     webdriver_service = Service("/workspace/chromedriver.exe")
    #     self.driver = webdriver.Chrome(options=self.options, service=webdriver_service)
        # self.driver = webdriver.Chrome(executable_path=r"/workspace/chromedriver.exe",options=self.options)
        # self.driver = webdriver.Chrome("/workspace/chromedriver.exe")
        # self.driver = webdriver.Chrome()
        self.browser.get(self.FINANCIAL_RATE_ADDRESS)
        self.browser_wait()
        print("Get page successfully..")


        sql = database.sqlprocess()
        sql.drop('revenue')
        sql.create('revenue')
        data_revenue = []
        month = self.MONTH - 1
        year = self.YEAR
        for i in range(self.times+1):
            if month == 0:
                year -= 1
                month = 12

            # print(year,month)
            select_history = Select(self.browser.find_element(By.CSS_SELECTOR, '#isnew'))
            select_history.select_by_index(1)
            print("select history successfully..")

            stock_id= self.browser.find_element(By.XPATH, '//*[@id="co_id"]')
            stock_id.clear()
            stock_id.send_keys(self.STOCK_NUMBER)
            print("Select stock number successfully..")

            stock_year = self.browser.find_element(By.CSS_SELECTOR, '#year')
            stock_year.clear()
            stock_year.send_keys(str(year-1911))
            print("Select year successfully..")

            select_month = Select(self.browser.find_element(By.XPATH, '//*[@id="month"]'))
            select_month.select_by_index(month)
            print("Select month successfully..")

            buttom = self.browser.find_element(By.CSS_SELECTOR, '#search_bar1 > div > input[type="button"]')
            buttom.click()
            print("Select buttom successfully..")

            self.browser_wait('//*[@id="table01"]/table[4]/tbody/tr[4]/th')
            time.sleep(0.2)
            soup = BeautifulSoup(self.browser.page_source, features="html5lib")

            table = soup.find("table", {"class": "hasBorder"})

            elements_name = table.findAll("th")
            elements_value = table.findAll("td")

            if elements_name:
                data = []
                for element in elements_name[2:10]:
                    data.append(element.text)
                # print("data= ",data)

            # print("elements = ",elements_name)
            if elements_value:
                data = []
                for element in elements_value[:9]:
                    text = element.text
                    text = text[4:]
                    if text[-4] == ",":
                        text = text[:-4]+text[-3:]
                        if text[-7] == ',':
                            text = text[:-7]+text[-6:]

                    try:
                        text = float(text)
                    except:
                        pass
                    data.append(text)
                # print("data= ",data)
                print("Get data successfully..")
                # time.sleep(10)
            else:
                result = {"price":None}
            data_revenue.append([data[0],data[0],data[1],data[3],data[4],data[7],data[8]])
            print("data_revenue = ",data_revenue)
            month = month-1
        for i in range(self.times):
            # print(data_income[i][0],' - ',data_income[i][2],' /',data_income[i][2],' = ',(data_income[i][0]-data_income[i][2])/data_income[i][2]*100)
            # data_income[i][1] = (data_income[i][0]-data_income[i][2])/data_income[i][2]*100
            data_revenue[i] =[data_revenue[i][0]/100000,(data_revenue[i][1]-data_revenue[i+1][1])/data_revenue[i+1][1]*100,data_revenue[i][2]/100000,data_revenue[i][3],data_revenue[i][4]/100000,data_revenue[i][5],data_revenue[i][6]]

        # #output data
        month = self.MONTH
        year = self.YEAR
        for data in data_revenue[:self.times]:
            month = month-1
            if month==0:
                year -= 1
                month = 12
            sql.insert('revenue',data,str(year)+'.'+str(month))

        sql.toExcel('revenue', self.STOCK_NUMBER+"-最新營收表")

        print("Complete..")
        # time.sleep(100)
        self.browser.close()

    # ########################################################################################################

    # 營收比較表
    def get_compare(self):
# ########################################################################################################
        self.browser = webdriver.Chrome("chromedriver", chrome_options=self.options)
        sql = database.sqlprocess()
        sql.drop("compare")
        sql.create('compare')
        income_statement = IS.getINFO()

        self.browser.get(self.INCOME_STATEMENT_ADDRESS)
        self.browser_wait('//*[@id="txtFinBody"]/table/tbody/tr/td/nobr/span[1]')
        print("Get page successfully..")
        data_income_statement_single = income_statement.get_income_statement_value(self.browser,"single")
        data_income_statement_accumulation = income_statement.get_income_statement_value(self.browser,"accumulation")
        print("Get data successfully..")

        self.browser.get(self.FINANCIAL_RATIOS_ADDRESS)
        self.browser_wait('//*[@id="tblFinDetail"]/tbody/tr[100]/td[1]/nobr')
        print("Get page successfully..")
        data_gross_profit_margin_single = income_statement.get_gross_profit_margin(self.browser,"single",TIME=True)
        data_gross_profit_margin_accumulation = income_statement.get_gross_profit_margin(self.browser,"accumulation")
        print("Get data successfully..")
        # time.sleep(10)


        print("data_income_single = ",data_income_statement_single)
        print("data_income_accumulation = ",data_income_statement_accumulation)
        print("data_gross_profit_margin_single = ",data_gross_profit_margin_single)
        print("data_gross_profit_margin_accumulation = ",data_gross_profit_margin_accumulation)
        datas = [data_gross_profit_margin_single[0],data_income_statement_single[0],data_income_statement_accumulation[0],data_gross_profit_margin_single[1],data_gross_profit_margin_accumulation[0],data_income_statement_single[1],data_income_statement_accumulation[1],data_income_statement_single[2],data_income_statement_single[3],data_income_statement_accumulation[2],data_income_statement_single[4],data_income_statement_accumulation[3]]
        for data in datas:
            sql.insert("compare",data)
        sql.toExcel('compare', self.STOCK_NUMBER+"-營收比較表")

        print("Complete..")
        # time.sleep(100)
        self.browser.close()
    # ########################################################################################################
    # #企業價值
    def get_value(self):
# ########################################################################################################
        self.browser = webdriver.Chrome("chromedriver", chrome_options=self.options)
        sql = database.sqlprocess()
        sql.drop('predict')
        sql.create('predict')
        info = IS.getINFO()

        self.browser.get(self.BALANCE_STATEMENT)
        self.browser_wait('/html/body/table[2]/tbody/tr/td[3]/table/tbody/tr/td[1]/table/tbody/tr[1]/th/table/tbody/tr/td[1]/nobr/a')
        print("Get page successfully..")
        data_value = info.get_net_value(self.browser)
        average_value = float(numpy.mean(data_value[0][1:1+7]))
        data_value[0].insert(0, average_value)
        data_value[0].insert(2, "預估...")
        print("Get data successfully..")

        self.browser.get(self.PERFORMANCE)
        self.browser_wait('/html/body/table[2]/tbody/tr/td[3]/table[1]/tbody/tr/td[1]/table/tbody/tr[1]/th/table/tbody/tr/td[1]/nobr/a')
        print("Get page successfully..")
        data_ROE = info.get_performance(self.browser, self.YEAR)
        data_ROE[0].insert(0, "ROE")
        average_ROE = float(numpy.mean(data_ROE[0][1:1+7]))
        data_ROE[0].insert(0, average_ROE)
        data_ROE[0].insert(2, "預估...")

        # time.sleep(30)
        print("Get data successfully..")


        print("data_value = ",data_value)
        print("data_ROE = ",data_ROE)
        print("average_value = ",average_value)
        print("average_ROE = ", average_ROE)
        value = average_value*(pow(1+average_ROE,10))
        print("10年:",value)


        business = ["average","企業價值",""]
        for i in range(7):

            average_value = numpy.mean(data_value[0][3:i+3+5])
            average_ROE_5 = numpy.mean(data_ROE[0][i+3:i+3+5])
            value = float(average_value * (pow(1 + average_ROE_5, 5)))
            business.append(value)
            print("第"+str(i+1)+"年",value)

        business[0] = numpy.mean(business[3:])

        datas = [data_value[0][0:10],data_ROE[0][0:10],business]
        # print(datas)

        for data in datas:
            print("data = ",data)
            sql.insert("predict",data)
        sql.toExcel('predict', self.STOCK_NUMBER+"-3")

        print("Complete..")



        #
        data_value[0][2] = float(input("value="))
        average_value = numpy.mean(data_value[0][2:2+5])
        print("average_value = ", average_value,data_value[0][2:2+5])
        data_ROE[0][2] = float(input("ROE="))
        average_ROE = numpy.mean(data_ROE[0][2:2+5])
        print("average_ROE = ", average_ROE,data_ROE[0][2:2+5])
        value = average_value * (pow(1 + average_ROE, 5))
        print("自訂 = :", value)
        # time.sleep(100)
        self.browser.close()
        datas = [data_value[0][0:10],data_ROE[0][0:10],business]
        # print(datas)
        # sql.drop('predict')
        # sql.create('predict')
        for data in datas:
            print("data = ",data)
            sql.insert("predict",data)
        sql.toExcel('predict', self.STOCK_NUMBER+"-3")

        print("Complete..")







def main():
    Stock = stock()
    StockNumber = input("輸入股票代號:")
    try:
        if 0 < int(StockNumber) < 9999:
            Stock.get_url(StockNumber)
        else:
            print("輸入錯誤，將使用", Stock.STOCK_NUMBER)

    except:
        print("將使用", Stock.STOCK_NUMBER)
    temp = input("輸入表格:(1 or 2 or 3)")
    if temp == "1":
        Stock.get_revenue()
    elif temp == "2":
        Stock.get_compare()
    elif temp == "3":
        Stock.get_value()
    else:
        print("err")








if __name__ == "__main__":
    main()


# time.sleep(300)


# ##################################################################################################################
# sql = database.sqlprocess()
# sql.create()
# # address = "https://www.facebook.com/"
# # address = "https://www.facebook.com/learncodewithmike"
# ID = "2851"
#
# options = Options()
# options.add_argument("--disable-notifications")
#
# browser = webdriver.Chrome("chromedriver", chrome_options=options)
# # ID = input("ID:")
# address = "https://goodinfo.tw/tw/StockBzPerformance.asp?STOCK_ID="+ID
# browser.get("https://goodinfo.tw/tw/ShowK_ChartFlow.asp?RPT_CAT=PER&STOCK_ID=2851&CHT_CAT=WEEK")
# browser_wait()
# soup = BeautifulSoup(browser.page_source, features="html5lib")
# # print("soup = ",soup)
#
#
#
#
#
#
#
# print("start 1")
# browser.get(address)
# browser_wait()
# try:
#     buttom = browser.find_element(By.XPATH, '//*[@id="dismiss-button"]/div/svg')
#     buttom.click()
#     print("close ads")
# except:
#     print("No ads")
# # print(3,browser.page_source)
# soup = BeautifulSoup(browser.page_source, features="html5lib")
# result = []
# elements_1, elements_2 = None, None
#
# for i in range(30):
#     try:
#         # print(i)
#         # buttom = browser.find_element(By.XPATH, '/html/body/table[2]/tbody/tr/td[3]/table/tbody/tr[1]/td/table/tbody/tr/td[1]/table/tbody/tr[1]/th/table/tbody/tr/td[1]/nobr/a')
#         soup = BeautifulSoup(browser.page_source, features="html5lib")
#         table_1 = soup.find("table", {"class": "b1 p4_2 r10"})
#         elements_1 = table_1.findAll("td")
#         print("got detail 1")
#         table_2 = soup.find("table", {"id": "tblDetail"})
#         elements_2 = table_2.findAll("td")
#         print("got detail 2")
#         break
#     except:
#         browser.execute_script("window.scrollTo(0,document.body.scrollHeight)")
#         print("scrolling down")
#         elements = None
#
# if elements_1:
#     data = []
#     for element in elements_1:
#         data.append(element.text)
#     print("data= ",data)
#     result = {"成交價":float(data[2])}
# else:
#     result = {"price":None}
#
# if elements_2:
#     data = []
#     for element in elements_2:
#         data.append(element.text)
#     print(3,data)
#
#     performance = {}
#     for i in range(3):
#         performance[data[i*21]] = []
#         temp = []
#         for j in range(20):
#             temp.append(data[i*21+j+1])
#         performance[data[i*21]] = temp
#
#
#     result["經營績效"] = performance
#     print("經營績效 = ", performance)
#     keys = list(performance.keys())
#     gain = []
#     for key in keys:
#         sql.insert(key,performance[key])
#         gain.append(performance[key][7])
#
#     print(gain)
#     result["營業毛利"] = gain
#
#
# else:
#     result["gain"] = None
#
# sql.read()
# print("result = ",result,type(result))
#
# ##################################################################################################################







#
# email = browser.find_element(By.ID,"email")
# password = browser.find_element(By.ID,"pass")
#
# email.send_keys("34555rr@gmail.com")
# password.send_keys("12345")
# password.submit()