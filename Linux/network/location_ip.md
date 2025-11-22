# Определяем местоположение по ip

## С помощью whois

whois a.b.c.d | grep -iE ^country:
whois 91.232.94.253 | grep -iE ^address:

whois - необходимо установить
a.b.c.d - ip адрес

## С помощью curl

обращаемся к сервису ipinfo.io - необходим только curl
curl ipinfo.io/91.232.94.253

## Фильтруем ip адреса, избавляемся от *

sudo traceroute -I 8.8.8.8 | awk '{if ($3 != "*") print $3}'

убираем открывающую и закрывающую скобки
sudo traceroute -I 8.8.8.8 | awk '{if ($3 != "*") { gsub(/\(/, "", $3); gsub(/\)/, "", $3); print $3 } }'

sudo traceroute -I 8.8.8.8 | awk '{if ($3 != "*") { gsub(/\(/, "", $3); gsub(/\)/, "", $3); print $3 } }'

## создать скрипт для автоматизации

list_ip=$( traceroute -I 8.8.8.8 | awk '{if ($3 != "*") { gsub(/\(/, "", $3); gsub(/\)/, "", $3); print $3 } }')

for ip in $list_ip; do
    echo $ip
    ip_info=$( curl -s ipinfo.io/${ip} | grep -iE 'city|timezone' )

    # ip_info=$( whois ${ip} | grep -iE 'city|address' ) 
    # city=$( echo $ip_info | grep -iE "city" )
    # timezone=$( echo $ip_info | grep -iE "timezone" )

    #echo "${city}\n{$timezone}"
    echo "$ip_info"
    echo "=========="
done