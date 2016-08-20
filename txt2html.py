# -*- coding: utf-8 -*-

import argparse, rules, handlers

argparser = argparse.ArgumentParser()
argparser.add_argument('file', help='the text file')
argparser.add_argument('-o', '--output', help='the filename of the output, default: output.html')
args = argparser.parse_args()

def blocks(file):
    block = []
    for line in file:
        if line.strip():
            block.append(line)
        elif block:
            yield ''.join(block).strip()
            block = []
    if block:
        yield ''.join(block).strip()
        
class TextParser(object):
    def __init__(self, html_handler):
        self.handler = html_handler
        self.rules = []
        self.addRule(rules.ListRule())
        self.addRule(rules.ListItemRule())
        self.addRule(rules.TitleRule())
        self.addRule(rules.HeadingRule())
        self.addRule(rules.ParagraphRule())
        
    def addRule(self, rule):
        self.rules.append(rule)
    
    def parse(self, file):
        self.handler.start('document')
        for block in blocks(file):
            for rule in self.rules:
                if rule.judge(block):
                    next = rule.action(block, self.handler)
                    if next:
                        break
        self.handler.end('document')
        
if __name__ == '__main__':
    html_file = args.output if args.output else 'output.html'
    html_handler = handlers.HTMLHandler(html_file)
    text_parser = TextParser(html_handler)
    with open(args.file, 'r') as text_file:
        text_parser.parse(text_file)