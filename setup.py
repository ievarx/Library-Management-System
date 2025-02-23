import os
try:
    import mysql.connector
except ImportError:
    print("Installing mysql-connector-python...")
    os.system('pip install mysql-connector-python')
