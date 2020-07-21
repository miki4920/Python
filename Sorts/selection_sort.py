def selection_sort(items):
    for i in range(0, len(items)):
        min = items[i]
        min_index = i
        for j in range(i + 1, len(items)):
            if items[j] < min:
                min = items[j]
                min_index = j
        items[i], items[min_index] = items[min_index], items[i]
    return items