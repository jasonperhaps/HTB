for ip in $(seq 1 5); do    ping -c 1 172.18.0.$ip > /dev/null && echo "Online: 172.18.0.$ip"; done

