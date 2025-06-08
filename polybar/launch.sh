killall -q polybar                     # Отключение бара, если он включен
echo "hdmi" | tee -a /tmp/hdmi_bar.log # Просмотр логов
echo "vga" | tee -a /tmp/vga_bar.log   # Просмотр логов
# polybar hdmi >>/tmp/hdmi_bar.log &     # Запуск бара hdmi и запись его лога
polybar vga >>/tmp/vga_bar.log & # Запуск бара vga и запись его лога
