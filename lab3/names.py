import sys
from html.parser import HTMLParser


class MyHTMLParser(HTMLParser):
    state = 'start'
    rankedNameList = []
    rank = 0
    name = ''

    def handle_starttag(self, tag, attrs):

        if tag == 'html':
            self.state = 'start'

        if tag == 'table' and self.state == 'start':
            for attr in attrs:
                if attr[0] == 'summary' and attr[1] == 'Popularity for top 1000':
                    del self.rankedNameList[:]
                    self.state = 'table_detected'

        if tag == 'tr' and self.state == 'table_detected':
            self.state = 'row_detect'

        if tag == 'td':
            if self.state == 'row_detect':
                self.state = 'rank'
            if self.state == 'rank_end':
                self.state = 'male_name'
            if self.state == 'male_name_end':
                self.state = 'female_name'

    def handle_endtag(self, tag):
        if tag == 'html':
            self.state = 'stop'
        if tag == 'td':
            if self.state == 'rank':
                self.state = 'rank_end'
            if self.state == 'male_name':
                self.state = 'male_name_end'
            if self.state == 'female_name':
                self.state = 'female_name_end'
            if self.state == 'female_name_end':
                self.state = 'table_detected'
        if tag == 'table' and self.state == 'table_detected':
            self.state = 'end_table'
            del self.rankedNameList[-1]

    def handle_data(self, data):
        if self.state == 'rank':
            self.rank = data
        if self.state == 'male_name':
            self.name = data
            self.rankedNameList.append([self.rank ,self.name])
        if self.state == 'female_name':
            self.name = data
            self.rankedNameList.append([self.rank ,self.name])


def extr_name(filename):
    file = open(filename, 'rt')
    html = file.read()
    file.close()
    parser = MyHTMLParser()
    parser.feed(html)
    """
    Вход: nameYYYY.html, Выход: список начинается с года, продолжается имя-ранг в алфавитном порядке.
    '2006', 'Aaliyah 91', Aaron 57', 'Abagail 895', ' и т.д.
    """
    return parser.rankedNameList


def main():
    args = sys.argv[1:]
    if not args:
        print('use: [--file] file [file ...]')
        sys.exit(1)
    else:
        if args[0] == '--file':
            args = args[1:]

        output = ''
        output2 = ''
        for filename in args:
            output += '\''+filename[4:8]+'\''
            output2 += filename + '\n'
            tmp = extr_name(filename)
            count = 0
            for name in tmp:
                if count < 20:
                    if count % 2 == 0:
                        output2 += '{0:.0f}'.format(count / 2 + 1)
                        output2 += '\n'
                    output2 += name[1]+'\n'
                else:
                    output2 += '\n'
                    break
                count += 1


            tmp.sort(key=lambda i: i[1])
            for name in tmp:
                output += ', \'' + name[1] + ' ' + name[0] + '\''
            output += '\n'

        print(output)
        print(output2)



    # для каждого переданного аргументом имени файла, вывести имена  extr_name

        # напечатать ТОП-10 муж и жен имен из всех переданных файлов


if __name__ == '__main__':
    main()
