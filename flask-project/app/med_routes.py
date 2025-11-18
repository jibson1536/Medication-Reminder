from flask import Blueprint, render_template

med_bp = Blueprint('med_bp', __name__)

@med_bp.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@med_bp.route('/addmed')
def addmed():
    return render_template('addmed.html')

@med_bp.route('/editmed')
def editmed():
    return render_template('editmed.html')

@med_bp.route('/medlist')
def medlist():
    return render_template('medlist.html')

@med_bp.route('/details')
def details():
    return render_template('details.html')

@med_bp.route('/medication')
def medication():
    return render_template('medication.html')
