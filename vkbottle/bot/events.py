"""
 MIT License

 Copyright (c) 2019 Arseniy Timonik

 Permission is hereby granted, free of charge, to any person obtaining a copy
 of this software and associated documentation files (the "Software"), to deal
 in the Software without restriction, including without limitation the rights
 to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
 copies of the Software, and to permit persons to whom the Software is
 furnished to do so, subject to the following conditions:

 The above copyright notice and this permission notice shall be included in all
 copies or substantial portions of the Software.

 THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
 SOFTWARE.
"""

"""
VKBOTTLE EVENTS TYPES
"""

from ..utils import Logger, make_priority_path, dict_of_dicts_merge

import re


def regex_message(text):
    escape = {ord(x): ('\\' + x) for x in r'\.*+?()[]|^$'}
    pattern = re.sub(r'(<.*?>)',  r'(?P\1.*)', text.translate(escape))
    return re.compile(pattern)


class OnMessage(object):
    def __init__(self, this):
        self.this = this
        self.processor = this.processor_message_regex

    def __call__(self, text, priority: int = 0):
        def decorator(func):
            self.processor = make_priority_path(self.processor,
                                                *[priority, regex_message(text)],
                                                func)
            return func
        return decorator

    def startswith(self, text, priority: int = 0):

        def decorator(func):

            pattern = re.sub(
                r'(<.*?>)',
                r'(?P\1.*)',
                text.translate(
                    {ord(x): ('\\' + x) for x in r'\.*+?()[]|^$'}
                )
            ) + r'.*?'

            self.processor = make_priority_path(
                  self.processor,
                  *[priority, re.compile(pattern)],
                  func
            )

            return func

        return decorator

    def regex(self, pattern, priority: int = 0):
        def decorator(func):
            self.processor = make_priority_path(self.processor,
                                                *[priority, re.compile(pattern)],
                                                func)
            return func
        return decorator

    def __repr__(self):
        return '<Do not use on-message as a variable>'


class OnMessageChat(object):
    def __init__(self, this):
        self.this = this
        self.processor = this.processor_message_chat_regex

    def __call__(self, text, priority: int = 0):
        def decorator(func):
            self.processor = make_priority_path(self.processor,
                                                *[priority, regex_message(text)],
                                                func)
            return func
        return decorator


    def startswith(self, text, priority: int = 0):
        def decorator(func):
            escape = {ord(x): ('\\' + x) for x in r'\.*+?()[]|^$'}
            pattern = re.sub(r'(<.*?>)', r'(?P\1.*)', text.translate(escape)) + r'.*?'
            self.processor = make_priority_path(self.processor,
                                                *[priority, re.compile(pattern)],
                                                func)
            return func
        return decorator

    def regex(self, regex, priority: int = 0):
        def decorator(func):
            pattern = regex
            self.processor = make_priority_path(self.processor,
                                                *[priority, re.compile(pattern)],
                                                func)
            return func
        return decorator

    def __repr__(self):
        return '<Do not use on-message as a variable>'


class OnMessageBoth(object):
    def __init__(self, this):
        self.this = this
        self.processor_message = this.processor_message_regex
        self.processor_chat = this.processor_message_regex

    def __call__(self, text, priority: int = 0):
        def decorator(func):
            self.processor_message = make_priority_path(self.processor_message,
                                                        *[priority, regex_message(text)],
                                                        func)
            self.processor_chat = make_priority_path(self.processor_chat,
                                                     *[priority, regex_message(text)],
                                                     func)
            return func
        return decorator

    def startswith(self, text, priority: int = 0):
        def decorator(func):
            escape = {ord(x): ('\\' + x) for x in r'\.*+?()[]|^$'}
            pattern = re.sub(r'(<.*?>)', r'(?P\1.*)', text.translate(escape)) + r'.*?'
            self.processor_message = make_priority_path(self.processor_message,
                                                        *[priority, re.compile(pattern)],
                                                        func)
            self.processor_chat = make_priority_path(self.processor_chat,
                                                     *[priority, re.compile(pattern)],
                                                     func)
            return func
        return decorator

    def regex(self, pattern, priority: int = 0):
        def decorator(func):
            self.processor_message = make_priority_path(self.processor_message,
                                                        *[priority, re.compile(pattern)],
                                                        func)
            self.processor_chat = make_priority_path(self.processor_chat,
                                                     *[priority, re.compile(pattern)],
                                                     func)
            return func
        return decorator

    def __repr__(self):
        return '<Do not use on-message as a variable>'


class Events:
    def __init__(self):
        self.processor_message_regex = {}
        self.processor_message_chat_regex = {}
        self.undefined_message_func = (
            lambda *args: Logger(True).warn('Add to your on-message file an on-message-undefined decorator')
        )
        self.events = {}
        self.chat_action_types = {}

        # Processors
        self.message = OnMessage(self)
        self.message_chat = OnMessageChat(self)
        self.message_both = OnMessageBoth(self)

    def get_message(self):
        print('getmewhubs', self.message.processor)
        processor = dict_of_dicts_merge(self.message.processor, self.message_both.processor_message)
        print('getmessgae', processor)
        self.processor_message_regex = processor

    def get_message_chat(self):
        processor = dict_of_dicts_merge(self.message_chat.processor, self.message_both.processor_chat)
        self.processor_message_chat_regex = processor

    def append_plugin(self, plugin):
        self.processor_message_regex = dict_of_dicts_merge(self.processor_message_regex, plugin.on.processor_message_regex)
        self.processor_message_chat_regex = dict_of_dicts_merge(self.processor_message_chat_regex, plugin.on.processor_message_chat_regex)

    def chat_action(self, type_):
        def decorator(func):
            self.chat_action_types[type_] = {'call': func}
            return func
        return decorator

    def message_undefined(self):
        def decorator(func):
            self.undefined_message_func = func
            return func
        return decorator

    def group_join(self, join_type='join'):
        def decorator(func):
            if 'group_join' not in self.events:
                self.events['group_join'] = {'rule': 'join_type', 'equal': {join_type: func}}
            else:
                self.events['group_join']['equal'][join_type] = func
            return func
        return decorator

    def group_leave(self, yourself=True):
        def decorator(func):
            event = 'group_leave'
            if event not in self.events:
                self.events[event] = {'rule': 'self', 'equal': {yourself: func}}
            else:
                self.events[event]['equal'][yourself] = func
            return func
        return decorator

    def message_reply(self):
        def decorator(func):
            event = 'message_reply'
            self.events[event] = {'rule': '=', 'equal': {'=': func}}
            return func
        return decorator

    def message_allow(self):
        def decorator(func):
            event = 'message_allow'
            self.events[event] = {'rule': '=', 'equal': {'=': func}}
            return func
        return decorator

    def message_deny(self):
        def decorator(func):
            event = 'message_deny'
            self.events[event] = {'rule': '=', 'equal': {'=': func}}
            return func
        return decorator
