check_cpu(){

top -bn1 | grep "Cpu(s)"

}

check_ram(){

free -h

}

check_disk(){

df -h /

}

check_uptime(){

uptime

}
