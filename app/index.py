# -*- coding: utf-8 -*-
from flask import Flask, redirect,render_template, jsonify, request, url_for
from app import app
import json
import arrow
from db import Db

@app.route("/")
def index():
    date = arrow.now()
    transactions = Db().view_transactions(date.format("YYYY-MM-DD"))

    total = sum([transaction['actual'] for transaction in transactions])

    return render_template('index.html', transactions=transactions, total=total, date=date.format("MMMM DD, YYYY"))

@app.template_filter('count')
def count(items):
    return len(items)
