__author__ = 'shy'
__date__ = '2018/3/19 11:53'


def iterative_binary_search(array, target):
    count = len(array)
    low = 0
    high = count - 1

    while low <= high:
        mid = (low + high) // 2
        if target < array[mid]:
            high = mid - 1
        elif target > array[mid]:
            low = mid + 1
        else:
            return mid


def recursive_binary_search(array, target):
    if len(array) == 0:
        return False
    else:
        middle = len(array) // 2
        if target == array[middle]:
            return middle
        elif target < array[middle]:
            return recursive_binary_search(array[:middle], target)
        else:
            return recursive_binary_search(array[middle + 1:], target)


if __name__ == '__main__':
    array = [1, 2, 3, 4, 5, 6, 7, 8, 9, ]
    # iterative_binary_search(array, 6)
    print(recursive_binary_search(array, 3))