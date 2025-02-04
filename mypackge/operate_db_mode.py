from pymysql import Connection
# 定义能够操作存储数据库的表的方法

# 数据库链接方法
def link_db(db_name: str) -> tuple:
    # 创建数据库连接
    conn = Connection(
        host='localhost',
        port=3306,
        user='root',
        password='2571160029',
        autocommit=True
    )
    # 选择数据库
    conn.select_db(db_name)
    # 创建游标对象
    cursor = conn.cursor()
    return conn, cursor

# 数据库操作类
class Operate_DB:
    def __init__(self, db_name: str):
        self.db_name = db_name

    # 查询方法 返回查询结果的个数和查询结果的值
    def select_table(self, table_name: str, bequeried_column: str, judgment_conditions_column2: str, value1: str):
        # 获取数据库连接和游标
        conn, cursor = link_db(self.db_name)
        # 执行查询语句
        result1 = cursor.execute(f"select {bequeried_column} from {table_name} where {judgment_conditions_column2}='{value1}'")
        # 获取查询结果
        result2 = cursor.fetchall()
        # 关闭游标和数据库连接
        cursor.close()
        conn.close()
        return result1, result2

    # 插入方法 对指定表进行插入
    def insert_table(self, table_name: str, info1: str, info2: str, info3: str):
        # 获取数据库连接和游标
        conn, cursor = link_db(self.db_name)
        # 执行插入语句
        result = cursor.execute(fr"insert into {table_name} values ('{info1}','{info2}','{info3}')")
        # 关闭游标和数据库连接
        cursor.close()
        conn.close()
        return result

if __name__ == '__main__':
    db = Operate_DB('opencv_images1')
    print(db.select_table('user1','user_image_path','user_id','3120210971055'))
    print(db.insert_table('user1','3120210971054','ywj','123456'))

