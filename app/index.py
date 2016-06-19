# -*- coding: utf-8 -*-
from flask import Flask, redirect,render_template, jsonify, request, url_for
from app import app
import json
import arrow
from db import Db

@app.route("/")
def index():
    return render_template('index.html')

@app.template_filter('count')
def count(items):
    return len(items)
