from flask import Flask, jsonify
from funcoes import consulta_cpf as consulta

app = Flask(__name__)


@app.route('/consulta/<cpf>')
def consulta_cpf(cpf):
    if len(cpf) != 11:
        return {'CPF inválido': 'Digite os 11 números do CPF.'}
    resultado = consulta(cpf=cpf)
    if len(resultado[0]) == 14:
        resultado = {
            'CPF': resultado[0],
            'Nome': resultado[1],
            'Situação': resultado[2],
            'Texto': resultado[3]
        }
    else:
        resultado = {'Mensagem': resultado[0]}
    return jsonify(resultado)


app.run(port=8000, host="localhost", debug=True)
