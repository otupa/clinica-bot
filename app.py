from flask import Flask, request, jsonify
from datetime import datetime

app = Flask(__name__)

@app.route('/process-date', methods=['POST'])
def process_date_route():
    # Tenta obter o JSON enviado na requisição
    data = request.get_json()
    
    # Verifica se a chave 'date' está presente no JSON
    if not data or 'date' not in data:
        return jsonify({"error": "Por favor, forneça a data no formato ISO 8601 no campo 'date'."}), 400
    
    date_str = data['date']
    formatted_date, days_remaining = process_date(date_str)
    
    # Verifica se ocorreu algum erro no processamento da data
    if days_remaining is None:
        return jsonify({"error": formatted_date}), 400
    
    # Retorna a resposta em formato JSON
    return jsonify({
        "formatted_date": formatted_date,
        "days_remaining": days_remaining
    })

def process_date(date_str):
    try:
        # Converte a string da data recebida para um objeto datetime
        date_obj = datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%SZ")
    except ValueError:
        return "Formato de data inválido", None

    # Formatar a data no formato dd/mm/yy - HH:MM
    formatted_date = date_obj.strftime("%d/%m/%y - %H:%M")

    # Definir a hora como 00:00 para ambos os objetos datetime para o cálculo de dias restantes
    today = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
    target_date = date_obj.replace(hour=0, minute=0, second=0, microsecond=0)

    # Calcular a diferença de dias a partir da data atual (00:00)
    days_remaining = (target_date - today).days

    return formatted_date, days_remaining

if __name__ == "__main__":
    app.run()
