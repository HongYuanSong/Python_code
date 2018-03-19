__author__ = 'shy'
__date__ = '2018/3/19 11:53'


def binary_search(array, item):
    count = len(array)
    low = 0
    high = count - 1

    while low <= high:
        mid = (low + high) // 2
        if item < array[mid]:
            high = mid - 1
        elif item > array[mid]:
            low = mid + 1
        else:
            print(mid)
            return


if __name__ == '__main__':
    array = [1, 2, 3, 4, 5, 6, 7, 8, 9, ]
    binary_search(array, 6)
