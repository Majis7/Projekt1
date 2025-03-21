from flask import Flask
from flask import render_template_string
from flask import request

app = Flask(__name__)

@app.route('/')
def home():
    # Beispiel: Eingangsstatus simuliert (kann durch echte Hardware-Daten ersetzt werden)
    eingangs_status = {
        1: 'Aus',
        2: 'Aus',
        3: 'An',
        4: 'Aus'
    }

    # HTML-Template mit dynamischen Daten
    html_template = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Smart-Home-Steuerung</title>
        <style>
            tr:nth-child(odd) { background-color: #dbdfdb; }
            table {
                width: 50%;
                border: 2px solid black;
            }
            td {
                border: 2px solid black;
                padding: 10px;
                text-align: center;
                font-size: 60%;
                color: #0000ff;
            }
            th {
                background-color: #8c016b;
                padding: 10px;
                font-size: 90%;
                color: #ffffff;
            }
            h2 {
                color: #0000ff;
                font-size: 190%;
            }
            body {
                background-color: rgb(255, 255, 255);
                font-family: arial;
                font-size: 120%;
            }
        </style>
    </head>
    <body>
        <div>
            <h1 style="text-align: center;">Smart-Home-Steuerung</h1>
        </div>
        <div style="border: 2px solid black; padding: 10px; margin-top: 10px; color: #2b00ff;">
            <h2>Eingänge</h2>
            <table border="2">
                <tr>
                    <th>Eingang</th>
                    <th>Wert</th>
                </tr>
                {% for eingang, status in eingangs_status.items() %}
                <tr>
                    <td>{{ eingang }}</td>
                    <td>{{ status }}</td>
                </tr>
                {% endfor %}
            </table>
        </div>
        <div style="border: 2px solid black; padding: 10px; margin-top: 10px;">
            <h2>Ausgänge</h2>
            Ausgang: <input>
            <form>
                <input type="radio" id="ein" name="button1" value="ein"> Ein
                <input type="radio" id="aus" name="button1" value="aus"> Aus
            </form>
            <button>Absenden</button>
        </div>
    </body>
    </html>
    """

    # Übergibt die Daten und rendert die Seite
    return render_template_string(html_template, eingangs_status=eingangs_status)

if __name__ == '__main__':
    # starte Flask-Server im Debug-Modus
    app.debug = True
    app.run(host='0.0.0.0', port=5000)