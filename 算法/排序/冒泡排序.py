__author__ = 'shy'
__date__ = '2018/3/19 10:01'


def bubble_sort(array):
    count = len(array)
    for i in range(count):
        for j in range(count - i - 1):
            if array[j] > array[j + 1]:
                array[j], array[j + 1] = array[j + 1], array[j]
    return array


if __name__ == '__main__':
    array = [6, 4, 2, 5, 7, 9, 1, 3, 8]
    print(bubble_sort(array))
