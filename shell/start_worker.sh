#!/bin/bash
# author:wangdong
# date:2023-03-03

# 启动Celery worker进程,并且设置为后台运行
start_celery_worker() {
  celery -A celery_app worker -l debug -c 10 --max-tasks-per-child=1000 --detach --logfile=logs/celery_worker.log
  # 检查进程是否启动成功
  if [ $? -eq 0 ]
  then
    echo "Celery worker started successfully."
  else
    echo "Celery worker failed to start."
  fi
}

stop_celery_worker() {
  # 获取Celery worker进程的进程ID
  ps aux | grep 'celery' | grep -v grep | awk '{print $2}' | xargs kill
  # 检查进程是否停止成功
  if  [ $? -ne 0 ]
  then
    echo "Celery worker failed to stop."
  else
    echo "Celery worker stopped successfully."
  fi
}


case "$1" in
  start)
    start_celery_worker
    ;;
  stop)
    stop_celery_worker
    ;;
  restart)
    stop_celery_worker
    start_celery_worker
    ;;
  *)
    echo "Usage: $0 {start|stop|restart}"
    exit 1
    ;;
esac
