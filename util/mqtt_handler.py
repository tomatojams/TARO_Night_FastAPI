import subprocess
import threading
import paho.mqtt.client as mqtt
from database import get_db
from model import MqttMessage
from contextlib import asynccontextmanager
from fastapi import FastAPI


# MQTT 브로커 실행
def run_mosquitto():
    process = subprocess.Popen(["mosquitto", "-v"])

    def cleanup():
        try:
            process.terminate()  # 권장되는 방법
            process.wait()  # 프로세스가 종료될 때까지 기다립니다.
        except Exception as e:
            print(f"Error terminating mosquitto: {e}")

    return cleanup


# MQTT 클라이언트 설정
def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")
    client.subscribe("your/mqtt/topic")


def on_message(client, userdata, msg):
    print(f"Message received: Topic={msg.topic}, Payload={msg.payload.decode()}")

    # 데이터베이스에 저장
    db = next(get_db())
    mqtt_message = MqttMessage(topic=msg.topic, payload=msg.payload.decode())
    db.add(mqtt_message)
    db.commit()


def start_mqtt():
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message

    client.connect("localhost", 1883, 60)
    client.loop_forever()


# Lifespan 이벤트 핸들러 사용
@asynccontextmanager
async def lifespan(app: FastAPI):
    # 앱 시작 시 모스키토 실행 및 MQTT 클라이언트 시작
    mosquitto_cleanup = run_mosquitto()

    mqtt_thread = threading.Thread(target=start_mqtt)
    mqtt_thread.daemon = True
    mqtt_thread.start()

    yield
    # 앱 종료 시 모스키토 종료
    mosquitto_cleanup()
