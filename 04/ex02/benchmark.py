import sys, timeit

def main(emails):
    if len(sys.argv) != 3:
        print("Error! Usage: benchmark.py function number_of_calls")
        sys.exit(1)
    else:
        function_name = sys.argv[1]
        number = int(sys.argv[2])
        if function_name == "loop":
            time = timeit.timeit(lambda:loop(emails), number=number)
        elif function_name == "list_comprehension":
            time = timeit.timeit(lambda:list_comprehension(emails), number=number)
        elif function_name == "map":
            time = timeit.timeit(lambda:maap(emails), number=number)
        elif function_name == "filter":
            time = timeit.timeit(lambda:filteer(emails), number=number)
        else:
            print("Error! Choose from available options: loop, list_comprehension, map, filter.")
            sys.exit(1)
    return time

def loop(emails):
    result = []
    for mail in emails:
        result.append(mail)
    return result


def list_comprehension(emails):
    return [mail for mail in emails]

def maap(emails):
    return map(list(),emails)

def filteer(emails):
    return(filter(lambda mail: mail in emails, emails))


if __name__ == '__main__':
    emails = ['john@gmail.com', 'james@gmail.com', 'alice@yahoo.com', 'anna@live.com', 'philipp@gmail.com']
    emails = 5 * emails
    time = main(emails)
    print(f"{time:.9f}")

#python3 benchmark.py loop 10000000
#python3 benchmark.py list_comprehension 10000000
#python3 benchmark.py  map 10000000
