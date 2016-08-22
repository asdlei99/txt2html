# -*- coding: utf-8 -*-

from collections import OrderedDict
import re

class HTMLHandler(object):
    def __init__(self, html_file):
        self.output = html_file
        self.patterns = OrderedDict([
        ('next_line', r'\n'),
        ('emphasis', r'\*(.+?)\*'),
        ('url', r'((http|https)://[\.a-zA-Z]+)'),
        ('mail', r'([\.a-zA-Z]+@[\.a-zA-Z]+[a-zA-Z]+)')
        ])
        
    def start(self, name):
        str = {
        'document': '<html>\n\t<head>\n\t\t<title>\n\t\t'+ self.output[:-5] +'\n\t\t</title>\n\t</head>\n\t<body>',
        'title': '\n\t\t<h1 style="color: #1ABC9C;">',
        'heading': '\n\t\t<h2 style="color: #68BE5D;">',
        'list': '\n\t\t<ul style="color: #363736;">',
        'listitem': '\n\t\t<li>',
        'paragraph': '\n\t\t<p style="color: #444;">'
        }
           
        with open(self.output, 'a') as f:
            f.write(str[name]) 
            
    def end(self, name):
        str = {
        'document': '\n\t</body>\n</html>',
        'title': '</h1>',        
        'heading': '</h2>',
        'list': '\n\t\t</ul>',
        'listitem': '</li>',
        'paragraph': '</p>'
        }
           
        with open(self.output, 'a') as f:
            f.write(str[name])
        
    def sub(self, name):
        def substitution(match):
            if name == 'next_line':
                return self.sub_next_line()
            elif name == 'emphasis':
                return self.sub_emphasis(match)
            elif name == 'url':
                return self.sub_url(match)
            elif name == 'mail':
                return self.sub_mail(match)
        return substitution
        
    def sub_next_line(self):
        return '<br />'

    def sub_emphasis(self, match):
        return '<em>%s</em>' % match.group(1)

    def sub_url(self, match):
        return '<a target="_blank" style="text-decoration: none;color: #BC1A4B;" href="%s">%s</a>' % (match.group(1), match.group(1))

    def sub_mail(self, match):
        return '<a style="text-decoration: none;color: #BC1A4B;" href="mailto:%s">%s</a>' % (match.group(1), match.group(1))
        
    def handle_block(self, block):
        for name,pattern in self.patterns.items():
            block = re.sub(pattern, self.sub(name), block)
        
        with open(self.output, 'a') as f:
            f.write(block)