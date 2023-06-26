#!/bin/bash
# author:wangdong
# date:2023-06-25

# 启动Celery beat进程,并且设置为后台运行
start_celery_flower() {
  celery -A celery_app flower --address=127.0.0.1 --port=5566
  # 检查进程是否启动成功
  if [ $? -eq 0 ]
  then
    echo "Celery flower started successfully."
  else
    echo "Celery flower failed to start."
  fi
}

stop_celery_beat() {
  # 获取Celery beat进程的进程ID
  ps aux | grep 'flower' | grep -v grep | awk '{print $2}' | xargs kill
  # 检查进程是否停止成功
  if  [ $? -ne 0 ]
  then
    echo "Celery flower failed to stop."
  else
    echo "Celery flower stopped successfully."
  fi
}


case "$1" in
  start)
    start_celery_flower
    ;;
  stop)
    stop_celery_flower
    ;;
  restart)
    stop_celery_flower
    start_celery_flower
    ;;
  *)
    echo "Usage: $0 {start|stop|restart}"
    exit 1
    ;;
esac
