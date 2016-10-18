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
    query = request.form.get('query')

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

        return redirect(url_for('search_inventory', q=query))
    else:
        return "[Error Sale#30] This shouldn't happen. Conctact Jolo."

@app.route("/sale/clear", methods=['GET'])
def clear_sales():
    if 'sales' in session:
        session.pop('sales', None)

    return redirect(url_for('view_sale'))    

@app.route("/sale/return", methods=['POST'])
def return_sale():
    sale_id = request.form.get('sale_id')
    item_id = request.form.get('item_id')
    quantity = int(request.form.get('quantity'))
    returnee = int(request.form.get('returnee', 0))
    date = request.form.get('date')

    if sale_id and item_id and quantity and date and returnee <= quantity:
        if quantity - returnee == 0:
            Db().delete_sale(sale_id)
        else:
            Db().update_sale(sale_id, quantity, returnee)

        Db().add_return(item_id, returnee, date)
        Db().add_item_quantity(item_id, returnee)

    return redirect(url_for('index'))

@app.template_filter('total_sale')
def total_sale(sales):
    return sum([sale['srp'] for sale in sales])

@app.template_filter('item_in_sale')
def item_in_sale(sales):
    return len(sales.keys())
