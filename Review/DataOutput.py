import MySQLdb

class DataOutput(object):
    def __init__(self):
        try:
            self.con=MySQLdb.connect(host='localhost',user='***',passwd='****',port=3306,db='****',charset='utf8')
            self.cur=self.con.cursor()
            print("Connect to db successfully!")
        except:
            print("Failed to connect db!")

    def store_data(self,data):
        if data is None:
            return
        if data['rank']=='':
            data['rank']='0'
        try:
            insert_content = "insert into review_content(title,body,author,rank,movie) values('{}','{}','{}',{},'{}')".format(data['title'], data['content'], data['author'], int(data['rank']), data['movie'])
            insert_category = "insert into review_category(name) values('{}')".format(data['movie_type'])
            self.cur.execute(insert_category)
            self.cur.execute(insert_content)
            self.con.commit()
        except:
            pass

    def output_end(self):
        self.cur.close()
        self.con.close()
