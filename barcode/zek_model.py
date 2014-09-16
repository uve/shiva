#!/usr/bin/env python
# -*- coding: utf-8 --

'''Высокоуровневые шняги для генерации картинок.
Пока только SVG'''

__all__ = ('mm2pix',
           'badge', 'badge_size',
           'cell', 'cell_size',
           'pallet', 'pallet_size',
           'party', 'party_size',
           'barcode2depart_sid', 'depart_uid2barcode',
           'barcode2cellinfo', 'cellinfo2barcode',
           'barcode2pallet', 'pallet2barcode',
           'barcode2party', 'party2barcode')

from barcode import render, EZInvalidBarcode, ZEan13, ZFillRect, ZRect, ZText, ZImage_UP, ZImage_Umbrel, ZImage_Glaz

import textwrap

#=============================================================================#
def mm2pix(mm):
    '''
    Переводчик мм в пиксели.
    @param mm - int или float или list/tule с числами
    '''
    if isinstance(mm, (list, tuple)):
        return type(mm)([mm2pix(i) for i in mm])

    return int(round(mm * 3.75))

#=============================================================================#
badge_size = (90, 50)  # размер бэйджика в мм.
def badge(bar_code, fio, type_result='svg'):
    '''Бэйджик'''
    return render(type_result, badge_size,
                  ZRect(badge_size),
                  ZEan13((7, 20, 74, 28), bar_code),
                  ZFillRect((1, 18, 88, 0.5)),
                  ZText((1, 1, 88, 15), fio, align='center')
                  )


#=============================================================================#
cell_size = (96, 70)  # размер этикеток на ячейки в мм.
def cell(line, row, floor, depart, type_result='svg'):
    '''Этикетка на ячейки'''
    
    ztext = '%02d-%02d-%1d' % (int(line), int(row), int(floor))
    zbarcode = cellinfo2barcode(int(depart), int(line), int(floor), int(row))
    
    return render(type_result, cell_size,
                  ZRect((96, 70)),
                  ZText((96, 26), ztext, align='center', weight=True),
                  ZEan13((7, 30, 80, 37), zbarcode),
                  )



#=============================================================================#
pallet_size = (49, 36)  # размер этикеток на палеты в мм.
def pallet(pallet_id, type_result='svg'):
    '''Этикетка на палеты'''
    return render(type_result, pallet_size,
                  ZText((49, 6), 'pallet:%s' % pallet_id),
                  ZEan13((1, 8, 47, 26), pallet2barcode(pallet_id)),
                  )

#=============================================================================#
party_size = (49, 36) # размер этикетки в мм.
def barcode(code, party='', rem='', type_result='svg'):
    '''Партионные этикетки'''

    title = 'party'
    if code.startswith('8'):
        title = 'extra_party'

    return render(type_result, party_size,
                  ZText((0, 0.5, 42.7, 5), '%s:%s' % (title,party)),
                  ZText((0, 0.5, 49, 5), rem, align='right', weight=True),
                  ZEan13((1, 8, 47, 26), code),
                  )


#=============================================================================#
party_size = (49, 36) # размер этикетки в мм.
def party(party_id, rem='', type_result='svg'):
    '''Партионные этикетки'''
    return render(type_result, party_size,
                  ZText((0, 0.5, 42.7, 5), 'party:%s' % party_id),
                  ZText((0, 0.5, 49, 5), rem, align='right', weight=True),
                  ZEan13((1, 8, 47, 26), party2barcode(party_id)),
                  )

def party2(party_id, num, name, type_result='svg'):
    '''Партионные этикетки имени Мантурова'''    
  
    name = name.decode('utf-8')  
    num = num.decode('utf-8')  
    
    if len(name) > 64:
        name = [name[:33], name[33:66], name[66:]]
        fs = 2.6
    elif len(name) > 32:
        name = [name[:32], name[32:]]
        fs = 3.0
    else:
        fs = 3.5

    return render(type_result, party_size,
                  # ZRect(party_size),
                  ZText((0, 0, 48, 9), name, font_size=fs),
                  ZFillRect((0, 9.1, 49, 0.2)),
                  ZText((0, 9.5, 42.7, 5), u'партия: %s' % num),

                  ZEan13((1, 16, 45, 19), party2barcode(party_id)),
                  )


#=============================================================================#
# box_label_size = (90, 105) # размер этикетки в мм.
box_label_size = (110, 95)  # размер этикетки в мм.
def box_label(num, forwarder, phone, address, name, phone_to, place, item, isUp=True, isGlaz=True, isUmbrell=True, type_result='svg'):
    '''Транспортные этикетки'''
    def gn():
        x = (1, 16, 32)
        i = 0
        while True:
            yield x[i]
            i += 1
            i = i % (len(x))
    gx = gn()
    f1 = 4; f2 = 5.6

    # forwarder
    # recipient
   
    try:
        if forwarder and len(forwarder) > 50:
            forwarder = textwrap.wrap(forwarder, 55, break_long_words=False)
    except:
        pass
    try:
        if address and len(address) > 50:
            address = textwrap.wrap(address, 85, break_long_words=False)
    except:
        pass
    
    
    data = [ZRect(box_label_size),
           ZText((1, 1, 20, 6), u'Заказ:', font_size=f1),
           ZText((18, 1, 70, 6), num, align='right', weight=True),

           ZText((1, 8.5, 28, 6), u'Отправитель:', font_size=f1),
           
           
           ZText((4, 15, 88, 6), forwarder, font_size=f1),
           ZText((4, 29, 88, 6), phone, font_size=f1),

           ZFillRect((1, 37, 88, 0.5)),

           ZFillRect((1, 56.5, 88, 0.5)),

           ZText((1, 55, 28, 6), u'Получатель:', font_size=f1),
           ZText((4, 62, 88, 6), address, align="left", font_size=f1),
           ZText((4, 75, 88, 6), name, font_size=f1),
           ZText((4, 80, 88, 6), phone_to, font_size=f1),

           ZText((1, 85, 28, 6), u'Место:', font_size=f1),
           ZText((17, 85, 28, 6), place, font_size=f2),

           ZText((45, 85, 28, 6), u'Отправка:', font_size=f1),
           ZText((67, 85, 28, 6), item, font_size=f2)]

    if isUp: data.append(ZImage_UP((gx.next(), 39, 15, 16)))
    if isGlaz: data.append(ZImage_Glaz((gx.next(), 39, 15, 16)))
    if isUmbrell: data.append(ZImage_Umbrel((gx.next(), 39, 15, 16)))

    return render(type_result, box_label_size, *data)



