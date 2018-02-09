import sys

yearly = sys.stdin.readlines()

row = [0]*3
cal = [0]*35

for i in range(35):
	cal[i] = list(map(''.join, zip(*[iter(yearly[i+1])]*22)))

print(yearly[0])

for j in range(3):
	for i in range(8):
		print(cal[i][j]+" "+cal[i+9][j]+" "+cal[i+18][j]+" "+cal[i+27][j])
	print("")
