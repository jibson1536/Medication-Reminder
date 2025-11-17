from flask import Blueprint, render_template, request, redirect, url_for

med_bp = Blueprint('med_bp', __name__, url_prefix='/medications')

@med_bp.route('/')
def med_list():
    return render_template('medlist.html')

@med_bp.route('/add', methods=['GET', 'POST'])
def add_med():
    if request.method == 'POST':
        name = request.form.get('name')
        return redirect(url_for('med_bp.med_list'))
    return render_template('addmed.html')

@med_bp.route('/<int:med_id>')
def med_details(med_id):
    return render_template('details.html', med_id=med_id)

@med_bp.route('/<int:med_id>/edit', methods=['GET', 'POST'])
def edit_med(med_id):
    if request.method == 'POST':
        updated_name = request.form.get('name')
        return redirect(url_for('med_bp.med_details', med_id=med_id))
    return render_template('editmed.html', med_id=med_id)
