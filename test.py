import sqlite3
conn = sqlite3.connect('spyder.db')
c = conn.cursor()
c.execute("INSERT INTO comic (name,path) VALUES ('%s','%s')" % (comic_name,comic_path) )
conn.commit()
conn.close()