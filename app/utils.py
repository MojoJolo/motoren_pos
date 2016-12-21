# -*- coding: utf-8 -*-
from settings import CODE

def convert_code(item_code):
    if item_code == None:
        return 0.0

    item_code = item_code.upper()
    price = "0"

    for letter in item_code:
        try:
            equivalent = CODE.index(letter) + 1
        except:
            continue

        if equivalent == 10:
            equivalent = 0

        price += str(equivalent)

    price = price[:-2] + "." + price[-2:]

    return float(price)