import sqlite3
conn = sqlite3.connect('./database.db')
cursor = conn.cursor()
cursor.execute('delete from Users where user_id = ?', (1, ))
conn.commit()
conn.close()