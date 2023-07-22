def db_connect():
    import psycopg2
    conn = psycopg2.connect(database="workwise",
                            host="workwise.cflu08otoe2q.us-east-2.rds.amazonaws.com",
                            user="postgres",
                            password="UXD3B9H3Caexcch",
                            port=5432)
    cursor = conn.cursor()
    return cursor