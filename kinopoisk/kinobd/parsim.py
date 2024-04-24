def shell_sort(lst):
    gap = len(lst) // 2

    while gap > 0:
        for value in range(gap, len(lst)):
            current_value = lst[value]
            position = value

            while position >= gap and lst[position - gap] > current_value:
                lst[position] = lst[position-gap]
                position -= gap
                lst[position] = current_value

        gap //= 2
    return lst


def quick_sort(s):
    if len(s) <= 1:
        return s
    pivot = s[len(s) // 2]
    left = [x for x in s if x < pivot]
    center = [x for x in s if x == pivot]
    right = [x for x in s if x > pivot]
    return quick_sort(left) + center + quick_sort(right)


def binary_search(arr, target):
    low = 0
    high = len(arr) - 1

    while low <= high:
        mid = (low + high) // 2
        mid_val = arr[mid]

        if mid_val == target:
            return mid
        elif mid_val < target:
            low = mid + 1
        else:
            high = mid - 1

    return -1



print(quick_sort([-1, 2, 3,1, 1 , 0 ,-10, 10, 100, 25]))