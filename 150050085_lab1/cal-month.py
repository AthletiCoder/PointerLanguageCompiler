import sys

NUMBER_WEEKS = 7
NUMBER_WEEKDAYS = 7

data = sys.stdin.readlines()
row = [0]*NUMBER_WEEKS
cal = [0]*NUMBER_WEEKS
for i in range(NUMBER_WEEKS):
	row[i] = data[1+i]
	cal[i] = list(map(''.join, zip(*[iter(row[i])]*3)))

print(data[0],end="")
for j in range(NUMBER_WEEKDAYS):
	for i in range(len(cal)):
		print(cal[i][j], end=" ")
	print("")
