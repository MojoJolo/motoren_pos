# -*- coding: utf-8 -*-
from flask import Flask, redirect,render_template, jsonify, request, url_for
from app import app
import json
import arrow
from db import Db

@app.route("/inventory/add", methods=['GET', 'POST'])
def add_inventory():
    if request.method == 'POST':
        print request.form

        request.form.get('name')

        for i in range(0, 5):
            name = request.form.get('name-{}'.format(i))

            if not name:
                continue

            description = request.form.get('description-{}'.format(i), '')
            code = request.form.get('code-{}'.format(i))

            try:
                price = float(request.form.get('price-{}'.format(i)))
            except:
                print "Price is invalid"
                continue

            try:
                stock = int(request.form.get('stock-{}'.format(i)))
            except:
                print "Stock is invalid"
                continue

            supplier = request.form.get('supplier', '')
            category = request.form.get('category', '')

            if name and code and price and stock and category:
                item = (
                    name, description, code, stock, price, supplier, category
                )

                Db().add_inventory(item)

        return redirect(url_for('view_inventories'))
    else:
        categories = Db().get_categories()
        categories = [category['name'] for category in categories]

        suppliers = Db().get_suppliers()
        suppliers = [supplier['name'] for supplier in suppliers]

        return render_template('add.html', categories=categories, suppliers=suppliers)

@app.route("/inventory", methods=['GET'])
def view_inventories():
    inventories = Db().get_inventories()

    return render_template('inventories.html', items=inventories)

@app.route("/inventory/search", methods=['GET'])
def search_inventory():
    q = request.args.get('q', '')

    if q == '':
        return redirect(url_for('index'))

    results = Db().search_inventory(q)

    return render_template('search.html', items=results)
