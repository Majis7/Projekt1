#! /usr/bin/env python3

# Notwendige Bibliotheken
import time
import threading

from flask import Flask, render_template
from flask_socketio import SocketIO, emit

# PiFace-Bibliothek importieren und initialisieren
import pifacedigitalio
piface = pifacedigitalio.PiFaceDigital()

# Flask-App und SocketIO initialisieren
app = Flask(__name__)
socketio = SocketIO(app)

# Globale Variable zur Speicherung der aktuellen Geschwindigkeit
aktuelle_geschwindigkeit = 100
lauflicht_aktiv = True  # Zum Starten und Stoppen des Lauflichts

# HTML-Template (als einfacher String)
html_template = """
<!DOCTYPE html>
<html>
<head>
  <title>Lauflicht Steuerung</title>
  <script src="https://cdnjs.cloudflare.com/ajax/libs/socket.io/4.0.1/socket.io.js"></script>
  <script>
    var socket = io();

    function sendeGeschwindigkeit() {
      var geschwindigkeit = document.getElementById('geschwindigkeit').value;
      socket.emit('geschwindigkeit', geschwindigkeit);
    }

    function toggleLauflicht() {
      socket.emit('toggle_lauflicht');
    }

    socket.on('update', function(data) {
      document.getElementById('anzeige').innerText = 'Geschwindigkeit: ' + data.geschwindigkeit + ' ms';
    });
  </script>
</head>
<body>
  <h1>Lauflicht mit WebSocket</h1>
  <p id="anzeige">Geschwindigkeit: 100 ms</p>
  <input type="number" id="geschwindigkeit" value="100" />
  <button onclick="sendeGeschwindigkeit()">Setze Geschwindigkeit</button>
  <button onclick="toggleLauflicht()">Lauflicht Start/Stop</button>
</body>
</html>
"""

@app.route('/')
def index():
    return html_template

# WebSocket-Events
@socketio.on('geschwindigkeit')
def setze_geschwindigkeit(data):
    global aktuelle_geschwindigkeit
    try:
        geschwindigkeit = int(data)
        if 10 <= geschwindigkeit <= 1000:  # Eingabe validieren
            aktuelle_geschwindigkeit = geschwindigkeit
            print(f'Geschwindigkeit geändert zu: {aktuelle_geschwindigkeit}')
            emit('update', {'geschwindigkeit': aktuelle_geschwindigkeit}, broadcast=True)
        else:
            print("Ungültige Geschwindigkeit!")
    except ValueError:
        print("Ungültige Eingabe!")

@socketio.on('toggle_lauflicht')
def toggle_lauflicht():
    global lauflicht_aktiv
    lauflicht_aktiv = not lauflicht_aktiv  # Start oder Stop
    print(f'Lauflicht {"gestartet" if lauflicht_aktiv else "gestoppt"}!')

# Hintergrundprozess für Lauflicht
def lauflicht_steuerung():
    global aktuelle_geschwindigkeit, lauflicht_aktiv
    while True:
        if lauflicht_aktiv:
            for i in range(8):  # 8 LEDs
                piface.output_pins[i].value = 1
                time.sleep(aktuelle_geschwindigkeit / 1000.0)
                piface.output_pins[i].value = 0
        else:
            time.sleep(0.1)  # Wartezeit, wenn Lauflicht gestoppt ist

# Thread für Lauflicht starten
thread = threading.Thread(target=lauflicht_steuerung)
thread.daemon = True
thread.start()

# Flask-SocketIO starten
if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000)
