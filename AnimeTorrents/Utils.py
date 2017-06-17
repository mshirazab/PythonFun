class IO(object):
    class Message(object):
        error = '[ERROR]   '
        added = '[ADDED]   '
        message = '[MESSAGE] '
        updated = '[UPDATED] '
        searched = '[SEARCHED]'


class HtmlBuilder(object):
    def __init__(self):
        self.__html = u''
        self.__stack = []

    def __push(self, data):
        self.__stack.append(data)

    def __pop(self):
        return self.__stack.pop()

    def open_tag(self, tag, attrs):
        data = '\n<' + tag  # opening tag
        for right, left in attrs.items():
            data += ' ' + right + '="' + left + '"'
        data += '>'
        self.__push(tag)

        data = ''.join([i if ord(i) < 128 else ' ' for i in data])
        self.__html += data

    def close_tag(self):
        tag = self.__pop()
        self.__html += '</' + tag + '>\n'

    def add_data(self, data):
        self.__html += data

    def get_html(self):
        length = len(self.__stack)
        while length > 0:
            self.close_tag()
            length = len(self.__stack)
        return self.__html
