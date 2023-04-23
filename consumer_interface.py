from flask import Flask, request, jsonify
import json

app  = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        print(request)
        print(request.data)
    data = json.dumps({"resposta": str(request.data)})
    return jsonify(data)
    # return f'Dados retornados do broker: {data.decode("utf-8")}'


if __name__ == '__main__':
    app.run()