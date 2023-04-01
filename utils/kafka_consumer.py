import json

from kafka import KafkaConsumer
from kafka import TopicPartition


# 创建一个kafka消费者，返回ConsumerRecords，这是简单的命名元祖，公开基本的消息属性
# 主题、分区、偏移量，键和值
# consumer = KafkaConsumer(group_id='my_topic_group', value_serializer=msgpack.loads)
# 默认是从上次消费的偏移量开始继续消费
consumer = KafkaConsumer(value_deserializer=json.loads)
# 手动指定主题的分区
# consumer.assign([TopicPartition('my_topic', 0)])
# 订阅指定的主题
consumer.subscribe(["my_topic"])
for msg in consumer:
    print(
        f"当前消费者订阅的主题是:{msg.topic},当前消费者消费的分区是:{msg.partition},"
        f"当前消费者的消费偏移量是:{msg.offset}, 当前消费者消费的key是:{msg.key},"
        f"当前消费者得到的消息是:{msg.value}"
    )
