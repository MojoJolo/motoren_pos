# -*- coding: utf-8 -*-
from flask import Flask, redirect,render_template, jsonify, request, url_for
from app import app
import json
import arrow
from db import Db

@app.route("/inventory/add", methods=['GET', 'POST'])
def add_inventory():
    if request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description', '')
        code = request.form.get('code')

        try:
            price = float(request.form.get('price'))
        except:
            return request.form.get('price')

        try:
            stock = int(request.form.get('stock'))
        except:
            return "Stock is invalid"

        supplier = request.form.get('supplier', '')

        if name and code and price and stock:
            item = (
                name, description, code, stock, price, supplier
            )

            Db().add_inventory(item)

            return redirect(url_for('search_inventory', q=name))
        else:
            return "Please complete required fields."
    else:
        return render_template('add.html')

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
