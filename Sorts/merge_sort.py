def merge(list_one, list_two):
    sorted = []
    index = 0
    while len(list_one) != 0 and len(list_two) != 0:
        if list_one[index] > list_two[index]:
            sorted.append(list_two.pop(0))
        else:
            sorted.append(list_one.pop(0))
    return sorted + list_one + list_two


def merge_sort(items):
    if len(items) == 1:
        return items
    else:
        return merge(merge_sort(items[0:len(items)//2]), merge_sort(items[len(items)//2:len(items)]))