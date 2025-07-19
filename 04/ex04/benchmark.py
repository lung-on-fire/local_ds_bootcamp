import timeit
import random
from collections import Counter


def create_random():
    return [random.randint(0, 100) for _ in range(1000000)]

def my_function1(rlist):
    newdict = {key: rlist.count(key) for key in range(101) if rlist.count(key) != 0}
    return newdict


def counter_function1(rlist):
    cnt = Counter(rlist)
    return {key: cnt[key] for key in sorted(cnt)}

#cnt = Counter()
#for key in sorted(rlist):
#cnt[key] +=1
#return dict(cnt)

def my_get_top10(rlist):
    rdict = my_function1(rlist)
    sorted_items = sorted(rdict.items(), key = lambda item: item[1], reverse=True)[:10]
    return dict(sorted_items)

def counter_get_top10(rlist):
    rdict = counter_function1(rlist)
    counter = Counter(rdict)
    top10 = counter.most_common(10)
    return dict(top10)


if __name__ == '__main__':
    rlist = create_random()
    print(my_get_top10(rlist))
    print(counter_get_top10(rlist))
    time1 = timeit.timeit(lambda:my_function1(rlist), number=1)
    time2 = timeit.timeit(lambda:counter_function1(rlist), number=1)
    time3 = timeit.timeit(lambda:my_get_top10(rlist), number=1)
    time4 = timeit.timeit(lambda:counter_get_top10(rlist), number=1)
    print(f"my function: {time1:.7f}")
    print(f"Counter: {time2:.7f}")
    print(f"my top: {abs(time3-time1):.7f}")
    print(f"Counter's top: {abs(time4-time2):.7f}")


    
