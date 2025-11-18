from flask import Blueprint, render_template

onboarding_bp = Blueprint('onboarding_bp', __name__)

@onboarding_bp.route('/onboarding1')
def onboarding1():
    return render_template('onboarding.html')

@onboarding_bp.route('/onboarding2')
def onboarding2():
    return render_template('onboarding2.html')

@onboarding_bp.route('/onboarding3')
def onboarding3():
    return render_template('onboarding3.html')
