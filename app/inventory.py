# -*- coding: utf-8 -*-
from flask import Flask, redirect,render_template, jsonify, request, url_for, session
from app import app
import json
import arrow
from db import Db
from utils import search

@app.route("/inventory/add", methods=['GET', 'POST'])
def add_inventory():
    if request.method == 'POST':
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

        inventories = Db().get_inventories()

        return render_template('add.html', categories=categories, suppliers=suppliers, items=inventories)

@app.route("/inventory", methods=['GET'])
def view_inventories():
    inventories = Db().get_inventories()
    no_stocks = Db().get_no_stocks()

    return render_template('inventories.html', items=inventories, no_stocks=no_stocks)

@app.route("/inventory/search", methods=['GET'])
def search_inventory():
    q = request.args.get('q', '')

    if q == '':
        return redirect(url_for('index'))

    results = Db().search_inventory_2(q)
    # results = search(q, results)

    return render_template('search.html', items=results, q=q)

@app.route("/inventory/delete/<int:item_id>", methods=['GET'])
def delete_inventory(item_id):
    Db().delete_inventory(item_id)

    q = request.args.get('q', '')

    if q == '':
        return redirect(url_for('view_inventories'))

    return redirect(url_for('search_inventory', q=q))

@app.route("/inventory/edit/<int:item_id>", methods=['GET', 'POST'])
def edit_inventory(item_id):
    if request.method == 'POST':
        user = session.get('user', 'Paco Roman')

        name = request.form.get('name')

        if not name:
            return "Name is invalid"

        description = request.form.get('description', '')
        code = request.form.get('code')

        try:
            price = float(request.form.get('price'))
        except:
            return "Price is invalid"

        try:
            stock = int(request.form.get('stock'))
            stock_prev = int(request.form.get('stock-prev'))
        except:
            return "Stock is invalid"

        supplier = request.form.get('supplier', '')
        category = request.form.get('category', '')

        if name and code and price and stock and category:
            item = (
                name, description, code, stock, price, supplier, category, item_id
            )

            Db().edit_inventory(item)

            quantity = stock - stock_prev

            # negative because update db is subtracting it already
            if user == 'Paco Roman':
                Db().update_paco_roman_transfer_inventory(item_id, -quantity)
            else:
                Db().update_gen_tinio_transfer_inventory(item_id, -quantity)

        return redirect(url_for('search_inventory', q=name))
    else:
        item = Db().view_inventory(item_id)

        categories = Db().get_categories()
        categories = [category['name'] for category in categories]
        try:
            categories.remove(item['category'])
        except:
            pass

        suppliers = Db().get_suppliers()
        suppliers = [supplier['name'] for supplier in suppliers]
        try:
            suppliers.remove(item['supplier'])
        except:
            pass

        return render_template('edit.html', item=item, suppliers=suppliers, categories=categories)


