# -*- coding: utf-8 -*-
from flask import Flask, redirect, render_template, jsonify, request, url_for, session
from app import app
import json
import arrow
from db import Db

@app.route("/transaction/checkout", methods=['POST'])
def checkout():
    sales = []
    inventories = []

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
        )

        inventory = (
            stock - quantity,
            item_id
        )

        sales.append(item)
        inventories.append(inventory)

    transaction_id = Db().add_transaction(srp_total, selling_total)
    sales = [item + (transaction_id,) for item in sales]

    Db().add_sales(sales)
    Db().update_inventory(inventories)

    session.pop('sales', None)

    return redirect(url_for('index'))

@app.route("/transaction/view/<date>", methods=['GET'])
def view_transaction(date):
    date = arrow.get(date, "MMMM DD, YYYY")

    transactions = Db().view_transactions(date.format("YYYY-MM-DD"))
    total = sum([transaction['actual'] for transaction in transactions])

    prev_dates = arrow.Arrow.range('day', date.replace(days=-7), date)
    prev_dates = [prev_date.format("MMMM DD, YYYY") for prev_date in prev_dates]

    return render_template('transactions.html', transactions=transactions, total=total, date=date.format("MMMM DD, YYYY"), prev_dates=prev_dates)

