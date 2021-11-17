import sys

count = int(sys.argv[1])

for i in range(1, count + 1):
    print(" " * (count - i) + "#" * i)
