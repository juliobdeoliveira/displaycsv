from flask import Flask, request, render_template
import pandas as pd

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/display', methods=['POST'])
def display_file():
    file = request.files.get('file')
    if not file or file.filename == "":
        return "No file"

    df = None
    try:
        df = pd.read_csv(file, delimiter=";")
    except UnicodeDecodeError:
        file.seek(0)
        try:
            df = pd.read_csv(file, encoding='latin1', delimiter=";")
        except UnicodeDecodeError:
            file.seek(0)
            df = pd.read_csv(file, encoding='ISO-8859-1', delimiter=";")

    return render_template(
        'display.html',
        tables=[df.to_html(classes='data', index=False)],
        titles=df.columns.values
    )

if __name__ == '__main__':
    # Para rodar localmente
    app.run(host="0.0.0.0", port=8000, debug=True)