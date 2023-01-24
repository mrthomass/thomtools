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



res = cur.execute(f"SELECT * FROM con")
print(f"ONE {res.fetchall()}")




## CREATING MAPS FROM THE PREEXISTING DATA


for ij in range(2, nk):
	cur.execute(f"ALTER TABLE con ADD {'cons' + str(ij)}")

	for i in range(nk):
		res = cur.execute(f"SELECT {'cons' + str(1)} FROM con WHERE id = (SELECT {'cons' + str(ij - 1)} FROM con WHERE id = {i})")
		a = res.fetchall()
		
		cur.execute(f"UPDATE con SET {'cons' + str(ij)} = {a[0][0]} WHERE id = {i}")

		if len(a) > 1:

			ss = ""
			for j in range(1, ij):
				if j == (ij -1):
					ss += f"cons{j}"
				else:
					ss += f"cons{j}, "

			print(f"A {ss}")

			cur.execute(f"INSERT INTO con (id, {ss}) SELECT id, {ss} FROM con WHERE id = {i}")
			cur.execute(f"UPDATE con SET {'cons' + str(ij)} = {a[1][0]} WHERE id = {i}")



## FINDING WHERE OUR RESULTS ARE (myI is the index of the tuple where we want to construct from), this needs to be reamped

res = cur.execute("SELECT * FROM con")
print(res.fetchall())

myI = -1

for i in range(nk):
	res = cur.execute(f"SELECT {'cons' + str(nk - 1)} FROM con WHERE id = {i} AND {'cons' + str(nk - 1)} IS NOT NULL")
	a = res.fetchall()
	if len(a) == 1:
		myI = i

res = cur.execute(f"SELECT * FROM con WHERE id = {myI}")
m = res.fetchall()[0]




## CONSTRUCTING RESULTS


opt = ""

lenm = len(m)

for i in range(len(m)):
	if i == 0:
		## if start print the prefix
		res = cur.execute(f"SELECT seq FROM pre WHERE id = {m[i]}") ## FIRST
		opt = opt + res.fetchall()[0][0]
	elif i == lenm - 1:
		## if end print suffix
		res = cur.execute(f"SELECT seq FROM suf WHERE id = {m[i]}")
		opt = opt + res.fetchall()[0][0]
	else:
		## if middle print end of prefix, middle
		res = cur.execute(f"SELECT seq FROM pre WHERE id = {m[i]}")
		opt = opt + res.fetchall()[0][0][1:2] ## this will obviously need to be rearranged when the K CHANGES
	

print(f"\nACTUAL: {s}")
print(f"CONSTS: {opt}\n")

cur.execute("DROP TABLE IF EXISTS pre")
cur.execute("DROP TABLE IF EXISTS suf")
cur.execute("DROP TABLE IF EXISTS con")