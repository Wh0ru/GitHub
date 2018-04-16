import MySQLdb

class DataOutput(object):
    def __init__(self):
        try:
            self.con=MySQLdb.connect(host='localhost',user='***',passwd='***',port=3306,db='***',charset='utf8') #数据库设置
            self.cur=self.con.cursor()
            print("Connect to db successfully!")
        except:
            print("Failed to connect db!")

    def store_data(self,data):
        if data is None:
            return
        # print(data)
        sql="insert into zhihu_info(username,education) values('{}','{}')".format(data['username'],data['school'])
        # print(sql)
        self.cur.execute(sql)
        self.con.commit()

    def output_end(self):
        self.cur.close()
        self.con.close()