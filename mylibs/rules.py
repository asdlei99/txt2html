# -*- coding: utf-8 -*-

class HTMLRule(object):
    def action(self, block, handler):
        handler.start(self.type)
        handler.handle_block(block)
        handler.end(self.type)
        return True
        
class HeadingRule(HTMLRule):
    type = 'heading'
    def judge(self, block):
        return block[0] == block[1] == '#' and not '\n' in block and len(block) <= 30 and not block[-1] == ':'
        
    def action(self, block, handler):
        handler.start(self.type)
        handler.handle_block(block.strip('# '))
        handler.end(self.type)
        return True
        
class TitleRule(HeadingRule):
    type = 'title'
    first = True
    def judge(self, block):
        if not self.first:
            return False
        self.first = False
        return HeadingRule.judge(self, block)
        
class ListItemRule(HTMLRule):
    type = 'listitem'
    def judge(self, block):
        return block[0] == '-'
        
    def action(self, block, handler):
        handler.start(self.type)
        handler.handle_block(block[1:].strip())
        handler.end(self.type)
        return True
        
class ListRule(ListItemRule):
    type = 'list'
    inside = False
    def judge(self, block):
        return True
        
    def action(self, block, handler):
        if not self.inside and ListItemRule.judge(self, block):
            handler.start(self.type)
            self.inside = True
        elif self.inside and not ListItemRule.judge(self, block):
            handler.end(self.type)
            self.inside = False
        return False
        
class ParagraphRule(HTMLRule):
    type = 'paragraph'
    def judge(self, block):
        return True