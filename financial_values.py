"""Amounts are integer kuruş; decimal input rounds half up, once."""
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP
from fastapi import HTTPException


def number(value, label="Değer", maximum=Decimal("1000000000000")):
    try:
        result = Decimal(str(value if value is not None else 0))
        if not result.is_finite() or result < 0 or result > maximum:
            raise ValueError()
        return result
    except (InvalidOperation, ValueError, TypeError):
        raise HTTPException(422, f"{label} geçerli, negatif olmayan bir sayı olmalıdır.")


def kurus(value):
    return int((number(value, "Birim fiyat") * 100).quantize(Decimal("1"), rounding=ROUND_HALF_UP))


def amount(quantity, unit_kurus):
    return int((number(quantity, "Miktar") * number(unit_kurus, "Birim fiyat")).quantize(Decimal("1"), rounding=ROUND_HALF_UP))
