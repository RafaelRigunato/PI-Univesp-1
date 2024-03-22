from flask import Blueprint, render_template, request
from spread_calculator import calcular_spread

index = Blueprint('index', __name__)

@index.route('/', methods=['GET'])
def homepage():
    return render_template('index.html')

@index.route('/calculadora', methods=['GET', 'POST'])
def calculadora():
    if request.method == 'POST':
        try:
            taxa_oferecida = float(request.form['taxa_oferecida'])
            trashold = float(request.form['trashold'])
            currency = str(request.form['currency'])  
            side = str(request.form['side'])  
            resultado = calcular_spread(currency, side, taxa_oferecida, trashold)
            return render_template('calculadora.html', **resultado)
        except ValueError:
            return render_template('calculadora.html', error_message="Erro: Insira valores numéricos válidos.")
    return render_template('calculadora.html')
