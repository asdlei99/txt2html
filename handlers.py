# -*- coding: utf-8 -*-

from collections import OrderedDict
import re

class HTMLHandler(object):
    def __init__(self, html_file):
        self.output = html_file
        self.patterns = OrderedDict([
        ('emphasis', r'\*(.+?)\*'),
        ('url', r'((http|https)://[\.a-zA-Z]+)'),
        ('mail', r'([\.a-zA-Z]+@[\.a-zA-Z]+[a-zA-Z]+)')
        ])
        
    def start(self, name):
        str = ''
        if name == 'document':
            str = '<html>\n\t<head>\n\t\t<title>\n\t\tShiYanLou\n\t\t</title>\n\t</head>\n\t<body>'
        elif name == 'paragraph':
            str = '\n\t\t<p style="color: #444;">'
        elif name == 'heading':
            str = '\n\t\t<h2 style="color: #68BE5D;">'
        elif name == 'list':
            str = '\n\t\t<ul style="color: #363736;">'
        elif name == 'listitem':
            str = '\n\t\t<li>'
        elif name == 'title':
            str = '\n\t\t<h1 style="color: #1ABC9C;">'
           
        with open(self.output, 'a') as f:
            f.write(str) 
            
    def end(self, name):
        str = ''
        if name == 'document':
            str = '\n\t</body>\n</html>'
        elif name == 'paragraph':
            str = '</p>'
        elif name == 'heading':
            str = '</h2>'
        elif name == 'list':
            str = '\n\t\t</ul>'
        elif name == 'listitem':
            str = '</li>'
        elif name == 'title':
            str = '</h1>'
           
        with open(self.output, 'a') as f:
            f.write(str)
        
    def sub(self, name):
        def substitution(match):
            if name == 'emphasis':
                return self.sub_emphasis(match)
            elif name == 'url':
                return self.sub_url(match)
            elif name == 'mail':
                return self.sub_mail(match)
        return substitution

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