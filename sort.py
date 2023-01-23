import sqlite3

## basic setup
con = sqlite3.connect("temporary.db")
cur = con.cursor()
cur.execute("CREATE TABLE IF NOT EXISTS pre(id, seq)")
cur.execute("CREATE TABLE IF NOT EXISTS suf(id, seq)")
cur.execute("CREATE TABLE IF NOT EXISTS con(id, cons1)")

s = "TGATCGAT"
k = 3
nk = (len(s) - k) + 1

for i in range(nk):
	cur.execute(f"INSERT INTO pre VALUES ({i}, '{s[i:k+i - 1]}')")
	cur.execute(f"INSERT INTO suf VALUES ({i}, '{s[i + 1:k+i]}')")


## this is where you add the initiall link

for i in range(nk):

	res = cur.execute(f"SELECT id FROM pre WHERE seq = (SELECT seq FROM suf WHERE id = {i})")
	a = res.fetchall()
	for j in range(len(a)):
		print(a[j][0])

	cur.execute(f"INSERT INTO con VALUES ({i}, (SELECT id FROM pre WHERE seq = (SELECT seq FROM suf WHERE id = {i})))")


res = cur.execute(f"SELECT * from con")
print(f"DOUG {res.fetchall()}")



print(nk)


for ij in range(2, nk):
	cur.execute(f"ALTER TABLE con ADD {'cons' + str(ij)}")
	for i in range(nk):
		cur.execute(f"UPDATE con SET {'cons' + str(ij)} = (SELECT {'cons' + str(1)} FROM con WHERE id = (SELECT {'cons' + str(ij - 1)} FROM con WHERE id = {i})) WHERE id = {i}")





## SO THIS IS TWO ITERATIONS BUT I COULD SEE DOING IT UNTIL ALL WERE NONE

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
		opt = opt + res.fetchall()[0][0][1:2] ## this will obviously need to be rearranged
	

print(f"ACTUAL: {s}")
print(f"CONSTS: {opt}")

cur.execute("DROP TABLE IF EXISTS pre")
cur.execute("DROP TABLE IF EXISTS suf")
cur.execute("DROP TABLE IF EXISTS con")