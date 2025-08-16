import sqlite3 as lite
import json
conn = lite.connect('./database.db')
cursor = conn.cursor()

skin_types = ["oily"]
cursor.execute(
    "UPDATE Products SET skin_types = ? WHERE product_id = ?",
    (json.dumps(skin_types), 3)
)
conn.commit()