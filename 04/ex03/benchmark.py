import sys, timeit
from functools import reduce

def main():
    if len(sys.argv) != 4:
        print("Error! Usage: benchmark.py function number_of_calls digit_for_calculation")
        sys.exit(1)
    else:
        function_name = sys.argv[1]
        number_of_calls = int(sys.argv[2])
        digit = int(sys.argv[3])
        if function_name == "loop":
            time = timeit.timeit(lambda:loop(digit), number=number_of_calls)
            print (loop(digit))
        elif function_name == "reduce":
            time = timeit.timeit(lambda:reduuce(digit), number=number_of_calls)
            print(reduuce(digit))
        else:
            print("Error! Choose from available options: loop, reduce.")
            sys.exit(1)
    return time

def loop(num):
    sum = 0
    i = 0
    for i in range(num+1):
        sum += i*i
    return sum

def reduuce(num):
    return reduce(lambda sum, i: sum+i*i,range(num+1))


if __name__ == '__main__':
    time = main()
    print(f"{time:.9f}")

#python3 benchmark.py loop 10000000 5
#python3 benchmark.py reduce 10000000 5

