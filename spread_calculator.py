import requests

def cotadora(currency, side):
    try:
        url = f"http://economia.awesomeapi.com.br/json/last/{currency}-BRL"
        response = requests.get(url)
        response.raise_for_status()
        taxa_cal = response.json()
        bid_value = float(taxa_cal.get(f'{currency}BRL', {}).get(side))
        return bid_value
    except (requests.RequestException, ValueError) as e:
        print(f"Erro ao obter taxa de câmbio: {e}")
        return None

def calcular_spread(currency, side, taxa_oferecida, trashold):
    try:
        taxa_coletada = cotadora(currency, side)
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
