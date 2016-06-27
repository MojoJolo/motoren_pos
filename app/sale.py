# -*- coding: utf-8 -*-
from flask import Flask, redirect, render_template, jsonify, request, url_for, session
from app import app
import json
import arrow
from db import Db

@app.route("/sale/view", methods=['GET'])
def view_sale():
    return render_template('sale.html')

@app.route("/sale/add", methods=['POST'])
def add_sale():
    item_id = request.form.get('id', -1)
    name = request.form.get('name')
    description = request.form.get('description', '')
    code = request.form.get('code')

    try:
        price = float(request.form.get('price'))
    except:
        return "Price is invalid!"

    try:
        quantity = int(request.form.get('quantity'))
    except:
        return "Quantity is invalid!"

    try:
        stock = int(request.form.get('stock'))
    except:
        return "Stock is invalid"

    if quantity > stock:
        return "Not enough stock."

    srp = price * quantity

    supplier = request.form['supplier'] if 'supplier' in request.form else ''

    if name and code and price and quantity and stock:
        if 'sales' not in session:
            session['sales'] = {}

        sale = {
            'item_id': item_id,
            'name': name,
            'description': description,
            'code': code,
            'supplier': supplier,
            'price': price,
            'srp': srp, # Price x Quantity
            'quantity': quantity,
            'stock': stock,
        }

        session['sales'][item_id] = sale

        return redirect(url_for('view_sale'))
    else:
        return "[Error Sale#30] This shouldn't happen. Conctact Jolo."

@app.template_filter('total_sale')
def total_sale(sales):
    return sum([sale['srp'] for sale in sales])

@app.template_filter('item_in_sale')
def item_in_sale(sales):
    return len(sales.keys())
