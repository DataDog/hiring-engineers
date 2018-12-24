import sqlite3

db = sqlite3.connect(":memory:")
sql = """
create table users (
  id integer,
  name varchar(10),
  age integer
);
"""
db.execute(sql)
sql = "insert into users values (1, 'foo', 26)"
db.execute(sql)
c = db.cursor()
c.execute("select * from users where id = 1")
for row in c:
    print (row)

