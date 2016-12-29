# -*- coding: utf-8 -*-
from flask import Flask, redirect, render_template, jsonify, request, url_for, session
from app import app
import json
import arrow
from db import Db
from settings import CODE
from utils import convert_code
import collections

@app.route("/transaction/checkout", methods=['POST'])
def checkout():
    sales = []
    inventories = []

    datetime = request.form.get('date')
    if datetime == '':
        datetime = arrow.now().format('YYYY-MM-DD HH:mm:ss')
    else:
        datetime = arrow.get(datetime).format('YYYY-MM-DD HH:mm:ss')

    try:
        total_items = int(request.form.get('total_items', 0))
    except:
        return "Total items not valid."

    try:
        srp_total = float(request.form.get('srp_total', 0))
        selling_total = float(request.form.get('selling_total', 0))
    except:
        return "Totals not valid."

    if total_items == 0:
        return "No item in sales."

    for i in range(0, total_items):
        item_id = request.form.get('id::{}'.format(i))

        if not item_id:
            return "[Error Transaction#24] This shouldn't happen. Conctact Jolo."

        try:
            stock = int(request.form.get('stock::{}'.format(i)))
            quantity = int(request.form.get('quantity::{}'.format(i)))
            price = float(request.form.get('price::{}'.format(i)))
            actual = float(request.form.get('actual::{}'.format(i)))
        except:
            return "[Error Transaction#31] This shouldn't happen. Conctact Jolo."

        item = (
            item_id,
            quantity,
            price,
            actual,
            session.get('user', 'Paco Roman')
        )

        inventory = (
            stock - quantity,
            item_id
        )

        sales.append(item)
        inventories.append(inventory)

    transaction_id = Db().add_transaction(srp_total, selling_total, datetime)
    sales = [item + (transaction_id,) for item in sales]

    Db().add_sales(sales)
    Db().update_inventory(inventories)

    session.pop('sales', None)

    return redirect(url_for('index'))

@app.route("/transaction/view/<date>", methods=['GET'])
def view_transaction(date):
    date = arrow.get(date, "MMMM DD, YYYY")
    show = request.args.get('show', 'no')

    transactions = Db().view_transactions(date.format("YYYY-MM-DD"))
    total = sum([transaction['actual'] for transaction in transactions])

    paco_roman_transactions = []
    gen_tinio_transactions = []

    for transaction in transactions:
        transaction['converted_code'] = convert_code(transaction['code'])

        if transaction['user'] == 'Paco Roman':
            paco_roman_transactions.append(transaction)
        else:
            gen_tinio_transactions.append(transaction)

    paco_roman_total = sum([transaction['actual'] for transaction in paco_roman_transactions])
    paco_roman_code_total = sum([transaction['quantity'] * convert_code(transaction['code']) for transaction in paco_roman_transactions])
    paco_roman_profit = float(paco_roman_total) - paco_roman_code_total
    
    try:
        paco_roman_gain = paco_roman_profit / paco_roman_code_total * 100
        paco_roman_gain = round(paco_roman_gain, 2)
    except:
        paco_roman_gain = 0

    gen_tinio_total = sum([transaction['actual'] for transaction in gen_tinio_transactions])
    gen_tinio_code_total = sum([transaction['quantity'] * convert_code(transaction['code']) for transaction in gen_tinio_transactions])
    gen_tinio_profit = float(gen_tinio_total) - gen_tinio_code_total

    try:
        gen_tinio_gain = gen_tinio_profit / gen_tinio_code_total * 100
        gen_tinio_gain = round(gen_tinio_gain, 2)
    except:
        gen_tinio_gain = 0

    prev_dates = arrow.Arrow.range('day', date.replace(days=-7), date)
    prev_dates = [prev_date.format("MMMM DD, YYYY") for prev_date in prev_dates]

    return render_template('transactions.html',
        paco_roman_transactions=paco_roman_transactions, gen_tinio_transactions=gen_tinio_transactions,
        combined_total=total,
        paco_roman_total=paco_roman_total, paco_roman_code_total=paco_roman_code_total,
        paco_roman_profit=paco_roman_profit, paco_roman_gain=paco_roman_gain,
        gen_tinio_total=gen_tinio_total, gen_tinio_code_total=gen_tinio_code_total,
        gen_tinio_profit=gen_tinio_profit, gen_tinio_gain=gen_tinio_gain,
        date=date.format("MMMM DD, YYYY"), prev_dates=prev_dates,
        show=show)

