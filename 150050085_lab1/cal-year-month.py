import sys

yearly = sys.stdin.readlines()

row = [0]*3
cal = [0]*35

for i in range(35):
	cal[i] = list(map(''.join, zip(*[iter(yearly[i+1])]*22)))

for m in range(4):
	for n in range(3):
		old_rows = [0]*8
		for i in range(8):
			old_rows[i] = list(map(''.join, zip(*[iter(yearly[1+i+9*m][0+n*22:22+n*22])]*3)))

		new_rows = [""]*8
		new_rows[0] = old_rows[0]
		for i in range(7):
			for j in range(7):
				new_rows[i+1] = new_rows[i+1]+old_rows[j+1][i]


		for i in range(8):
			cal[i+9*m][0+n] = "".join(new_rows[i])

print(yearly[0])

for j in range(3):
	for i in range(8):
		print(cal[i][j]+" "+cal[i+9][j]+" "+cal[i+18][j]+" "+cal[i+27][j])
	print("")