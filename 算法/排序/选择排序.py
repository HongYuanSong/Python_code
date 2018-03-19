__author__ = 'shy'
__date__ = '2018/3/19 10:00'


def select_sort(array):
    count = len(array)
    for i in range(count):
        for j in range(i+1, count):
            if array[i] > array[j]:
                array[i], array[j] = array[j], array[i]
    return array


if __name__ == '__main__':
    array = [6, 4, 2, 5, 7, 9, 1, 3, 8]
    print(select_sort(array))