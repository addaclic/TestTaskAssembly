#!/bin/bash
#Создаем тестовые юниты

# Директория для тестовых сервисов
TEST_DIR="/opt/misc"
sudo mkdir -p "$TEST_DIR"

for i in {1..3}; do
    SERVICE_NAME="test$i"
    SERVICE_DIR="$TEST_DIR/$SERVICE_NAME"
    SERVICE_UNIT="/etc/systemd/system/foobar-$SERVICE_NAME.service"
    
    # Создаем директорию сервиса
    sudo mkdir -p "$SERVICE_DIR"
    
    # Создаем простой скрипт-демон
    sudo tee "$SERVICE_DIR/foobar-daemon" >/dev/null <<EOF
#!/bin/bash
while true; do
    echo "\$(date) - Service foobar-$SERVICE_NAME is running" >> "$SERVICE_DIR/service.log"
    sleep 10
done
EOF
    
    sudo chmod +x "$SERVICE_DIR/foobar-daemon"
    
    # Создаем юнит systemd
    sudo tee "$SERVICE_UNIT" >/dev/null <<EOF
[Unit]
Description=Foobar Test Service $i
After=network.target

[Service]
WorkingDirectory=$SERVICE_DIR
ExecStart=$SERVICE_DIR/foobar-daemon
Restart=always
User=nobody
Group=nogroup

[Install]
WantedBy=multi-user.target
EOF
    
    # Даем минимальные права для безопасности
    sudo chown nobody:nogroup "$SERVICE_DIR"
    sudo chmod 700 "$SERVICE_DIR"
done

# Перезагружаем systemd
sudo systemctl daemon-reload
echo -e "\033[32m========Скрипт завершен========\033[0m"