LOGFILE="logs/guardian.log"

mkdir -p logs

log(){

echo "$(date '+%F %T') | $1" >> "$LOGFILE"

}
