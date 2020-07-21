def insertion_sort(items):
    for i in range(0, len(items)):
        min = items[i]
        min_index = i
        for j in range(i+1, len(items)):
            if items[j] < min:
                min = items[j]
                min_index = j
        items.insert(i, items.pop(min_index))
    return items