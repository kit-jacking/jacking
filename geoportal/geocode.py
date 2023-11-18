from classes.node import Node
from classes.graph import Graph
from flask import Flask, render_template, request, json

app = Flask(__name__)
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/getNodesFromAddress', methods=['GET', 'POST'])
def getNodesFromAddress():
    tst = request.form.get('addressFrom')
    print(tst)
    return json.dumps({'success':True}), 200, {'ContentType':'application/json'}

if __name__ == '__main__':
    app.run(debug=True, port=5500)