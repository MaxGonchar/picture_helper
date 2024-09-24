function db_up() {
    echo "Starting elastic search and kibana..."
    docker-compose up -d || exit 1

    echo "Waiting for elastic search to start..."
    while true; do
        curl -s http://localhost:9200/_cat/health | grep -q -E "green|yellow" && break
        echo "sleep for 1 second..."
        sleep 1
    done
    echo "Elastic search is up and running!"
}

function db_down() {
    docker-compose down
}

case $1 in
    up)
        db_up
        ;;
    down)
        db_down
        ;;
    *)
        echo "Usage: $0 {up|down}"
        exit 1
        ;;
esac



