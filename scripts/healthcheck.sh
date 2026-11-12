#!/bin/bash

API_URL="https://api.openweathermap.org/data/2.5/weather?lat=53.2&lon=45.0&units=metric&lang=en&appid=4f92478666369bb38f354f1dbecbb794"
TIMEOUT=30
LOG_PATH="/home/pasqalex/pipelines/logs/weatherPipe-$(date +%F).log"

#Trap holder
trap "echo '   Ошибка: процесс завершён из-за внешнего воздействия!'" TERM INT

echo -n "Проверка работоспособности API "
for i in $(seq 1 3) ; do
    sleep 1 ; echo -n "." ; i=$(( i + 1 ))
done

HTTP_CODE=$(curl -s -m "$TIMEOUT" -o /home/pasqalex/pipelines/weatherPipe/tmp/weather_check.json -w "%{http_code}" "$API_URL")
CURL_EXIT=$?

echo " "

if [ $CURL_EXIT -ne 0 ] ; then
	echo "Отчёт сохранен в $LOG_PATH"
	echo "Ошибка: сетевая ошибка $CURL_EXIT. $(date +%d-%m-%Y\ %H:%M:%S)" >>/home/pasqalex/pipelines/logs/weatherPipe-$(date +%F).log
	exit 1
fi

if [ "$HTTP_CODE" -ne 200 ] ; then
	echo "Отчёт сохранен в $LOG_PATH"
	echo "Ошибка: API вернуло статус $HTTP_CODE. $(date +%d-%m-%Y\ %H:%M:%S)" >>/home/pasqalex/pipelines/logs/weatherPipe-$(date +%F).log
	exit 1
fi

rm -f /home/pasqalex/pipelines/weatherPipe/tmp/weather_check.json

echo "API работает корректно" >>/home/pasqalex/pipelines/logs/weatherPipe-$(date +%F).log
exit 0
