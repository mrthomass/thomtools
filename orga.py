import sqlite3

## basic setup
con = sqlite3.connect("temporary.db")
cur = con.cursor()
cur.execute("CREATE TABLE IF NOT EXISTS pre(id, seq)")
cur.execute("CREATE TABLE IF NOT EXISTS suf(id, seq)")
cur.execute("CREATE TABLE IF NOT EXISTS con(id, cons1)")

### DONE ---------------------------------------------
## INITIALIZING THE K-MERS


s = "ATGATG"
k = 3
nk = (len(s) - k) + 1


for i in range(nk):
	cur.execute(f"INSERT INTO pre VALUES ({i}, '{s[i:k+i - 1]}')")
	cur.execute(f"INSERT INTO suf VALUES ({i}, '{s[i + 1:k+i]}')")




### DONE ---------------------------------------------
## INPUTING EACH ONES CONNECTION
## this is where you add the initiall link each start to each of its seconds
 
for i in range(nk):

	res = cur.execute(f"SELECT id FROM pre WHERE seq = (SELECT seq FROM suf WHERE id = {i})")
	a = res.fetchall()
	for j in range(len(a)):
		cur.execute(f"INSERT INTO con VALUES ({i}, {a[j][0]})")


for i in range(2, nk):
	cur.execute(f"ALTER TABLE con ADD {'cons' + str(i)}")
	cur.execute(f"UPDATE con SET {'cons' + str(i)} = (SELECT {'cons' + str(i - 1)} FROM con WHERE id = {i - 1}) WHERE {'cons' + str(i - 1)} = 1")


res = cur.execute(f"SELECT * FROM con")
print(f"{res.fetchall()}")


