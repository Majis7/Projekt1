import paho.mqtt.client as mqtt
import json
import time

# MQTT-Konfiguration
MQTT_BROKER = "192.168.24.251"
MQTT_PORT = 1883
MQTT_TOPIC_TEMPERATURE = "homeautomation/aussen/temperatur"

# Zweipunktregler-Konfiguration
TEMP_ON = 20.0
TEMP_OFF = 22.0
CONTROL_HYSTERESIS = True

# Globale Variable zum Speichern des aktuellen Schaltzustands
heater_state = False

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Verbunden mit MQTT-Broker!")
        client.subscribe(MQTT_TOPIC_TEMPERATURE)
    else:
        print("Verbindungsfehler. Return-Code:", rc)

def on_message(client, userdata, msg):
    global heater_state
    
    try:
        # JSON-Payload dekodieren
        payload_str = msg.payload.decode("utf-8")
        data = json.loads(payload_str)
        
        # Aus dem JSON die Temperatur lesen
        temperature = float(data["sensor_value"])  # Hier wird sensor_value ausgelesen
        
        print(f"Empfangene Temperatur: {temperature} °C (Sensor: {data['sensor_name']})")
        
        # Beispiel: Zweipunktregler mit Hysterese
        if CONTROL_HYSTERESIS:
            if not heater_state and (temperature < TEMP_ON):
                heater_state = True
                print("Heizung wurde EINGESCHALTET (Hysterese-Logik)")
            elif heater_state and (temperature > TEMP_OFF):
                heater_state = False
                print("Heizung wurde AUSGESCHALTET (Hysterese-Logik)")
        else:
            # Ohne Hysterese
            if temperature < TEMP_ON and not heater_state:
                heater_state = True
                print("Heizung wurde EINGESCHALTET (Ohne Hysterese)")
            elif temperature >= TEMP_ON and heater_state:
                heater_state = False
                print("Heizung wurde AUSGESCHALTET (Ohne Hysterese)")

        # Aktuellen Zustand zurück an den Broker senden
        payload = "ON" if heater_state else "OFF"
        client.publish(MQTT_TOPIC_OUTPUT, payload)

    except (ValueError, KeyError) as e:
        print("Fehler beim Verarbeiten des empfangenen JSON:", e)

def main():
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    
    # Verbindung zum MQTT-Broker
    client.connect(MQTT_BROKER, MQTT_PORT, 60)
    
    # Netzwerk-Loop starten
    client.loop_start()
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Beende Skript...")
    finally:
        client.loop_stop()
        client.disconnect()

if __name__ == "__main__":
    main()
