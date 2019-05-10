# -*- coding: utf-8 -*-
from flask import Flask, redirect,render_template, jsonify, request, url_for
from app import app
import json
from db import Db

@app.route("/supplier/add", methods=['GET', 'POST'])
def add_supplier():
    if request.method == 'POST':
        name = request.form.get('name')

        if name:
            Db().add_supplier(name)

            return redirect(url_for('view_suppliers'))
        else:
            return "Please complete required fields."
    else:
        return redirect(url_for('view_suppliers'))

@app.route("/suppliers")
def view_suppliers():
    suppliers = Db().get_suppliers()

    return render_template('suppliers.html', items=suppliers)

@app.route("/supplier/delete", methods=['POST'])
def delete_supplier():
    if request.method == 'POST':
        supplier_id = request.form.get('supplier_id', '')
        Db().delete_supplier(supplier_id)

        return redirect(url_for('view_suppliers'))