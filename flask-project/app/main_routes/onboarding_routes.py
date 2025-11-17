from flask import Blueprint, render_template, request, redirect, url_for

onboarding_bp = Blueprint('onboarding_bp', __name__, url_prefix='/onboarding')

@onboarding_bp.route('/', methods=['GET', 'POST'])
def onboarding():
    if request.method == 'POST':
        full_name = request.form.get('full_name')
        return redirect(url_for('onboarding_bp.onboarding2'))
    return render_template('onboarding.html')

@onboarding_bp.route('/2', methods=['GET', 'POST'])
def onboarding2():
    if request.method == 'POST':
        medical_condition = request.form.get('medical_condition')
        return redirect(url_for('onboarding_bp.onboarding3'))
    return render_template('onboarding2.html')

@onboarding_bp.route('/3', methods=['GET', 'POST'])
def onboarding3():
    if request.method == 'POST':
        daily_routine = request.form.get('daily_routine')
        return redirect(url_for('auth_bp.welcome'))
    return render_template('onboarding3.html')
