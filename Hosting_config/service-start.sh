# Change ownership of the Kafka directory
chown -R $USER:$USER /usr/local/kafka

# Start Zookeeper and Kafka
/usr/local/kafka/bin/zookeeper-server-start.sh -daemon /usr/local/kafka/config/zookeeper.properties
/usr/local/kafka/bin/kafka-server-start.sh -daemon /usr/local/kafka/config/server.properties

sleep 5

echo "---------------"
if pgrep -f "kafka\.Kafka" >/dev/null; then
    echo "Kafka has been successfully started"
else
    echo "Error in starting Kafka. Check logs at /usr/local/kafka/logs"
fi
