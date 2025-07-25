#!/bin/bash
# Проверить статус
for i in {1..3}; do
    systemctl status "foobar-test$i"
done

# Посмотреть логи
for i in {1..3}; do
    echo "Логи foobar-test$i:"
    sudo tail "/opt/misc/test$i/service.log"
    echo
done

echo -e "\033[32m========Скрипт завершен========\033[0m"