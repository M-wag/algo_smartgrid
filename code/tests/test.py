import os

levels = 2
path = os.path.abspath(__file__)
common = path
for i in range(levels + 1):
    common = os.path.dirname(common)

print(common)