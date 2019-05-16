import random
import time
x = [random.randint(1, 100) for i in range(0, 10000)]


def insert_sort(unsorted):
    sorted = []
    for i in unsorted:
        for index in range(0, len(sorted)):
            if i < sorted[index]:
                sorted.insert(index, i)
                break
        else:
            sorted.append(i)
    return sorted

def bubble_sort(unsorted):
    while True:
        sorted = True
        for i in range(0, len(unsorted)-1):
            if unsorted[i] > unsorted[i+1]:
                temp = unsorted[i+1]
                unsorted[i+1] = unsorted[i]
                unsorted[i] = temp
                sorted = False
        if sorted:
            return unsorted

start = time.time()
print(insert_sort(x) == sorted(x))
print(bubble_sort(x) == sorted(x))
end = time.time()
print(end-start)


