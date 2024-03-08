from flask import Flask, render_template, request
import requests

app = Flask(__name__)

def cotadora():
    try:
        url = "http://economia.awesomeapi.com.br/json/last/USD-BRL"
        response = requests.get(url)
        response.raise_for_status()  # Lançar exceção para códigos de status HTTP diferentes de 200
        taxa_cal = response.json()
        bid_value = float(taxa_cal.get('USDBRL', {}).get('bid'))
        return bid_value
    except (requests.RequestException, ValueError) as e:
        # Tratamento genérico de exceção para chamadas de API e conversão de valor
        print(f"Erro ao obter taxa de câmbio: {e}")
        return None

def calcular_spread(taxa_oferecida, trashold):
    try:
        taxa_coletada = cotadora()
        if taxa_coletada is None:
            return {'error_message': "Erro ao obter taxa de câmbio."}

        spread = round(taxa_oferecida - taxa_coletada, 4)

        spread_10bps = round(taxa_coletada + 0.010, 4)
        spread_15bps = round(taxa_coletada + 0.015, 4)
        spread_20bps = round(taxa_coletada + 0.020, 4)
        spread_25bps = round(taxa_coletada + 0.025, 4)

        if spread > trashold:
            status = "SPREAD ACIMA, NÃO FECHAR"
        else:
            status = "SPREAD ABAIXO, PODE FECHAR"

        return {
            'spread_10bps': spread_10bps,
            'spread_15bps': spread_15bps,
            'spread_20bps': spread_20bps,
            'spread_25bps': spread_25bps,
            'taxa_coletada': taxa_coletada,
            'taxa_oferecida': taxa_oferecida,
            'spread': spread,
            'trashold': trashold,
            'status': status
        }
    except ValueError:
        return {'error_message': "Erro: Insira um valor válido para a taxa oferecida."}

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        try:
            taxa_oferecida = float(request.form['taxa_oferecida'])
            trashold = float(request.form['trashold'])
            resultado = calcular_spread(taxa_oferecida, trashold)
            return render_template('index.html', **resultado)
        except ValueError:
            return render_template('index.html', error_message="Erro: Insira valores numéricos válidos.")
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
