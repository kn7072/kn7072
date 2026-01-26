## запуск packettracer

создаем namespace(ns) test без доступа в интернет(иначе потребует регистрацию и не запустится)
sudo ip netns add test
запускаем packettracer в созданнм ns
sudo ip netns exec test su `id -un` -c "packettracer &"
