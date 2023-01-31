from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from bs4 import BeautifulSoup
import time

class getINFO():
    def __init__(self):
        self.rows = []

        self.time = 0
    def find_element(self, FORM, TYPE=None,elements_value=None,year:int = None):
        self.rows = []

        if FORM == "income_statement_value":
            if elements_value:
                if TYPE == 'single':
                    for i in range(len(elements_value)):
                        temp = elements_value[i].text
                        if temp == "營業收入":
                            self.rows.append(i)
                        elif temp == "營業利益":
                            self.rows.append(i)
                        elif temp == "稅後淨利":
                            self.rows.append(i)
                        elif temp == "業外損益合計":
                            self.rows.append(i)
                        elif temp == "每股稅後盈餘(元)":
                            self.rows.append(i)
                elif TYPE == 'accumulation':
                    for i in range(len(elements_value)):
                        temp = elements_value[i].text
                        if temp == "營業收入":
                            self.rows.append(i)
                        elif temp == "營業利益":
                            self.rows.append(i)
                        elif temp == "稅後淨利":
                            self.rows.append(i)
                        elif temp == "每股稅後盈餘(元)":
                            self.rows.append(i)
        elif FORM == "net_value":
            if elements_value:
                for i in range(len(elements_value)):
                    temp = elements_value[i].text
                    if temp == "每股淨值(元)":
                        self.rows.append(i)
        elif FORM == "ROE":
            if elements_value:
                for i in range(len(elements_value)):
                    temp = elements_value[i].text
                    if temp == str(year):
                        self.rows.append(i)




    def get_income_statement_value(self,browser,TYPE = 'single'):
        if TYPE == 'single':
            self.type = 0
        elif TYPE == 'accumulation':
            self.type = 1


        self.time = 0

        data_income_statement = []
        select_report = Select(browser.find_element(By.CSS_SELECTOR, '#RPT_CAT'))
        select_report.select_by_index(self.type)
        print("select report-single successfully..")
        time.sleep(0.2)
        select_time = Select(browser.find_element(By.CSS_SELECTOR, '#QRY_TIME'))
        select_time.select_by_index(self.time)
        print("select time successfully..")
        time.sleep(0.2)

        soup = BeautifulSoup(browser.page_source, features="html5lib")

        table = soup.find("table", {"id": "tblFinDetail"})

        # print(table)
        elements_value = table.findAll("td")
        # print("elements_value = ",elements_value)
        # single        營業收入   營業利益    稅後淨利    業外收益/損失（業外損益合計)       EPS(每股稅後盈餘(元)
        # accumulation  營業收入   營業利益    稅後淨利     EPS(每股稅後盈餘(元)

        self.find_element("income_statement_value",TYPE, elements_value)

        for row in self.rows:
            if elements_value:
                data = []
                element_temp = elements_value[row:row + 15]
                if self.type == 0:
                    text = element_temp[0].text
                else:
                    text = "累計"+element_temp[0].text
                data.append(text)
                for element in element_temp[1::2]:
                    text = element.text

                    try:
                        text = float(text)
                    except:
                        pass
                    data.append(text)
                # print("data= ",data)
                data_income_statement.append(data)
                # print("Get data successfully..")
                # time.sleep(10)

        select_time = Select(browser.find_element(By.CSS_SELECTOR, '#QRY_TIME'))
        select_time.select_by_index(self.time+7)
        print("select time successfully..")
        time.sleep(0.2)

        soup = BeautifulSoup(browser.page_source, features="html5lib")
        table = soup.find("table", {"id": "tblFinDetail"})
        elements_value = table.findAll("td")

        data = []
        self.find_element("income_statement_value",TYPE, elements_value)
        for row in self.rows:
            if elements_value:
                element = elements_value[row + 1]
                text = element.text

                try:
                    text = float(text)
                except:
                    pass
                data.append(text)
                # print("data= ",data)

        for i in range(len(self.rows)):
            data_income_statement[i].append(data[i])

        return  data_income_statement

    def get_gross_profit_margin(self, browser,TYPE:str,TIME=False):
        if TYPE == 'single':
            self.type = 0
        elif TYPE == 'accumulation':
            self.type = 1
        gross_profit_margin = []
        select_report = Select(browser.find_element(By.CSS_SELECTOR, '#RPT_CAT'))
        select_report.select_by_index(self.type)
        print("select report-single successfully..")
        time.sleep(0.2)
        select_time = Select(browser.find_element(By.CSS_SELECTOR, '#QRY_TIME'))
        select_time.select_by_index(0)
        print("select time successfully..")
        time.sleep(0.2)

        soup = BeautifulSoup(browser.page_source, features="html5lib")

        table = soup.find("table", {"id": "tblFinDetail"})
        # print(table)
        if TIME:
            elements_time = table.findAll("th")
            data = []
            for element in elements_time[:9]:
                text = element.text
                data.append(text)
            # print("data= ",data)
            gross_profit_margin.append(data)
        elements_value = table.findAll("td")
        self.rows = []
        if elements_value:
            if TYPE == 'single':
                for i in range(len(elements_value)):
                    temp = elements_value[i].text[:5]
                    if temp == "營業毛利率":
                        self.rows.append(i)
            elif TYPE == 'accumulation':
                for i in range(len(elements_value)):
                    temp = elements_value[i].text[:5]
                    if temp == "營業毛利率":
                        self.rows.append(i)

        # print(elements_value)
        # single  毛利率
        for row in self.rows:
            if elements_value:
                data = []
                element_temp = elements_value[row:row + 9]
                if self.type == 0:
                    text = element_temp[0].text[:5]
                else:
                    text = "累計" + element_temp[0].text[:5]
                data.append(text)
                for element in element_temp[1:]:
                    text = element.text

                    try:
                        text = float(text)
                    except:
                        pass
                    data.append(text)
                # print("data= ",data)
                gross_profit_margin.append(data)
                # print("Get data successfully..")
                # time.sleep(10)
        return gross_profit_margin

    def get_net_value(self,browser):
        data_net_value = []
        select_report = Select(browser.find_element(By.CSS_SELECTOR, '#RPT_CAT'))
        select_report.select_by_index(1)
        print("select year successfully..")
        time.sleep(0.2)
        select_time = Select(browser.find_element(By.CSS_SELECTOR, '#QRY_TIME'))
        select_time.select_by_index(self.time)
        print("select time successfully..")
        time.sleep(0.2)

        soup = BeautifulSoup(browser.page_source, features="html5lib")

        table = soup.find("table", {"id": "tblFinDetail"})

        # print(table)
        elements_value = table.findAll("td")
        # print("elements_value = ",elements_value)
        self.find_element("net_value", elements_value=elements_value)

        for row in self.rows:
            if elements_value:
                data = []
                element_temp = elements_value[row:row + 15]
                text = element_temp[0].text
                data.append(text)
                for element in element_temp[1::2]:
                    text = element.text

                    try:
                        text = float(text)
                    except:
                        pass
                    data.append(text)
                # print("data= ",data)
                data_net_value.append(data)
                # print("Get data successfully..")
                # time.sleep(10)
        select_time = Select(browser.find_element(By.CSS_SELECTOR, '#QRY_TIME'))
        select_time.select_by_index(self.time + 7)
        print("select time successfully..")
        time.sleep(0.2)

        soup = BeautifulSoup(browser.page_source, features="html5lib")
        table = soup.find("table", {"id": "tblFinDetail"})
        elements_value = table.findAll("td")


        self.find_element("net_value", elements_value=elements_value)
        for row in self.rows:
            if elements_value:
                element_temp = elements_value[row+1:row + 6]
                # print("element_temp", element_temp)
                for element in element_temp[0::2]:
                    text = element.text

                    try:
                        text = float(text)
                    except:
                        pass
                    data_net_value[0].append(text)
                # print("data= ",data)

                # print("data= ",data)



        return data_net_value

    def get_performance(self, browser, year):
        data_performance = []


        soup = BeautifulSoup(browser.page_source, features="html5lib")

        table = soup.find("table", {"id": "tblDetail"})
        print("table = ",table)
        # print(table)
        elements_value = table.findAll("td")
        print("elements_value = ",elements_value)
        # print("elements_value = ",elements_value)
        self.find_element("ROE", year=year-2, elements_value=elements_value)

        data = []
        for row in self.rows:
            if elements_value:
                element_temp = elements_value[row:]
                print("el = ",element_temp[16].text)
                for element in element_temp[16:16+12*21:21]:
                    text = element.text

                    try:
                        text = float(text)
                        text = text/100
                    except:
                        pass
                    data.append(text)
                # print("data= ",data)

                # print("data= ",data)
        data_performance.append(data)
        return data_performance