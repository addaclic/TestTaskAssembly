#!/bin/bash

for i in {1..3}; do
    sudo systemctl stop "foobar-test$i"
    sudo systemctl disable "foobar-test$i"
    sudo rm -f "/etc/systemd/system/foobar-test$i.service"
    sudo rm -rf "/opt/misc/test$i"
done

sudo systemctl daemon-reload

echo -e "\033[32m========Скрипт завершен========\033[0m"