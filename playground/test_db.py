import pymysql

# import charts
# 資料庫參數設定
db_settings = {
    "host": "127.0.0.1",
    "port": 3306,
    "user": "root",
    "password": "Mysql_0928601004",
    "db": "meetingroom_booking_system",
    "charset": "utf8"
}
try:
    # 建立Connection物件
    conn = pymysql.connect(**db_settings)
    print(conn)
except Exception as ex:
    print(ex)