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


def shell_sort(items, gap=3):
    sub_lists_count = len(items) // gap
    sub_lists = []
    merged_list = []
    for i in range(0, sub_lists_count):
        sub_list = []
        for j in range(0, sub_lists_count):
            index = i + j * gap
            sub_list.append(items[index])
        sub_list = insertion_sort(sub_list)
        sub_lists.append(sub_list)
    for i in range(0, sub_lists_count):
        for j in range(0, sub_lists_count):
            merged_list.append(sub_lists[j][i])
    return insertion_sort(merged_list)