#!/bin/bash
# author:wangdong
# date:2023-03-03

# 启动Celery beat进程,并且设置为后台运行
start_celery_beat() {
  celery -A celery_app beat -l debug --logfile=logs/celery_worker.log --detach
  # 检查进程是否启动成功
  if [ $? -eq 0 ]
  then
    echo "Celery beat started successfully."
  else
    echo "Celery beat failed to start."
  fi
}

stop_celery_beat() {
  # 获取Celery beat进程的进程ID
  ps aux | grep 'beat -l' | grep -v grep | awk '{print $2}' | xargs kill
  # 检查进程是否停止成功
  if  [ $? -ne 0 ]
  then
    echo "Celery beat failed to stop."
  else
    echo "Celery beat stopped successfully."
  fi
}


case "$1" in
  start)
    start_celery_beat
    ;;
  stop)
    stop_celery_beat
    ;;
  restart)
    stop_celery_beat
    start_celery_beat
    ;;
  *)
    echo "Usage: $0 {start|stop|restart}"
    exit 1
    ;;
esac
