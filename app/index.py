# -*- coding: utf-8 -*-
from flask import Flask, redirect,render_template, jsonify, request, url_for, session
from app import app
import json
import arrow
from db import Db

@app.route("/")
def index():
    date = arrow.now()
    transactions = Db().view_transactions(date.format("YYYY-MM-DD"))
    total = sum([transaction['actual'] for transaction in transactions])

    prev_dates = arrow.Arrow.range('day', date.replace(days=-7), date)
    prev_dates = [prev_date.format("MMMM DD, YYYY") for prev_date in prev_dates]

    if 'user' not in session:
        session['user'] = "Paco Roman"
        session.modified = True

    return render_template('index.html', transactions=transactions, total=total, date=date.format("MMMM DD, YYYY"), prev_dates=prev_dates)

@app.route("/user", methods=['GET'])
def change_user():
    user = request.args.get('user', '')
    session['user'] = user
    session.modified = True

    return user

@app.template_filter('count')
def count(items):
    return len(items)
