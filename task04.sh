#!/bin/bash

echo -e "\033[38;2;201;100;59mПолучаем список юнитов, начинающихся с 'foobar-'\033[0m"
units=$(systemctl list-units --all --no-legend 'foobar-*' | awk '{print $1}')

if [[ -z "$units" ]]; then
    echo -e "\033[31mНе найдено ни одного юнита с именем foobar-*\033[0m"
    exit 1
fi

for unit in $units; do
    echo -e "\033[38;2;201;100;59mОбработка юнита: $unit\033[0m"
    
    echo -e "\033[38;2;201;100;59mОстанавливаем сервис...\033[0m"
    sudo systemctl stop "$unit"
    
    echo -e "\033[38;2;201;100;59mПолучаем текущие WorkingDirectory и ExecStart\033[0m"
    working_dir=$(systemctl show -p WorkingDirectory "$unit" | cut -d= -f2)
    exec_start=$(systemctl show -p ExecStart "$unit" | cut -d= -f2)
    
    echo -e "\033[38;2;201;100;59mИзвлекаем название сервиса из имени юнита\033[0m"
    service_name=${unit#foobar-}
    service_name=${service_name%.service}  # Удаляем .service если есть
    
    echo -e "\033[38;2;201;100;59mОпределяем новые пути\033[0m"
    new_working_dir="/srv/data/$service_name"
    new_exec_start=${exec_start//\/opt\/misc\/$service_name/\/srv\/data\/$service_name}
    
    echo -e "\033[38;2;201;100;59mПереносим файлы из $working_dir в $new_working_dir...\033[0m"
    sudo mkdir -p "$new_working_dir"
    sudo cp -a "$working_dir/." "$new_working_dir/"
    
    echo -e "\033[38;2;201;100;59mОбновляем пути в юните...\033[0m"
    sudo sed -i "s|WorkingDirectory=$working_dir|WorkingDirectory=$new_working_dir|g" "/etc/systemd/system/$unit"
    sudo sed -i "s|ExecStart=$exec_start|ExecStart=$new_exec_start|g" "/etc/systemd/system/$unit"
    
    echo -e "\033[33mЗапускаем обновленный сервис...\033[0m"
    sudo systemctl daemon-reload
    sudo systemctl start "$unit"
    
    echo -e "\033[32mГотово для $unit\033[0m"
    echo
done

echo -e "\033[32mСкрипт завершен\033[0m"