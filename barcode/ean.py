#!/usr/bin/env python
# -*- coding: utf-8 --

'''EAN-13'''

__all__ = ('ZEan13',)

from primitives import ZPrimitiv
from errors import EZekBadChecksum, EZekInvalidLengthOfCode

class ZEan13(ZPrimitiv):
    '''EAN-13'''

    def __init__(self, size, code):
        '''@param size - размер в мм
           @param code - строка с кодом 12/13 символов'''

        ZPrimitiv.__init__(self, size)

        A = ("0001101", "0011001", "0010011", "0111101", "0100011",
             "0110001", "0101111", "0111011", "0110111", "0001011")
        B = ("0100111", "0110011", "0011011", "0100001", "0011101",
             "0111001", "0000101", "0010001", "0001001", "0010111")
        C = ("1110010", "1100110", "1101100", "1000010", "1011100",
             "1001110", "1010000", "1000100", "1001000", "1110100")
        self.groupC = C
        self.family = ((A, A, A, A, A, A), (A, A, B, A, B, B), (A, A, B, B, A, B), (A, A, B, B, B, A), (A, B, A, A, B, B),
                       (A, B, B, A, A, B), (A, B, B, B, A, A), (A, B, A, B, A, B), (A, B, A, B, B, A), (A, B, B, A, B, A))

        self.code = self._verify(code)
        self.mask = self._makemask()


    @staticmethod
    def checksum(code):
        """Compute the checksum of bar code"""
        x = 10
        # checksum based on first 12 digits.
        summ = sum(int(j) * (i % 2 * 2 + 1) for i, j in enumerate(code[:12]))
        res = (x - (summ % x)) % x

        if 0 <= res < x: return res


    def _verify(self, code):
        if not (13 >= len(code) >= 12):
            raise EZekInvalidLengthOfCode()

        ch = str(self.checksum(code))
        if len(code) == 12:
            return code + ch
        else:
            if code[12] == ch:
                return code
            else:
                raise EZekBadChecksum(code[12], ch)


    def _makemask(self):
        """ Create the binary code
        return a string which contains "0" for white bar, "1" for black bar, "L" for long bar """

        data = [int(i) for i in self.code]

        return ''.join(['L0L'] + 
                       [self.family[data[0]][i][data[i + 1]] for i in range(0, 6)] + 
                       ['0L0L0'] + 
                       [self.groupC[data[i]] for i in range (7, 13)] + 
                       ['L0L'])


    def content_svg(self):
        w = round(1.0 * self.W / (len(self.mask) + 8), 3)
        h1 = round(0.85 * self.H, 3)
        h2 = round(0.72 * self.H, 3)
        ofx = 8 * w + self.ofX

        content = ['<rect fill="black" x="%smm" y="%smm" width="%smm" height="%smm"/>' % (ofx + w * i, self.ofY, w, h1 if j == 'L' else h2)  for i, j in enumerate(self.mask) if j != '0']

        yt1 = round(self.ofY + 0.85 * self.H, 3)
        yt2 = round(self.ofY + 0.97 * self.H, 3)
 
        xt1 = round(self.ofX, 3)
        xt2 = round(self.ofX + 12.0 * w, 3)
        xt3 = round(self.ofX + 57.5 * w, 3)

        content.append('<text style="fill:black;font-family:Arial;font-size:%smm">' % round(12.0 * w, 2))        
        content.append('\t<tspan x="%smm" y="%smm">%s</tspan>' % (xt1, yt1, self.code[0].decode('utf-8')))
        content.append('</text>')
        
        content.append('<text style="fill:black;font-family:Arial;font-size:%smm">' % round(12.0 * w, 2))
        content.append('\t<tspan x="%smm" y="%smm">%s</tspan>' % (xt2, yt2, self.code[1:7].decode('utf-8')))        
        content.append('</text>')
        
        content.append('<text style="fill:black;font-family:Arial;font-size:%smm">' % round(12.0 * w, 2))
        content.append('\t<tspan x="%smm" y="%smm">%s</tspan>' % (xt3, yt2, self.code[7:13].decode('utf-8')))
        content.append('</text>')

        return u'\n'.join(content)


