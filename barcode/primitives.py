# coding: utf-8

'''Графические примитивы: прямоугольник, текст и пр.'''

__all__ = ('ZRect', 'ZFillRect', 'ZText')

from errors import EZekAbstractMethod, EZBadSize

#=============================================================================#
class ZPrimitiv:
    '''Базовый класс графических примитивов'''

    def __init__(self, size):
        '''@param size - размер примитива в мм - 
           tuple([left_offset, top_offset],  width, heigh)'''

        # print size
        
        if len(size) == 2:
            self.ofX = self.ofY = 0
            self.W, self.H = size
        elif len(size) == 4:
            self.ofX, self.ofY, self.W, self.H = size
        else:
            raise EZBadSize()

    def content_svg(self):
        raise EZekAbstractMethod

#    def content_png(self, canvas):
#        raise EZekAbstractMethod

#=============================================================================#
class ZRect(ZPrimitiv):
    '''Прямоугольник'''
    def __init__(self, size, stroke=0.3):
        '''@param stroke - толщина линии'''

        ZPrimitiv.__init__(self, size)
        self.WS = stroke

    def content_svg(self):
        return '<rect fill="none" x="%smm" y="%smm" width="%smm" height="%smm" stroke="black" stroke-width="%smm"/>' % (self.ofX, self.ofY, self.W - self.WS, self.H - self.WS, self.WS)

#=============================================================================#
class ZFillRect(ZPrimitiv):
    '''Заполненный прямоугольник'''

    def content_svg(self):
        return '<rect fill="black" x="%smm" y="%smm" width="%smm" height="%smm"/>' % (self.ofX, self.ofY, self.W, self.H)

#=============================================================================#
def _norm_txt(txt):
    if isinstance(txt, basestring):
        return txt
    elif isinstance(txt, (tuple, list)):
        return [_norm_txt(i) for i in txt]
    elif txt is None:
        return ''

    return str(txt)


class ZText(ZPrimitiv):
    '''Текст'''

    def __init__(self, size, text, align='left', weight=False, font_size=0):
        '''
        @param size - размер в мм tuple([left_offset, top_offset],  width, heigh)
        @param text - текст
        @param align - выравнивание текста: 'left', 'center', 'right'
        @param weight - если True - жирное написание
        @param font_size - размер шрифта. если 0 - высчитывается по size/text 
        '''
        
        ZPrimitiv.__init__(self, size)
        

            
        self.text = _norm_txt(text)
        self.anc = {'left':'start', 'center':'middle', 'right':'end'}[align]
        self.we = weight
        self.fs = font_size

    def content_svg(self):
        if not self.text: return ''           
            
        if self.anc == 'middle': x2 = self.ofX + self.W / 2
        elif self.anc == 'end':  x2 = self.ofX + self.W
        else:                    x2 = self.ofX

        ss = 'font-weight:bold;' if self.we else ''

        if isinstance(self.text, (list, tuple)):
            h = self.H / len(self.text)
            fs = self.fs or round(min(1.3 * h, 1.7 * self.W / len(self.text)) , 2)

            t = [i for i in self.text if i]
            
            try:
                t = '\n'.join('\t<tspan x="%smm" y="%smm">%s</tspan>' % (x2, self.ofY + 1.2 * fs * (0.8 + i), j.decode('utf-8')) for i, j in enumerate(t))
            except:
                t = '\n'.join('\t<tspan x="%smm" y="%smm">%s</tspan>' % (x2, self.ofY + 1.2 * fs * (0.8 + i), j) for i, j in enumerate(t))
                
            return '<text style="fill:black;font-family:Arial;font-size:%smm">\n%s</text>' % (fs, t)
        else:
            fs = self.fs or round(min(1.3 * self.H, 1.7 * self.W / len(self.text)) , 1)
            
            try:
                res = '<text style="fill:black;font-family:Arial;text-anchor:%s;font-size:%smm;%s" x="%smm" y="%smm">%s</text>' % (self.anc, fs, ss, x2, self.ofY + self.H, self.text.decode('utf-8'))
            except:
                res = '<text style="fill:black;font-family:Arial;text-anchor:%s;font-size:%smm;%s" x="%smm" y="%smm">%s</text>' % (self.anc, fs, ss, x2, self.ofY + self.H, self.text)
                
            return res
