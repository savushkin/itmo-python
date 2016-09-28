# 1.
# Вх: список строк, Возвр: кол-во строк
# где строка > 2 символов и первый символ == последнему


def me(words):
    count = 0
    for word in words:
        if len(word) > 2 and word[0] == word[-1]:
            count += 1
    return count


# 2. 
# Вх: список строк, Возвр: список со строками (упорядочено)
# за искл всех строк начинающихся с 'x', которые попадают в начало списка.
# ['tix', 'xyz', 'apple', 'xacadu', 'aabbbccc'] -> ['xacadu', 'xyz', 'aabbbccc', 'apple', 'tix']


def fx(words):
    a = []
    b = []
    for word in words:
        if word[0] == 'x':
            a.append(word)
        else:
            b.append(word)
    a.sort()
    b.sort()
    a.extend(b)
    return a


# 3.
# Вх: список непустых кортежей,
# Возвр: список сортир по возрастанию последнего элемента в каждом корт.
# [(1, 7), (1, 3), (3, 4, 5), (2, 2)] -> [(2, 2), (1, 3), (3, 4, 5), (1, 7)]


def f3(array):
    return sorted(array, key=lambda x: x[-1])

# test(...)


if __name__ == '__main__':
    print(me(['abc', 'aba', 'scs', 'dsv', 'ss']))
    print(fx(['tix', 'xyz', 'apple', 'xacadu', 'aabbbccc']))
    print(f3([(1, 7), (1, 3), (3, 4, 5), (2, 2)]))
