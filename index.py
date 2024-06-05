import pymysql.cursors
# Oppretter en tilkobling til databasen
connection = pymysql.connect(host='172.20.128.73', 
                            user='Daniel',         
                            password='123Akademiet',  
                            database='Users',     
                            charset='utf8mb4',      
                            cursorclass=pymysql.cursors.DictCursor)

