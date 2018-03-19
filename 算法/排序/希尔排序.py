__author__ = 'shy'
__date__ = '2018/3/19 11:29'


def shell_sort(array):
    count = len(array)
    gap = count//2
    while gap > 0:
        for i in range(gap, count):
            j = i - gap
            while array[i] <= array[j] and j >= 0:
                array[i], array[j] = array[j], array[i]
                i -= gap
                j -= gap
                j -= 1
        gap = gap//2
    return array


if __name__ == '__main__':
    array = [6, 4, 2, 5, 7, 9, 1, 3, 8]
    print(shell_sort(array))