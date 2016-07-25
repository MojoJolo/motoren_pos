# -*- coding: utf-8 -*-
from flask import Flask, redirect,render_template, jsonify, request, url_for
from app import app
import json
from db import Db

@app.route("/category/add", methods=['GET', 'POST'])
def add_category():
    if request.method == 'POST':
        name = request.form.get('name')

        if name:
            Db().add_category(name)

            return redirect(url_for('view_categories'))
        else:
            return "Please complete required fields."
    else:
        return redirect(url_for('view_categories'))

@app.route("/categories")
def view_categories():
    categories = Db().get_categories()

    return render_template('categories.html', items=categories)

@app.route("/category/delete/<int:category_id>", methods=['GET'])
def delete_category(category_id):
    Db().delete_category(category_id)

    return redirect(url_for('view_categories'))