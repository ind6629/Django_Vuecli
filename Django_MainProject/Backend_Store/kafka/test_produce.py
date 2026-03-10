from kafka import KafkaProducer
import json
import time

# 配置 Kafka 集群地址
bootstrap_servers = ['hadoop01:9092', 'hadoop02:9092', 'hadoop03:9092']

# 创建生产者（JSON 格式）
producer = KafkaProducer(
    bootstrap_servers=bootstrap_servers,
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

# 发送数据
for i in range(10):
    message = {
        "user_id": i,
        "product_id": 100 + i,
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S")
    }
    producer.send('track_clicks', message)
    print(f"Sent: {message}")
    time.sleep(1)  # 模拟实时数据

producer.flush()  # 确保所有消息发送完成