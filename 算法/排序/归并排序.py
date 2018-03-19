__author__ = 'shy'
__date__ = '2018/3/19 11:36'


def merge(left, right):
    i, j = 0, 0
    res = []
    while i < len(left) and j < len(right):
        if left[i] < right[j]:
            res.append(left[i])
            i += 1
        else:
            res.append(right[j])
            j += 1
    res += left[i:]
    res += right[j:]
    return res


def merge_sort(array):
    count = len(array)
    mid = count//2
    if count <= 1:
        return array
    left = merge_sort(array[:mid])
    right = merge_sort(array[mid:])
    return merge(left, right)


if __name__ == '__main__':
    array = [6, 4, 2, 5, 7, 9, 1, 3, 8]
    print(merge_sort(array))

