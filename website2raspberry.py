import pifacedigitalio as p
from flask import Flask
from flask import render_template

app = Flask(__name__)

p.init()
Merker = [0] * 4

@app.route('/')
def home():
    # Lese die Eingänge (0-3) des Pi-Face Digital
    for i in range(4):
        if p.digital_read(i) == 1:

            Merker[i] = 'An'
        else:
            Merker[i] = 'Aus'


    # Übergibt die Daten und rendert die Seite
    return render_template("index.html", eingangs_status=Merker)

if __name__ == '__main__':
    # starte Flask-Server im Debug-Modus
    app.debug = True
    app.run(host='0.0.0.0', port=5000)