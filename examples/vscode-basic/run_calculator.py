import numpy
import sys

from calculator import add_numbers, divide_numbers

i = 0
j = 0
max_val = 3
for i in range(max_val):
    for j in range(max_val):
        sum = add_numbers(i,j)
        divide = divide_numbers(i,j)
        print(f"{i} + {j} = {sum}")
        print(f"{i} / {j} = {divide}")