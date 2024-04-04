import pymysql
from pymysqlpool.pool import Pool
class Databases_lock():
    def __init__(self):
	
        self.db_config = {
            "host" : "101.101.166.204",
            "port" : 50000,
            "database" : "shopdb",
            "user" : "mydeal",
            "password" : "Nbigbang4cloud",
            "charset":"utf8mb4"
        }
        
        self.pool = Pool(**self.db_config)
        self.pool.init()
	
    def execute(self, query, args={}):
        connection = self.pool.get_conn() #커넥션 풀에서 풀 가져오기
        cursor = connection.cursor()
        cursor.execute(query, args)
        res = cursor.fetchall() 
        cursor.commit()
        self.pool.release(connection) #커넥션 반환
        return res