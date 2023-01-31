import sqlite3
# import datetime
# import time
import os
import sys
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
import pandas as pd


# import xlsxwriter


# c = conn.cursor()
class sqlprocess():
    def __init__(self, filename="Stock"):
        self.file = self.resource_path("stock/"+filename + ".db")
        print("file = ",self.file)

    def start(self):
        self.conn = sqlite3.connect(self.file)
        self.c = self.conn.cursor()

    def create(self, type: str):
        self.start()
        if type == "compare":
            self.sql = '''
                                    create table if not exists compare
                                        (id integer primary key autoincrement,
                                        "Name" char(20),
                                        "時間1" float,
                                        "時間2" float,
                                        "時間3" float,
                                        "時間4" float,
                                        "時間5" float,
                                        "時間6" float,
                                        "時間7" float,
                                        "時間8" float
                                          );
                                  '''
        elif type == "revenue":
            self.sql = '''
                          create table if not exists revenue
                              (id integer primary key autoincrement,
                              "時間" varchar(20),
                              "營收（億元）" float,
                              "月增率（%）" float,
                              "去年同期（億元）" float,
                              "營收(增減)年增率（％）" float,
                              "累積營收（億元）" float,
                              "年增率（％）" float,
                              "備注" varchar(90)
                                );
                        '''
        elif type == "predict":
            self.sql = '''
                           create table if not exists predict
                               (id integer primary key autoincrement,
                               "average" float,
                               "name" char(20),
                               "預估" float,
                               "時間1" float,
                               "時間2" float,
                               "時間3" float,
                               "時間4" float,
                               "時間5" float,
                               "時間6" float,
                               "時間7" float
                                 );
                         '''
        elif type == "":
            self.sql = '''
                create table if not exists stock
                    (id integer primary key autoincrement,
                    "年度" varchar(20) ,
                    "股本(億)" varchar(20) ,
                    "財報評分" varchar(20) ,
                    "收盤" varchar(20) ,
                    "平均" varchar(20) ,
                    "漲跌" varchar(20) ,
                    "漲跌(%)" varchar(20) ,
                    "獲利金額(億)-營業收入" varchar(20) ,
                    "獲利金額(億)-營業毛利" varchar(20) ,
                    "獲利金額(億)-營業利益" varchar(20) ,
                    "獲利金額(億)-業外損益" varchar(20) ,
                    "獲利金額(億)-稅後淨利" varchar(20) ,
                    "獲利率(%)-營業毛利" varchar(20) ,
                    "獲利率(%)-營業利益" varchar(20) ,
                    "獲利率(%)-業外損益" varchar(20) ,
                    "獲利率(%)-稅後淨利" varchar(20) ,
                    "ROE(%)" varchar(20) ,
                    "ROA(%)" varchar(20) ,
                    "稅後EPS" varchar(20) ,
                    "年增(元)" varchar(20) ,
                    "BPS(元)" varchar(20));
                    
            '''
        self.c.execute(self.sql)
        self.conn.commit()
        self.conn.close()

    def drop(self, type: str):
        self.start()
        if type == "compare":
            self.sql = '''
                   drop table compare
                       '''
        elif type == 'revenue':
            self.sql = '''
            drop table revenue
            '''
        elif type == "predict":
           self.sql = '''
           drop table predict
           '''

        elif type == '':
            self.sql = '''
            drop table stock
            '''
        try:
            self.c.execute(self.sql)
            self.conn.commit()
        except:
            print("no sqldata")

        if type == "ALL":
            self.sql = '''
                   drop table compare
                       '''
            try:
                self.c.execute(self.sql)
                self.conn.commit()
            except:
                print("no sqldata")
            self.sql = '''
            drop table revenue
            '''
            try:
                self.c.execute(self.sql)
                self.conn.commit()
            except:
                print("no sqldata")
            self.sql = '''
            drop table stock
            '''
            try:
                self.c.execute(self.sql)
                self.conn.commit()
            except:
                print("no sqldata")
        self.conn.close()

    def insert(self, Type: str, data: list, time=None):
        if time != None:
            data.insert(0, time)
        temp = []
        for d in data:
            if type(d) == float:
                temp.append(round(d, 2))
            else:
                temp.append(d)
        data = temp
        self.start()
        # datetime.date("now")
        if Type == "compare":
            self.sql = '''
                        insert into compare("Name" , "時間1", "時間2", "時間3", "時間4", "時間5", "時間6", "時間7", "時間8")
                        values(?,?,?,?,?,?,?,?,?)

                            '''

        elif Type == 'revenue':
            self.sql = '''
                insert into revenue( "時間","營收（億元）","月增率（%）","去年同期（億元）","營收(增減)年增率（％）" ,"累積營收（億元）","年增率（％）","備注")
                values(?,?,?,?,?,?,?,?)

                '''
        elif Type == "predict":
            self.sql = '''
                        insert into predict("average", "name", "預估", "時間1", "時間2", "時間3", "時間4", "時間5", "時間6", "時間7")
                        values(?,?,?,?,?,?,?,?,?,?)
                                         '''
        elif Type == '':
            self.sql = '''

                insert into stock("年度" ,"股本(億)" ,"財報評分", "收盤" ,"平均" ,"漲跌" ,"漲跌(%)","獲利金額(億)-營業收入" ,"獲利金額(億)-營業毛利" ,"獲利金額(億)-營業利益" ,"獲利金額(億)-業外損益" ,"獲利金額(億)-稅後淨利" ,"獲利率(%)-營業毛利" ,"獲利率(%)-營業利益" ,"獲利率(%)-業外損益" ,"獲利率(%)-稅後淨利" ,"ROE(%)" ,"ROA(%)" ,"稅後EPS" ,"年增(元)" ,"BPS(元)" )
                values(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)

                '''
        self.c.execute(self.sql, data)
        self.conn.commit()
        self.conn.close()

    def read(self, Type):
        # self.start()
        # sql = '''
        # select id,name,date,mode,times, Completeness from exercise
        # '''
        # content = self.c.execute(sql)
        # for row in content:
        #     print("id = ",row[0])
        #     print("name = ", row[1])
        #     print("date = ", row[2])
        #     print("mode = ", row[3])
        #     print("times = ", row[4])
        #     print("Completeness = ", row[5])
        # self.conn.close()
        self.toExcel(Type)

    def toExcel(self, Type, filename):

        my_path = self.file
        my_conn = create_engine("sqlite:///" + my_path)
        if Type == "compare":
            try:
                query = "SELECT * FROM compare"  # query to collect record
                df = pd.read_sql(query, my_conn, index_col='id')  # create DataFrame
                print(df.tail())  # Print last 5 rows as sample
                # print(self.resource_path('exercise.xlsx'))
                df.to_excel(self.resource_path('static/tmp/stock-' + filename + '.xlsx'))  # create the excel file

            except SQLAlchemyError as e:
                # print(e)
                error = str(e.__dict__['orig'])
                print(error)
            else:
                print("DataFrame created successfully..")
        if Type == 'revenue':
            try:
                query = "SELECT * FROM revenue"  # query to collect record
                df = pd.read_sql(query, my_conn, index_col='id')  # create DataFrame
                print(df.tail())  # Print last 5 rows as sample
                # print(self.resource_path('exercise.xlsx'))
                df.to_excel(self.resource_path('static/tmp/stock-' + filename + '.xlsx'))  # create the excel file

            except SQLAlchemyError as e:
                # print(e)
                error = str(e.__dict__['orig'])
                print(error)
            else:
                print("DataFrame created successfully..")
        elif Type == '':
            try:
                query = "SELECT * FROM revenue"  # query to collect record
                df = pd.read_sql(query, my_conn, index_col='id')  # create DataFrame
                print(df.tail())  # Print last 5 rows as sample
                # print(self.resource_path('exercise.xlsx'))
                df.to_excel(self.resource_path('static/tmp/stock.xlsx'))  # create the excel file

            except SQLAlchemyError as e:
                # print(e)
                error = str(e.__dict__['orig'])
                print(error)
            else:
                print("DataFrame created successfully..")

    def resource_path(self, relative_path):

        try:
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath("..")
        if base_path[-7:] != "linebot":
            relative_path = "linebot/" + relative_path

            # print("base = ",base_path)
        return os.path.join(base_path, relative_path)


def main():
    sql = sqlprocess()
    # sql.create("compare")
    # year = "9"
    # data = ["4","3","4","3","4","3","4","3","4","3","4","3","4","3","4","3","4","3","4","3"]
    # sql.insert(year,data)
    # sql.read()
    sql.drop('predict')
    # sql.drop('ALL')


if __name__ == "__main__":
    main()