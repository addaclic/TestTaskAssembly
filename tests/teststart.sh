#!/bin/bash

for i in {1..3}; do
    sudo systemctl start "foobar-test$i"
    sudo systemctl enable "foobar-test$i"
done

echo -e "\033[32m========Скрипт завершен========\033[0m"