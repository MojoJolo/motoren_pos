# -*- coding: utf-8 -*-
from flask import Flask, redirect,render_template, jsonify, request, url_for
from app import app
import json
import arrow

@app.route("/")
def index():
    return "hello world"

@app.route("/inventory/add", methods=['GET', 'POST'])
def addInventory():
    if request.method == 'POST':
        name = request.form['name'] if 'name' in request.form else None
        description = request.form['description'] if 'description' in request.form else ''
        code = request.form['code'] if 'code' in request.form else None
        price = request.form['price'] if 'price' in request.form else None
        stock = request.form['stock'] if 'stock' in request.form else None

        if name and code and price and stock:
            return ""
        else:
            return "Please complete required fields."
    else:
        return "add inventory"