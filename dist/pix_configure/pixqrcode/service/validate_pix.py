import re

from pixqrcode.model.pix_error import PixError
from pixqrcode.model.pix import Pix
from pixqrcode.utils.format_values import FormatValues


class ValidatePix:
    is_valid = False

    def __init__(self, pix: Pix):
        self.pix = pix

    def validate(self):
        self.name()
        self.amount()
        self.city()
        self.reference_label()
        self.key()
        self.is_valid = True
        return self.is_valid

    def name(self):
        if not self.pix.name:
            raise PixError("Nome nao informado")

        self.pix.name = FormatValues.texts(self.pix.name)
        return True

    def city(self):
        if not self.pix.city:
            raise PixError("cidade nao informada")

        self.pix.city = FormatValues.texts(self.pix.city)
        return True

    def amount(self):
        if self.pix.amount:
            self.pix.amount = FormatValues.amount(self.pix.amount)
        else:
            self.pix.amount = "0.00"
        return True

    def reference_label(self):
        if not self.pix.reference_label:
            self.pix.reference_label = "***"
        else:
            self.pix.reference_label = FormatValues.texts_no_space(self.pix.reference_label)

    def key(self):
        if not self.pix.key:
            raise PixError("telefone nao informado")

        self.pix.key = FormatValues.key(self.pix.key)
        if not re.match(r'^.55[\d]{3}', self.pix.key):
            if not re.match(r'^55[\d]{3}', self.pix.key):
                self.pix.key = f"{self.pix.key}"
            else:
                self.pix.key = f"+{self.pix.key}"

        return True
