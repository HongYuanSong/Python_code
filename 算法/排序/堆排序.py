__author__ = 'shy'
__date__ = '2018/3/19 10:35'


def create_max_heap(array, start, end):
    # 创建最大堆
    while True:
        left = 2 * start + 1
        if left > end:
            break
        if left + 1 <= end and array[left] < array[left+1]:
            left += 1
        if array[start] < array[left]:
            array[start], array[left] = array[left], array[start]
            start = left
        else:
            break


def heap_sort(array):
    count = len(array)
    # 假设第一个元素索引从0开始
    last_node_parent = count//2 - 1

    for i in range(last_node_parent, -1, -1):
        # 自下而上生成最大堆
        create_max_heap(array, i, count-1)

    for j in range(count-1, 0, -1):
        array[0], array[j] = array[j], array[0]
        # 自上而下再生成一次最大堆
        create_max_heap(array, 0, j-1)

    return array


if __name__ == '__main__':
    array = [6, 4, 2, 5, 7, 9, 1, 3, 8]
    print(heap_sort(array))