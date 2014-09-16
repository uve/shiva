# coding: utf-8

from core.sw_base import BaseHandler

from barcode.zek_model import barcode, barcode2party

class PrintBarcode(BaseHandler):

    def get(self, param):

        code = self.get_argument("code", "")

        party = barcode2party(code)

        self.write(barcode(code, party))
        self.set_header("Content-Type", "image/svg+xml")

