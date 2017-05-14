# coding: utf-8
# Copyright (c) Qotto, 2017

from decimal import Context
from decimal import Decimal
from decimal import DecimalException
from django.core.exceptions import ValidationError
from django.db.models import DecimalField
from django.utils.encoding import force_text

class RoundedDecimalField(DecimalField):
    """
    A RoundedDecimalField field acts like a normal field, except that it accepts any decimal,
    and automatically converts it to the proper format.
    """
    def to_python(self, value):
        if value in self.empty_values:
            return None
        value = force_text(value).strip()
        try:
            if self.max_digits:
                value = Decimal(value)
            else:
                value = Context(self.max_digits).create_decimal(value)
            if self.decimal_places:
                value = value.quantize(Decimal('.'+'0'*self.decimal_places))
        except DecimalException:
            raise ValidationError(self.error_messages['invalid'], code='invalid')
        return value
