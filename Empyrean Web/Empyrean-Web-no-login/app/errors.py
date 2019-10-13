# Deals with errors and redirects to corresponding pages

from flask import render_template
from app import app

# Handles 404 error
@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404
