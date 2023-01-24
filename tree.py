import sqlite3

## basic setup
con = sqlite3.connect("temporary.db")
cur = con.cursor()
cur.execute("CREATE TABLE IF NOT EXISTS pre(id, seq)")
cur.execute("CREATE TABLE IF NOT EXISTS suf(id, seq)")
cur.execute("CREATE TABLE IF NOT EXISTS links(Sid, Pid)")

a = "ATG"
b = "TGC"
c = "GCA"

## manually code the pres

cur.execute("INSERT INTO pre VALUES ('P0', 'AT')")
cur.execute("INSERT INTO pre VALUES ('P1', 'TG')")
cur.execute("INSERT INTO pre VALUES ('P2', 'GC')")

cur.execute("INSERT INTO suf VALUES ('S0', 'TG')")
cur.execute("INSERT INTO suf VALUES ('S1', 'GC')")
cur.execute("INSERT INTO suf VALUES ('S2', 'CA')")



cur.execute("INSERT INTO links VALUES ('S1', 'P2')")
cur.execute("IF (0 = 0, SELECT * FROM pre, SELECT * FROM suf)")


#cur.execute("INSERT VALUES IF (1 = 1, ('S1', 'P4'), ('S2', 'P5')) INTO links")

#for preid in range(3):
#	for sufid in range(3):
#		cur.execute(f"INSERT INTO links VALUES ('{'S' + str(sufid)}', '{'P' + str(preid)}') IF ((SELECT seq FROM suf WHERE id = '{'S' + str(sufid)}') == (SELECT seq FROM pre WHERE id = '{'P' + str(preid)}'))")






res = cur.execute("SELECT * FROM links")
print(res.fetchall())

