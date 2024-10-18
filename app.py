from flask import Flask, request, jsonify
from datetime import datetime
import pytz

app = Flask(__name__)

@app.route('/process-date', methods=['POST'])
def process_date_route():
    # Tenta obter o JSON enviado na requisição
    data = request.get_json()
    
    # Verifica se a chave 'date' está presente no JSON
    if not data or 'date' not in data:
        return jsonify({"error": "Por favor, forneça a data no formato ISO 8601 no campo 'date'."}), 400
    
    date_str = data['date']
    data_formatada, hora_formatada, days_remaining = process_date(date_str)
    
    # Verifica se ocorreu algum erro no processamento da data
    if days_remaining is None:
        return jsonify({"error": data_formatada}), 400
    
    # Retorna a resposta em formato JSON
    return jsonify({
        "data_formatada": data_formatada,
        "hora_formatada": hora_formatada,
        "days_remaining": days_remaining
    })

def process_date(date_str):
    try:
        # Converte a string da data recebida para um objeto datetime em UTC
        date_obj = datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%SZ")
        # Define o fuso horário como UTC
        utc = pytz.utc
        date_obj = utc.localize(date_obj)
        
        # Converte para o fuso horário de Brasília (BRT)
        br_tz = pytz.timezone('America/Sao_Paulo')
        date_obj = date_obj.astimezone(br_tz)

    except ValueError:
        return "Formato de data inválido", None, None

    # Separar a data e a hora em campos diferentes
    data_formatada = date_obj.strftime("%d/%m/%y")  # Retorna apenas a data
    hora_formatada = date_obj.strftime("%H:%M")     # Retorna apenas a hora

    # Definir a hora como 00:00 para ambos os objetos datetime para o cálculo de dias restantes
    today = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
    today = utc.localize(today).astimezone(br_tz)  # Converte o hoje para o fuso de Brasília também

    target_date = date_obj.replace(hour=0, minute=0, second=0, microsecond=0)

    # Calcular a diferença de dias a partir da data atual (00:00)
    days_remaining = (target_date - today).days

    return data_formatada, hora_formatada, days_remaining

if __name__ == "__main__":
    app.run()
