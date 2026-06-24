#!/bin/bash

# ==========================================
# Скрипт для автоматического восстановления
# комбинированного sink-устройства PulseAudio
# ==========================================

# НАСТРОЙКИ
SINK_NAME="combination-sink"             # Имя вашего комбинированного sink
MAC1="41_42_81_08_D9_83"                 # MAC адрес первого устройства
MAC2="74_45_CE_15_F4_BB"                 # MAC адрес второго устройства
CHECK_INTERVAL=5                         # Интервал проверки в секундах
LOG_FILE="/tmp/combine-sink-monitor.log" # Файл логов

# Функция для логирования
log() {
  echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

# Функция поиска sink-ов по MAC адресу
find_sink_by_mac() {
  local mac=$1
  # Ищем sink, содержащий MAC адрес в имени
  pactl list short sinks | grep -i "$mac" | awk '{print $2}' | head -n1
}

# Функция проверки существования комбинированного sink
sink_exists() {
  pactl list short sinks | grep -q "$SINK_NAME"
  return $?
}

# Функция создания комбинированного sink
create_combine_sink() {
  log "Попытка создать комбинированный sink..."

  # Ищем оба Bluetooth-устройства
  SINK1=$(find_sink_by_mac "$MAC1")
  SINK2=$(find_sink_by_mac "$MAC2")

  if [ -z "$SINK1" ] || [ -z "$SINK2" ]; then
    log "ОШИБКА: Не найдены оба Bluetooth-устройства"
    log "  Найдено: SINK1='$SINK1', SINK2='$SINK2'"
    return 1
  fi

  log "Найдены устройства: $SINK1 и $SINK2"

  # Создаем комбинированный sink
  if pactl load-module module-combine-sink \
    sink_name="$SINK_NAME" \
    slaves="$SINK1,$SINK2" \
    channels=2 2>&1 | tee -a "$LOG_FILE"; then

    log "✅ Комбинированный sink '$SINK_NAME' успешно создан"

    # Делаем его устройством по умолчанию (опционально)
    pactl set-default-sink "$SINK_NAME" 2>/dev/null &&
      log "Устройство '$SINK_NAME' установлено как default"

    return 0
  else
    log "❌ Ошибка при создании комбинированного sink"
    return 1
  fi
}

# Функция проверки и пересоздания
check_and_fix() {
  # Проверяем, существуют ли оба Bluetooth-устройства
  SINK1=$(find_sink_by_mac "$MAC1")
  SINK2=$(find_sink_by_mac "$MAC2")

  if [ -z "$SINK1" ] || [ -z "$SINK2" ]; then
    # Устройства не найдены - пропускаем проверку
    return 0
  fi

  # Проверяем, существует ли комбинированный sink
  if sink_exists; then
    # Все хорошо, ничего не делаем
    return 0
  else
    log "⚠️  Комбинированный sink '$SINK_NAME' не найден, пересоздаем..."
    create_combine_sink
    return $?
  fi
}

# ==========================================
# ОСНОВНАЯ ЧАСТЬ
# ==========================================

# Обработка сигналов для корректного завершения
trap 'log "Скрипт остановлен"; exit 0' SIGINT SIGTERM

log "========================================="
log "🚀 Запуск мониторинга комбинированного sink"
log "   Имя sink: $SINK_NAME"
log "   MAC1: $MAC1"
log "   MAC2: $MAC2"
log "   Интервал проверки: ${CHECK_INTERVAL}с"
log "========================================="

# Сразу создаем комбинированный sink при старте
create_combine_sink

# Основной цикл мониторинга
while true; do
  check_and_fix
  sleep "$CHECK_INTERVAL"
done
