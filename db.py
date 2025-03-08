from sqlalchemy import create_engine
def get_db_connection():
  try:
    print ("Connecting to MySQL DB")
    engine = create_engine("mysql+pymysql://root:tuan1218@localhost:4306/dbsmartlib")
    conn = engine.connect()
    return conn
  except Exception as e:
    print(f"❌ Lỗi kết nối: {e}")
    return None
