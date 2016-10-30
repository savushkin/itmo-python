"""
Прочитать из файла (имя - параметр командной строки)
все слова (разделитель пробел)

Создать "Похожий" словарь который отображает каждое слово из файла
на список всех слов, которые следуют за ним (все варианты).

Список слов может быть в любом порядке и включать повторения.
например "and" ['best", "then", "after", "then", ...] 

Считаем , что пустая строка предшествует всем словам в файле.

С помощью "Похожего" словаря сгенерировать новый текст
похожий на оригинал.
Т.е. напечатать слово - посмотреть какое может быть следующим 
и выбрать случайное.

В качестве теста можно использовать вывод программы как вход.парам. для следующей копии
(для первой вход.парам. - файл)

Файл:
He is not what he should be
He is not what he need to be
But at least he is not what he used to be
  (c) Team Coach


"""

import random
import sys
import re


def mem_dict(filename):
    lexemes = []
    file = open(filename, 'rt')
    file_content = file.read()
    file.close()
    file_content = file_content.replace('\n', ' ')
    file_content = re.sub(r'[ ]{2,}', ' ', file_content)
    words = file_content.split(' ')
    for key, word in enumerate(words):
        lexeme_id = find_lexeme(word, lexemes)
        if lexeme_id == -1:
            lexemes.append((word, []))
        if key > 0:
            prev_word_lexeme_id = find_lexeme(words[key - 1], lexemes)
            lexemes[prev_word_lexeme_id][1].append(word)
    random.seed()
    first_lexeme_id = 0
    text_len = 1
    new_text = ''
    new_text += lexemes[first_lexeme_id][0]
    prev_lexeme_id = first_lexeme_id
    while not len(lexemes[prev_lexeme_id][1]) == 0 or text_len > 1000:
        current_lexeme_id = random.randint(0, len(lexemes[prev_lexeme_id][1]) - 1)
        current_lexeme = lexemes[prev_lexeme_id][1][current_lexeme_id]
        current_lexeme_id = find_lexeme(current_lexeme, lexemes)
        new_text += ' '
        new_text += current_lexeme
        prev_lexeme_id = current_lexeme_id
        text_len += 1
    return new_text


def find_lexeme(word, lexemes):
    for key, (lexeme, words) in enumerate(lexemes):
        if lexeme == word:
            return key
    return -1


def main():
    args = sys.argv[1:]
    if not args:
        print('use: file')
        sys.exit(1)
    else:
        print(mem_dict(args[0]))


if __name__ == '__main__':
    main()
