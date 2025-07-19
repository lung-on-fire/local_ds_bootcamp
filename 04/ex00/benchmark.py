import timeit

def first_with_loop(emails):
    result = []
    for mail in emails:
        result.append(mail)
    return result


def second_with_lcompr(emails):
    return [mail for mail in emails]

def comparison(num1, num2):
    if num1 < num2:
        return "it is better to use a loop"
    else:
        return "it is better to use a list comprehension"
    
def time_comparison(num1, num2):
    numlist = [num1, num2]
    time1 = min(numlist)
    time2 = max(numlist)
    return f"{time1} vs {time2}"

if __name__ == '__main__':
    emails = ['john@gmail.com', 'james@gmail.com', 'alice@yahoo.com', 'anna@live.com', 'philipp@gmail.com']
    emails = 5 * emails
    time1 = timeit.timeit(lambda:first_with_loop(emails), number=9000)
    time2 = timeit.timeit(lambda:second_with_lcompr(emails), number=9000)
    print(comparison(time1, time2))
    print(time_comparison(time1, time2))