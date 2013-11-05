# coding: utf-8

class EZekBadChecksum(Exception):
    def __str__(self): return "Checksums dont match: %s" % self.args


class EZekInvalidLengthOfCode(Exception):
    def __str__(self): return "Invalid length of code"


class EZekNoData(Exception):
    def __str__(self): return "No data for rendering"


class EZekAbstractMethod(Exception):
    def __str__(self): return "Abstract method not available"


class EZUnknownFormat(Exception):
    def __str__(self): return 'Unknown format: "%s"' % self.args[0]


class EZBadSize(Exception):
    def __str__(self): return "Bad size"


class EZInvalidBarcode(Exception):
    def __str__(self): return 'Invalid Barcode: "%s"' % self.args[0]
