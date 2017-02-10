# -*- coding: utf-8 -*-
from flask import Flask, redirect, render_template, jsonify, request, url_for, session
from app import app
import json
import arrow
from db import Db

@app.route("/transfer/view", methods=['GET'])
def view_transfer():
    date_today = request.args.get('date')

    if date_today:
        date_today = arrow.get(date_today, "MMMM DD, YYYY")
    else:
        date_today = arrow.now()

    prev_dates = arrow.Arrow.range('day', date_today.replace(days=-7), date_today)
    prev_dates = [prev_date.format("MMMM DD, YYYY") for prev_date in prev_dates]
    prev_dates.reverse()
    prev_dates = prev_dates[1:]

    date = date_today.format("YYYY-MM-DD")

    gen_tinio_transfers = Db().get_transfers(date, "Gen. Tinio")
    paco_roman_transfers = Db().get_transfers(date, "Paco Roman")

    return render_template('transfers.html', date=date_today.format("MMMM DD, YYYY"), prev_dates=prev_dates,
        gen_tinio_transfers=gen_tinio_transfers, paco_roman_transfers=paco_roman_transfers)

@app.route("/transfer/view-by-date/<date>", methods=['GET'])
def view_transfers_by_date(date):
    # return redirect
    return redirect(url_for('view_transfer', date=date))

@app.route("/transfer/add", methods=['POST'])
def add_transfer():
    datetime = arrow.now().format('YYYY-MM-DD HH:mm:ss')
    query = request.form.get('query')    

    paco_roman_count = request.form.get('paco-roman-count', 0)
    gen_tinio_count = request.form.get('gen-tinio-count', 0)

    try:
        transfer_count = int(request.form.get('transfer-count', 0))
        transfer_stock = int(request.form.get('transfer-stock', 0))
    except:
        return "Transfer count or stock is invalid"

    if transfer_count > transfer_stock:
        return "Not enough stock to transfer"

    transfer_to = request.form.get('transfer-to', '')
    item_id = request.form.get('transfer-id')

    if transfer_to == "Gen. Tinio":
        # if paco_roman_count >= transfer_count:
        Db().transfer_to_gen_tinio(item_id, transfer_count, transfer_stock)
        # else:
        #     return "Stock in Paco Roman is not enough to transfer"
    else:
        # if gen_tinio_count >= transfer_count:
        Db().transfer_to_paco_roman(item_id, transfer_count, transfer_stock)
        # else:
        #     return "Stock in Gen. Tinio is not enough to transfer"

    Db().log_transfer(item_id, transfer_to, transfer_count, datetime)

    return redirect(url_for('search_inventory', q=query))

@app.route("/transfer/reset/<int:item_id>", methods=['GET'])
def reset_transfer(item_id):
    Db().reset_transfer(item_id)

    q = request.args.get('q', '')

    if q == '':
        return redirect(url_for('view_inventories'))

    return redirect(url_for('search_inventory', q=q))