@app.route("/transaction/monthly/<month>", methods=['GET'])
def view_monthly(month):
    date = arrow.get(month, "MMMM YYYY")

    transactions = Db().view_transactions(date.format("YYYY-MM"))

    paco_roman_per_day = {}
    gen_tinio_per_day = {}

    for transaction in transactions:
        if transaction['user'] == 'Paco Roman':
            per_day = paco_roman_per_day
        else:
            per_day = gen_tinio_per_day

        day = arrow.get(transaction['date']).format("MMMM DD, YYYY")

        if day not in per_day:
            per_day[day] = {}
            per_day[day]['total'] = 0
            per_day[day]['code_total'] = 0

        per_day[day]['total'] += transaction['actual']
        per_day[day]['code_total'] += transaction['quantity'] * convert_code(transaction['code'])
        per_day[day]['profit'] = float(per_day[day]['total']) - per_day[day]['code_total']

        try:
            per_day[day]['gain'] = per_day[day]['profit'] / per_day[day]['code_total'] * 100
            per_day[day]['gain'] = round(per_day[day]['gain'], 2)
        except:
            per_day[day]['gain'] = 0

    paco_roman_per_day = collections.OrderedDict(sorted(paco_roman_per_day.items()))
    gen_tinio_per_day = collections.OrderedDict(sorted(gen_tinio_per_day.items()))

    paco_roman_total = sum([per_day['total'] for per_day in paco_roman_per_day.values()])
    paco_roman_code_total = sum([per_day['code_total'] for per_day in paco_roman_per_day.values()])
    paco_roman_profit = float(paco_roman_total) - paco_roman_code_total
    
    try:
        paco_roman_gain = paco_roman_profit / paco_roman_code_total * 100
        paco_roman_gain = round(paco_roman_gain, 2)
    except:
        paco_roman_gain = 0

    gen_tinio_total = sum([per_day['total'] for per_day in gen_tinio_per_day.values()])
    gen_tinio_code_total = sum([per_day['code_total'] for per_day in gen_tinio_per_day.values()])
    gen_tinio_profit = float(gen_tinio_total) - gen_tinio_code_total
    
    try:
        gen_tinio_gain = gen_tinio_profit / gen_tinio_code_total * 100
        gen_tinio_gain = round(gen_tinio_gain, 2)
    except:
        gen_tinio_gain = 0

    return render_template('monthly.html',
        month=date.format("MMMM YYYY"),
        paco_roman_per_day=paco_roman_per_day, gen_tinio_per_day=gen_tinio_per_day,
        paco_roman_total=paco_roman_total, paco_roman_code_total=paco_roman_code_total,
        paco_roman_profit=paco_roman_profit, paco_roman_gain=paco_roman_gain,
        gen_tinio_total=gen_tinio_total, gen_tinio_code_total=gen_tinio_code_total,
        gen_tinio_profit=gen_tinio_profit, gen_tinio_gain=gen_tinio_gain)


    # total = sum([transaction['actual'] for transaction in transactions])

    # paco_roman_transactions = []
    # gen_tinio_transactions = []

    # for transaction in transactions:
    #     if transaction['user'] == 'Paco Roman':
    #         paco_roman_transactions.append(transaction)
    #     else:
    #         gen_tinio_transactions.append(transaction)

    # paco_roman_total = sum([transaction['actual'] for transaction in paco_roman_transactions])
    # paco_roman_code_total = sum([transaction['quantity'] * convert_code(transaction['code']) for transaction in paco_roman_transactions])
    # paco_roman_profit = float(paco_roman_total) - paco_roman_code_total
    
    # try:
    #     paco_roman_gain = paco_roman_profit / paco_roman_code_total * 100
    #     paco_roman_gain = round(paco_roman_gain, 2)
    # except:
    #     paco_roman_gain = 0

    # gen_tinio_total = sum([transaction['actual'] for transaction in gen_tinio_transactions])
    # gen_tinio_code_total = sum([transaction['quantity'] * convert_code(transaction['code']) for transaction in gen_tinio_transactions])
    # gen_tinio_profit = float(gen_tinio_total) - gen_tinio_code_total

    # try:
    #     gen_tinio_gain = gen_tinio_profit / gen_tinio_code_total * 100
    #     gen_tinio_gain = round(gen_tinio_gain, 2)
    # except:
    #     gen_tinio_gain = 0

    # # profit = float(total) - code_total
    # # gain = profit / code_total * 100
    # # gain = round(gain, 2)

    # prev_dates = arrow.Arrow.range('day', date.replace(days=-7), date)
    # prev_dates = [prev_date.format("MMMM DD, YYYY") for prev_date in prev_dates]

    # return render_template('monthly.html',
    #     paco_roman_transactions=paco_roman_transactions, gen_tinio_transactions=gen_tinio_transactions,
    #     total=total, month=date.format("MMMM YYYY"),
    #     paco_roman_total=paco_roman_total, paco_roman_code_total=paco_roman_code_total,
    #     paco_roman_profit=paco_roman_profit, paco_roman_gain=paco_roman_gain,
    #     gen_tinio_total=gen_tinio_total, gen_tinio_code_total=gen_tinio_code_total,
    #     gen_tinio_profit=gen_tinio_profit, gen_tinio_gain=gen_tinio_gain)
    #     # code_total=code_total, gain=gain, profit=profit)
