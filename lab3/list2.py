# 1.
# Вх: список чисел, Возвр: список чисел, где
# повторяющиеся числа урезаны до одного
# пример [0, 2, 2, 3] returns [0, 2, 3].


def rm_adj(nums):
    result = []
    for num in nums:
        if num not in result:
            result.append(num)
    return result


# 2. Вх: Два списка упорядоченных по возрастанию, Возвр: новый отсортированный объединенный список


def task2(list1, list2):
    list1.extend(list2)
    list1.sort()
    return list1


def test(res, expt):
    print('res: {} vs expt: {}, {}'.format(res, expt, res == expt))
    return res == expt


if __name__ == '__main__':
    test(rm_adj([0, 2, 2, 3]), [0, 2, 3])
    test(task2([1, 3, 5], [2, 4, 6]), [1, 2, 3, 4, 5, 6])
