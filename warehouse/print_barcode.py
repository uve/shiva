# coding: utf-8

from core.sw_base import BaseHandler

from barcode.zek_model import barcode

class PrintBarcode(BaseHandler):

    def get(self, param):

        code = self.get_argument("code", None)

        self.write(barcode(code))
        self.set_header("Content-Type", "image/svg+xml")

