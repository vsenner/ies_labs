from paho.mqtt import client as mqtt_client
import time
from schema.aggregated_data_schema import AggregatedDataSchema
from file_datasource import FileDatasource
import config

def on_connect(broker: str, port: int) -> None:
    """Callback function for MQTT client connection"""
    def callback(client, userdata, flags, rc):
        if rc == 0:
            print(f"Connected to MQTT Broker ({broker}:{port})!")
        else:
            print(f"Failed to connect {broker}:{port}, return code {rc}")
            exit(rc)  # Stop execution
    return callback

def connect_mqtt(broker: str, port: int) -> mqtt_client.Client:
    """Create and connect MQTT client"""
    print(f"CONNECT TO {broker}:{port}")
    client = mqtt_client.Client()
    client.on_connect = on_connect(broker, port)
    client.connect(broker, port)
    client.loop_start()
    return client

def publish_data(client: mqtt_client.Client, topic: str, datasource, delay: float) -> None:
    """Publish data to MQTT topic"""
    datasource.startReading()
    while True:
        time.sleep(delay)
        data_list = datasource.read()
        for data in data_list:
            msg = AggregatedDataSchema().dumps(data)
            result = client.publish(topic, msg)
            status = result[0]
            if status == 0:
                print(f"Sent `{msg}` to topic `{topic}`")
            else:
                print(f"Failed to send message to topic {topic}")

def main():
    """Main function"""
    # Prepare MQTT client
    mqtt_client = connect_mqtt(config.MQTT_BROKER_HOST, config.MQTT_BROKER_PORT)
    # Prepare datasource
    datasource = FileDatasource("data/accelerometer.csv", "data/gps.csv", "data/parking.csv")
    # Publish data indefinitely
    publish_data(mqtt_client, config.MQTT_TOPIC, datasource, config.DELAY)

if __name__ == '__main__':
    main()