#==============================================================================
if __name__ == "__main__":
#    bar = EanBarCode()
    bar = ZEan13((10, 10, 20, 20), '7777777777772')
    print bar
#    #bar.getImage("9782212110708", 50, "gif")
#    #bar.getImage("700000017451", 50, "png")
#
#    b = bar.makeCode('7777777777772')
    if bar.mask <> 'L0L0111011001000101110110010001011101100100010L0L0100010010001001000100100010010001001101100L0L':
        print 'OPPAAAA'
    else:
        print 'G'

#    assert(bar.makeCode('0000000000000') == 'L0L0001101000110100011010001101000110100011010L0L0111001011100101110010111001011100101110010L0L')
#    assert(bar.makeCode('1111111111116') == 'L0L0011001001100101100110011001011001101100110L0L0110011011001101100110110011011001101010000L0L')
#    assert(bar.makeCode('2222222222222') == 'L0L0010011001001100110110011011001001100110110L0L0110110011011001101100110110011011001101100L0L')
#    assert(bar.makeCode('3333333333338') == 'L0L0111101011110101000010100001010000101111010L0L0100001010000101000010100001010000101001000L0L')
#    assert(bar.makeCode('4444444444444') == 'L0L0100011001110101000110100011001110100111010L0L0101110010111001011100101110010111001011100L0L')
#    assert(bar.makeCode('5555555555550') == 'L0L0110001011100101110010110001011000101110010L0L0100111010011101001110100111010011101110010L0L')
#    assert(bar.makeCode('6666666666666') == 'L0L0101111000010100001010000101010111101011110L0L0101000010100001010000101000010100001010000L0L')
#    assert(bar.makeCode('7777777777772') == 'L0L0111011001000101110110010001011101100100010L0L0100010010001001000100100010010001001101100L0L')
#    assert(bar.makeCode('8888888888888') == 'L0L0110111000100101101110001001000100101101110L0L0100100010010001001000100100010010001001000L0L')
#    assert(bar.makeCode('9999999999994') == 'L0L0001011001011100101110001011001011100010110L0L0111010011101001110100111010011101001011100L0L')
#
#    assert(bar.makeCode('000000000000') == 'L0L0001101000110100011010001101000110100011010L0L0111001011100101110010111001011100101110010L0L')
#    assert(bar.makeCode('111111111111') == 'L0L0011001001100101100110011001011001101100110L0L0110011011001101100110110011011001101010000L0L')
#    assert(bar.makeCode('222222222222') == 'L0L0010011001001100110110011011001001100110110L0L0110110011011001101100110110011011001101100L0L')
#    assert(bar.makeCode('333333333333') == 'L0L0111101011110101000010100001010000101111010L0L0100001010000101000010100001010000101001000L0L')
#    assert(bar.makeCode('444444444444') == 'L0L0100011001110101000110100011001110100111010L0L0101110010111001011100101110010111001011100L0L')
#    assert(bar.makeCode('555555555555') == 'L0L0110001011100101110010110001011000101110010L0L0100111010011101001110100111010011101110010L0L')
#    assert(bar.makeCode('666666666666') == 'L0L0101111000010100001010000101010111101011110L0L0101000010100001010000101000010100001010000L0L')
#    assert(bar.makeCode('777777777777') == 'L0L0111011001000101110110010001011101100100010L0L0100010010001001000100100010010001001101100L0L')
#    assert(bar.makeCode('888888888888') == 'L0L0110111000100101101110001001000100101101110L0L0100100010010001001000100100010010001001000L0L')
#    assert(bar.makeCode('999999999999') == 'L0L0001011001011100101110001011001011100010110L0L0111010011101001110100111010011101001011100L0L')
