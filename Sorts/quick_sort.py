def merge(list_one, list_two):
    sorted = []
    index = 0
    while len(list_one) != 0 and len(list_two) != 0:
        if list_one[index] > list_two[index]:
            sorted.append(list_two.pop(0))
        else:
            sorted.append(list_one.pop(0))
    return sorted + list_one + list_two


def pivot_sort(items):
    low = 0
    high = len(items) - 1
    pivot = items[len(items)//2]
    while low < high:
        if items[low] <= pivot:
            low += 1
        if items[high] >= pivot:
            high -= 1
        if items[low] > pivot > items[high]:
            items[low], items[high] = items[high], items[low]
    return items[0:len(items)//2], items[len(items)//2:len(items)]


def quick_sort(items):
    if len(items) == 1:
        return items
    else:
        list_one, list_two = pivot_sort(items)
        return merge(quick_sort(list_one), quick_sort(list_two))
