import string2

# 1.
# Входящие параметры: int <count> , 
# Результат: string в форме
# 'Number of: <count>', где <count> число из вход.парам.
#  Если число равно 10 или более, напечатать 'many'
#  вместо <count>
#  Пример: (5) -> 'Number of: 5'
#  (23) -> 'Number of: many'


def num_of_items(count):
    return 'Number of: {0}'.format(str(count) if count < 10 else 'many')


# 2. 
# Входящие параметры: string s, 
# Результат: string из 2х первых и 2х последних символов s
# Пример 'welcome' -> 'weme'.


def start_end_symbols(s):
    if len(s) > 2:
        return '{}{}{}{}'.format(s[0], s[1], s[-2], s[-1])
    else:
        return s


# 3. 
# Входящие параметры: string s,
# Результат: string где все вхождения 1го символа заменяются на '*'
# (кроме самого 1го символа)
# Пример: 'bibble' -> 'bi**le'
# s.replace(stra, strb) 


def replace_char(s):
    first_letter = s[0]
    return s if len(s) < 2 else '{}{}'.format(first_letter, s.replace(s[0], '*')[1:])


# 4
# Входящие параметры: string a и b, 
# Результат: string где <a> и <b> разделены пробелом 
# а превые 2 симв обоих строк заменены друг на друга
# Т.е. 'max', pid' -> 'pix mad'
# 'dog', 'dinner' -> 'dig donner'


def str_mix(a, b):
    a_first_letters = a[0:2]
    b_first_letters = b[0:2]
    return '{}{} {}{}'.format(b_first_letters, a[2:], a_first_letters, b[2:])


# # Provided simple test() function used in main() to print
# # what each function returns vs. what it's supposed to return.


def test(res, expt):
    print('res: {} vs expt: {}, {}'.format(res, expt, res == expt))
    return res == expt


if __name__ == '__main__':
    test(num_of_items(5), 'Number of: 5')
    test(num_of_items(23), 'Number of: many')
    test(start_end_symbols('mishka'), 'mika')
    test(start_end_symbols('w'), 'w')
    test(replace_char('bibble'), 'bi**le')
    test(str_mix('max', 'pid'), 'pix mad')
    test(str_mix('dog', 'dinner'), 'dig donner')
    test(string2.v('mishka'), 'mishkaing')
    test(string2.v('mishkaing'), 'mishkaingly')
    test(string2.v('mis'), 'mis')
    test(string2.nb('This music is not so bad!'), 'This music is good!')
