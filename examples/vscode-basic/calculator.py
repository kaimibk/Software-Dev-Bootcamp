import numpy
import sys

def add_numbers(a,b):
    return (a + b)

def divide_numbers(a,b):
    if (b == 0):
        print(f"Your denominator is {b}, leading to division by zero!")
        return (1)
        sys.exit()
    else:
        return (a / b)


# a = 5
# b = 3
# result_add = add_numbers(a:=5,b:=3)
# print(f"The sum of {a} and {b} is {result_add}")

# result_divide = divide_numbers(1,0)
# print(f"The division of {1} and {0} is {result_divide}")
