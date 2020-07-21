def bubble_sort(items):
    for i in range(0, len(items)):
        for j in range(0, len(items)-1-i):
            if items[j] > items[j+1]:
                items[j], items[j+1] = items[j+1], items[j]
    return items