"""
    由于logging模块是线程安全的，但是在多线程环境下，无法保证多线程安全，这里重写TimedRotatingFileHandler
"""
import json
import logging
import os
import time
from logging.handlers import TimedRotatingFileHandler
from kafka import KafkaProducer
from kafka.errors import KafkaError


class CommonTimedRotatingFileHandler(TimedRotatingFileHandler):
    """
    重写TimedRotatingFileHandler逻辑
    """

    @property
    def dfn(self):
        """

        Returns:

        """
        current_time = int(time.time())
        # get the time that this sequence started at and make it a TimeTuple
        dst_now = time.localtime(current_time)[-1]
        t = self.rolloverAt - self.interval
        if self.utc:
            time_tuple = time.gmtime(t)
        else:
            time_tuple = time.localtime(t)
            dst_then = time_tuple[-1]
            if dst_now != dst_then:
                if dst_now:
                    addend = 3600
                else:
                    addend = -3600
                time_tuple = time.localtime(t + addend)
        dfn = self.rotation_filename(
            self.baseFilename + "." + time.strftime(self.suffix, time_tuple)
        )
        return dfn

    def shouldRollover(self, record):
        """
            是否应该执行日志滚动操作：
        1、存档文件已存在时，执行滚动操作
        2、当前时间 >= 滚动时间点时，执行滚动操作
        Args:
            record:

        Returns:

        """
        dfn = self.dfn
        t = int(time.time())
        if t >= self.rolloverAt or os.path.exists(dfn):
            return 1
        return 0

    def doRollover(self):
        """
        执行滚动操作
        1、文件句柄更新
        2、存在文件处理
        3、备份数处理
        4、下次滚动时间点更新
        """
        if self.stream:
            self.stream.close()
            self.stream = None
        # get the time that this sequence started at and make it a TimeTuple

        dfn = self.dfn
        # 存档log 已存在处理
        if not os.path.exists(dfn):
            self.rotate(self.baseFilename, dfn)

        # 备份数控制
        if self.backupCount > 0:
            for s in self.getFilesToDelete():
                os.remove(s)

        # 延迟处理
        if not self.delay:
            self.stream = self._open()

        # 更新滚动时间点
        currentTime = int(time.time())
        newRolloverAt = self.computeRollover(currentTime)
        while newRolloverAt <= currentTime:
            newRolloverAt = newRolloverAt + self.interval

        # If DST changes and midnight or weekly rollover, adjust for this.
        if (self.when == "MIDNIGHT" or self.when.startswith("W")) and not self.utc:
            dstAtRollover = time.localtime(newRolloverAt)[-1]
            dstNow = time.localtime(currentTime)[-1]
            if dstNow != dstAtRollover:
                if (
                    not dstNow
                ):  # DST kicks in before next rollover, so we need to deduct an hour
                    addend = -3600
                else:  # DST bows out before next rollover, so we need to add an hour
                    addend = 3600
                newRolloverAt += addend
        self.rolloverAt = newRolloverAt


class KafkaLoggingHandler(logging.Handler):
    """
    Kafka日志处理器
    """

    def __init__(
        self, bootstrap_servers=["localhost:9092"], topic="my_topic", retries=5
    ):
        super(KafkaLoggingHandler, self).__init__()
        # 创建一个kafka生产者，向指定的主题发送消息
        self.kafka_producer = KafkaProducer(
            # kafka集群或者单机的地址
            bootstrap_servers=bootstrap_servers,
            value_serializer=lambda x: json.dumps(x).encode(),
            # 指定生产者在发送批次之前等待更多消息加入批次的时间，kafka生产者会在批次填满或者linger.ms达到
            # 上限之后把批次发送出去
            linger_ms=10,
            # 设置最大重试次数为5次
            retries=retries,
        )

        self.topic = topic

    def emit(self, record: logging.LogRecord) -> None:
        # 删除kafka的日志避免无限递归
        if "kafka." in record.name:
            return
        try:
            msg = self.format(record)
            # 生产者producer发送消息，默认是异步形式,同时添加发送成功和发送失败的回调
            self.kafka_producer.send(self.topic, {"message": msg}).add_callback(
                self.on_send_success
            ).add_errback(self.on_send_error)
            self.flush(timeout=1.0)
        except KafkaError:
            logging.Handler.handleError(self, record)

    def on_send_success(self, record_metadata):
        print(record_metadata.topic)
        print("发送消息到kafka成功")

    def on_send_error(self, record_metadata):
        print(record_metadata.topic)
        print("发送消息到kafka失败")

    def flush(self, timeout=None) -> None:
        """
            刷新对象
        Args:
            timeout: 刷新的时间间隔

        Returns:

        """
        self.kafka_producer.flush(timeout)

    def close(self) -> None:
        self.acquire()
        try:
            if self.kafka_producer:
                self.kafka_producer.close()
            logging.Handler.close(self)
        finally:
            self.release()
