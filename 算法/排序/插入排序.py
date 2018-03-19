__author__ = 'shy'
__date__ = '2018/3/19 10:00'


def insert_sort(array):
    count = len(array)
    for i in range(1, count):
        j = i-1
        key = array[i]
        while j >= 0:
            if array[j] > key:
                array[j+1] = array[j]
                array[j] = key
            j -= 1
    return array


if __name__ == '__main__':
    array = [6, 4, 2, 5, 7, 9, 1, 3, 8]
    print(insert_sort(array))