#=============================================================================#
assembly_bar_size = (170, 80)  # размер этикетки в мм.
def assembly_bar_label(assembly_id, type_result='svg'):
    '''Штрихкод для сборочного листа'''
    return render(type_result, assembly_bar_size,
                  ZEan13(assembly_bar_size, assembly2barcode(assembly_id)),
                  )





#=============================================================================#
def barcode2depart_sid(barcode):
    '''1 (4)depart (7)id
    :return tuple(depart_id, sotrud_id)'''
    try:
        barcode = str(barcode)[:12]
        if barcode[0] != '1' or len(barcode) != 12:
            raise EZInvalidBarcode(barcode)
        return int(barcode[1:5]), int(barcode[5:])
    except EZInvalidBarcode:
        return 0, 0

def depart_uid2barcode(depart, sid):
    '''1 (4)depart (7)id'''
    return '1%04d%07d' % (depart, sid)

#=============================================================================#
def barcode2cellinfo(barcode):
    '''Штрихкод -> tuple(департамент, стеллаж, этаж, ячейка) 
   3`123456`789012   (департамент 1234, стеллаж 567, этаж 8, ячейка 901, контрольная сумма 2)'''
    try:
        barcode = str(barcode)[:12]
        if barcode[0] != '3' or len(barcode) != 12:
            raise EZInvalidBarcode(barcode)
        return int(barcode[1:5]), int(barcode[5:8]), int(barcode[8:9]), int(barcode[9:12])
    except EZInvalidBarcode: return 0, 0, 0, 0
    except ValueError: return 0, 0, 0, 0

def cellinfo2barcode(depart, stelag, polka, cell):
    '''tuple(департамент, стеллаж, этаж, ячейка) -> Штрихкод'''
    return '3%04d%03d%01d%03d' % (depart, stelag, polka, cell)


#=============================================================================#
def barcode2pallet(barcode):
    '''Штрихкод -> ID палеты 
    2`123456`789012   (id - 12345678901, контрольная сумма 2)'''
    try:
        barcode = str(barcode)[:12]
        if barcode[0] != '2' or len(barcode) != 12:
            raise EZInvalidBarcode(barcode)
        return int(barcode[1:])
    except EZInvalidBarcode: return 0
    except ValueError: return 0


def pallet2barcode(pallet_id):
    '''ID палеты -> Штрихкод'''
    return '2%011d' % pallet_id

#=============================================================================#
def barcode2party(barcode):
    '''Штрихкод -> ID партии 
    7`123456`789012   (id - 12345678901, контрольная сумма 2)'''
    try:
        print barcode
        barcode = str(barcode)[:12]
        if not barcode[0] in ['7', '8'] or len(barcode) != 12:
            raise EZInvalidBarcode(barcode)
        print int(barcode[1:])        
        return int(barcode[1:])
    except EZInvalidBarcode: return 0
    except ValueError: return 0

def party2barcode(party_id, start='7'):
    '''ID партии -> Штрихкод'''
    return '%s%011d' % (start, int(party_id))


#=============================================================================#
def barcode2assembly(barcode):
    '''Штрихкод -> ID сборочного листа 
    5`123456`789012   (id - 12345678901, контрольная сумма 2)'''
    try:
        barcode = str(barcode)[:12]
        if barcode[0] != '5' or len(barcode) != 12:
            raise EZInvalidBarcode(barcode)
        return int(barcode[1:])
    except EZInvalidBarcode: return 0
    except ValueError: return 0

def assembly2barcode(party_id):
    '''ID сборочного листа -> Штрихкод'''
    return '5%011d' % party_id

# A4 - 2480x3508
#=============================================================================#
if __name__ == "__main__":
    # z = badge("700000017451", u'Пушкин А.С.')
    # z = cell(81, 60, 1, 3)
    # z = pallet(1234567890)
    # z = party(17451, rem=u'БТК')
    # z = party2(17451, [u'товара-товара', u'бла-бла-бла'])

    # z = party2(17451, '"Тунгалаг" (Свежесть) балансирующий бальзам для жирной и комбинированной кожи')
    # z = party2(17451, '"Тунгалаг" (Свежесть) балансирующий бальзам для жирной и 12345=+')

    # isUp=True, isGlaz=True, isUmbrell=True
    # z = box_label(u'K-8615\\400580001',
    #             [u'ООО "ФинСиб СД"', u'76-22-71'],
    #             [u'Лучегорск, мкрн7, д.4б', u'Дубицкая Г.В.,ИП', u'(42357)-22-6-77'],
    #              u'1', u'0002')
    z = assembly_bar_label(3)

    print type(z), z

    myfile = open("C:\\Shiva\\shiva_dhx\\src\\shiva\\ean13_test3.svg", "w")
    print >> myfile, z
    myfile.close()
    print 'OK'
