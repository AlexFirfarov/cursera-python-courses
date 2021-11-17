import sys

a = int(sys.argv[1])
b = int(sys.argv[2])
c = int(sys.argv[3])

x_1 = int((-b + (b**2 - 4 * a * c) ** 0.5) / (2 * a))
x_2 = int((-b - (b**2 - 4 * a * c) ** 0.5) / (2 * a))

print(x_1)
print(x_2)
