from flask import Flask, render_template
from newbot import run_bot  # Importa a função do bot

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/start_bot')
def start_bot():
    run_bot()  # Inicia o bot do Discord
    return "Bot iniciado!"

if __name__ == '__main__':
    app.run(debug=True)
