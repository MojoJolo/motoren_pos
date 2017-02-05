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

def search(text, text_list):
    text = set(list(text.lower()))

    search_results = []

    for t in text_list:
        search_text = set(list(''.join([t['category'], t['description'], t['name']]).lower()))

        if text.issubset(search_text):
            search_results.append(t)

    return search_results