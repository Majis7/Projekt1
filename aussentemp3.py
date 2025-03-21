
   
import paho.mqtt.client as mqtt
import json
import time

# ----------------------------------------------------
# MQTT-Konfiguration
# ----------------------------------------------------
MQTT_BROKER = "192.168.24.251"    # Broker-Adresse oder IP
MQTT_PORT = 1883                    # Standard-Port
MQTT_TOPIC_TEMPERATURE = "homeautomation/aussen/temperatur"  # Topic, das du abonnierst

# ----------------------------------------------------
# Zweipunktregler-Konfiguration (mit Hysterese)
# ----------------------------------------------------
TEMP_ON = 20.0   # Unterhalb dieser Temperatur wird eingeschaltet
TEMP_OFF = 22.0  # Oberhalb dieser Temperatur wird ausgeschaltet

# Globale Variable, die den aktuellen Schaltzustand hält
# False = Aus, True = Ein
heater_state = False

# ----------------------------------------------------
# MQTT-Callback-Funktionen
# ----------------------------------------------------
def on_connect(client, userdata, flags, rc):
    """
    Wird aufgerufen, wenn sich der Client mit dem MQTT-Broker verbindet.
    rc == 0 bedeutet: erfolgreiche Verbindung.
    """
    if rc == 0:
        print("Verbunden mit MQTT-Broker!")
        client.subscribe(MQTT_TOPIC_TEMPERATURE)
        print(f"Abonniere Topic: {MQTT_TOPIC_TEMPERATURE}")
    else:
        print("Fehler beim Verbinden. Return-Code:", rc)

def on_message(client, userdata, msg):
    """
    Wird aufgerufen, sobald eine neue Nachricht auf dem abonnierten Topic ankommt.
    """
    global heater_state

    # 1. Payload dekodieren und ausgeben, um zu sehen, was tatsächlich ankommt
    payload_str = msg.payload.decode("utf-8", errors="replace")
    print("Rohdaten (Payload):", payload_str)

    try:
        # 2. JSON parsen
        data = json.loads(payload_str)

        # Beispielhaftes JSON-Format (basierend auf deiner Angabe):
        # {
        #   "location": "Mein Haus",
        #   "sensor data": [
        #       {
        #           "sensor_name": "Temperatur Außen",
        #           "Sensor value": 3.8
        #       }
        #   ]
        # }

        # 3. Temperatur aus dem Array "sensor data" auslesen
        #    Beachte: "Sensor value" != "sensor_value"
        temperature = float(data["sensor data"][0]["Sensor value"])

        print(f"Ausgelesene Temperatur: {temperature} °C")

        # 4. Zweipunktregler mit Hysterese
        if not heater_state and temperature < TEMP_ON:
            # Heizung einschalten
            heater_state = True
            print("Heizung wurde EINGESCHALTET")
        elif heater_state and temperature > TEMP_OFF:
            # Heizung ausschalten
            heater_state = False
            print("Heizung wurde AUSGESCHALTET")

        # 5. Falls gewünscht, den Schaltzustand zurück an den Broker senden
        #    Hier z. B. als einfachen String "ON"/"OFF"
        state_str = "ON" if heater_state else "OFF"
        client.publish(MQTT_TOPIC_OUTPUT, state_str)

    except (ValueError, KeyError, IndexError) as e:
        # Tritt auf, wenn das JSON nicht passt, der Key nicht stimmt etc.
        print("Fehler beim Verarbeiten des empfangenen JSON:", e)

def main():
    """
    Hauptfunktion, um den MQTT-Client einzurichten
    und die Endlosschleife zu starten.
    """
    # MQTT-Client anlegen
    client = mqtt.Client()

    # Callback-Funktionen zuweisen
    client.on_connect = on_connect
    client.on_message = on_message

    # Verbindung zum Broker herstellen
    print(f"Verbinde mit Broker: {MQTT_BROKER}:{MQTT_PORT} ...")
    client.connect(MQTT_BROKER, MQTT_PORT, 60)

    # Den MQTT-Loop im Hintergrund starten
    client.loop_start()

    try:
        while True:
            # Hier könnte andere Logik stehen
            # Wir warten in diesem Beispiel nur in einer Schleife
            time.sleep(1)
    except KeyboardInterrupt:
        print("Beende Skript ...")
    finally:
        # MQTT-Verbindung ordentlich schließen
        client.loop_stop()
        client.disconnect()

# ----------------------------------------------------
# Script-Einstiegspunkt
# ----------------------------------------------------
if __name__ == "__main__":
    main()
