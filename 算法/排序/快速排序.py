__author__ = 'shy'
__date__ = '2018/3/19 10:55'


# 方法一：lambda表达式实现

# quick_sort = lambda array: array if len(array) <= 1 else quick_sort([i for i in array[1:] if i <= array[0]]) + \
#             [array[0]] + quick_sort([i for i in array[1:] if i > array[0]])
#
# if __name__ == '__main__':
#     array = []
#     print(quick_sort(array))

# 方法二：pythonic（随机取位置）

# import random
#
#
# def quick_sort(array):
#     left = []
#     right = []
#     count = len(array)
#
#     if count <= 1:
#         return array
#     r = random.randint(0, count-1)
#     for i in range(0, count):
#         if array[i] < array[r]:
#             left.append(array[i])
#         else:
#             right.append(array[i])
#     return quick_sort(left) + quick_sort(right)
#
#
# if __name__ == '__main__':
#     array = [6, 4, 2, 5, 7, 9, 1, 3, 8]
#     print(quick_sort(array))


# 方法三：传统方法

def q_sort(arr, first, last):
    if first < last:
        target = partition(arr, first, last)

        q_sort(arr, first, target)
        q_sort(arr, target + 1, last)
    else:
        return


def partition(arr, first, last):
    start = first - 1
    for i in range(first, last):
        if arr[i] <= arr[last]:
            start = start + 1
            arr[start], arr[i] = arr[i], arr[start]
    arr[start + 1], arr[last] = arr[last], arr[start + 1]
    return start


if __name__ == '__main__':
    array = [6, 4, 2, 5, 7, 9, 1, 3, 8]
    q_sort(array, 0, len(array)-1)
    print(array)
