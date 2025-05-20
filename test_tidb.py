import mysql.connector

config = {
    'host': 'gateway01.us-west-2.prod.aws.tidbcloud.com',
    'port': 4000,
    'user': '2QtpTawfnPeuRgg.root',
    'password': 'WgUmRz49VZe2eASI',
    'database': 'test',
    'ssl_ca': 'isrgrootx1 (1).pem'
}

try:
    conn = mysql.connector.connect(**config)
    print("✅ Connected to TiDB Cloud!")
    cursor = conn.cursor()
    cursor.execute("SHOW TABLES;")
    for table in cursor.fetchall():
        print(table)
    conn.close()
except mysql.connector.Error as err:
    print(f"❌ Error: {err}")
