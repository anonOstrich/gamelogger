from flask import render_template, redirect, url_for, request
from app import app, db, login_required
from application.search.forms import SearchForm