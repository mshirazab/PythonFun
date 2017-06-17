import re


class Message(object):
    error = '[ERROR]   '
    added = '[ADDED]   '
    message = '[MESSAGE] '
    updated = '[UPDATED] '
    searched = '[SEARCHED]'


def remove_multiple_spaces(data):
    return re.sub('\s+', ' ', data)
