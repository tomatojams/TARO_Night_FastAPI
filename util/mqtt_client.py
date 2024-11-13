import threading
import paho.mqtt.client as mqtt
from contextlib import asynccontextmanager
from fastapi import FastAPI


# MQTT 클라이언트 설정
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print(f"Connected successfully with result code {rc}")
        # 모든 토픽을 구독하여 모든 대화를 모니터링
        client.subscribe("#")
    else:
        print(f"Failed to connect with result code {rc}")


def on_message(client, userdata, msg):
    # 토픽과 메시지 내용을 로그로 출력
    print(f"Message received: Topic={msg.topic}, Payload={msg.payload.decode()}")


def start_mqtt():
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message

    try:
        client.connect("localhost", 1883, 60)  # MQTT 브로커에 연결
        print("Connected to the MQTT broker at localhost:1883")
    except Exception as e:
        print(f"Failed to connect to MQTT broker: {e}")

    # 메시지 수신을 위한 이벤트 루프 시작
    client.loop_forever()


# FastAPI Lifespan 이벤트 핸들러 사용
@asynccontextmanager
async def lifespan(app: FastAPI):
    # MQTT 클라이언트 시작
    mqtt_thread = threading.Thread(target=start_mqtt)
    mqtt_thread.daemon = True
    mqtt_thread.start()

    yield
    # 앱 종료 시 MQTT 연결 정리
    mqtt_thread.join()  # 필요 시 추가적으로 MQTT 종료 처리를 할 수 있습니다.
