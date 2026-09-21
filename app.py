from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/buscar-cep', methods=['POST'])
def buscar_cep():
    try:
        cep = request.json.get('cep', '').strip()
        
        # Remove caracteres não numéricos
        cep = ''.join(filter(str.isdigit, cep))
        
        if len(cep) != 8:
            return jsonify({'erro': 'CEP deve ter 8 dígitos'}), 400
        
        # Consulta a API do ViaCEP
        url = f'https://viacep.com.br/ws/{cep}/json/'
        response = requests.get(url)
        dados = response.json()
        
        if 'erro' in dados:
            return jsonify({'erro': 'CEP não encontrado'}), 404
        
        # Retorna os dados formatados
        return jsonify({
            'cep': dados['cep'],
            'logradouro': dados['logradouro'],
            'bairro': dados['bairro'],
            'cidade': dados['localidade'],
            'estado': dados['uf'],
            'completo': f"{dados['logradouro']}, {dados['bairro']} - {dados['localidade']}/{dados['uf']}"
        })
        
    except Exception as e:
        return jsonify({'erro': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=9000)