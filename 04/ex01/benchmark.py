import timeit

def first_with_loop(emails):
    result = []
    for mail in emails:
        result.append(mail)
    return result


def second_with_lcompr(emails):
    return [mail for mail in emails]

def third_with_map(emails):
    return map(list(),emails)

def comparison(num1, num2, num3):
    if num1 < num2 and num1 < num3:
        return "it is better to use a loop"
    elif num2 < num1 and num2 < num3:
        return "it is better to use a list comprehension"
    else:
        return "it is better to use a map"
    
def time_comparison(num1, num2, num3):
    numlist = [num1, num2, num3]
    time1 = min(numlist)
    time3 = max(numlist)
    filtered_list = [elem for elem in numlist if elem !=time1 and elem !=time3]
    time2 = filtered_list[0] if filtered_list else None
    return f"{time1} vs {time2} vs {time3}"


if __name__ == '__main__':
    emails = ['john@gmail.com', 'james@gmail.com', 'alice@yahoo.com', 'anna@live.com', 'philipp@gmail.com']
    #emails = 5 * emails
    print(first_with_loop(emails))
    print(second_with_lcompr(emails))
    print(third_with_map(emails))
    time1 = timeit.timeit(lambda:first_with_loop(emails), number=9000)
    time2 = timeit.timeit(lambda:second_with_lcompr(emails), number=9000)
    time3 = timeit.timeit(lambda:third_with_map(emails), number=9000)
    print(comparison(time1, time2, time3))
    print(time_comparison(time1, time2, time3))