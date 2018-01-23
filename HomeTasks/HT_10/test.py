from main import *


p = Parser('all')
c = p._curs

c.execute("""SELECT table_name
                   FROM information_schema.tables
                   WHERE table_schema = 'public'""")
tables = c.fetchall()
tables = [i[0] for i in tables]
first = True
for t in tables:
    c.execute("""SELECT column_name FROM information_schema.columns
                   WHERE table_name='{}'""".format(t))
    columns = c.fetchall()
    columns = [i[0] for i in columns]
    if first:
        result = columns
        first = False
    else:
        tmp = []
        for i in columns:
            if i in result:
                tmp.append(i)
        result = tmp[:]
