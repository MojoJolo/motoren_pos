# -*- coding: utf-8 -*-
from flask import Flask, redirect,render_template, jsonify, request, url_for
from app import app
import json
import arrow
from db import Db

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/inventory/add", methods=['GET', 'POST'])
def add_inventory():
    if request.method == 'POST':
        name = request.form['name'] if 'name' in request.form else None
        description = request.form['description'] if 'description' in request.form else ''
        code = request.form['code'] if 'code' in request.form else None

        try:
            price = int(request.form['price']) if 'price' in request.form else None
        except:
            return "Price is invalid!"

        try:
            stock = int(request.form['stock']) if 'stock' in request.form else None
        except:
            return "Stock is invalid"

        supplier = request.form['supplier'] if 'supplier' in request.form else ''

        if name and code and price and stock:
            item = (
                name, description, code, stock, price, supplier
            )

            Db().add_inventory(item)

            return "Success."
        else:
            return "Please complete required fields."
    else:
        return "Add inventory"

@app.route("/inventory/get_all", methods=['GET'])
def get_inventories():
    inventories = Db().get_inventories()

    return json.dumps(inventories)

@app.route("/inventory/search", methods=['GET'])
def search_inventory():
    q = request.args.get('q', '')

    if q == '':
        return redirect(url_for('index'))

    results = Db().search_inventory(q)

    return render_template('search.html', items=results)
