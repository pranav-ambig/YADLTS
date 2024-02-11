#!/bin/sh
start_dir=$(pwd)
echo "Starting Kafka installation"
cd

apk update
apk upgrade

# Delete previous zookeeper files and installations
rm -rf kafka*
if [ -d "/usr/local/kafka" ]; then
    echo "Deleting previous Kafka files and installations"
    rm -rf /usr/local/kafka
fi

# Download Kafka
echo "Downloading Kafka binaries"
wget https://downloads.apache.org/kafka/3.6.0/kafka_2.12-3.6.0.tgz

# Extract Kafka
echo "Decompressing tar archive for Kafka"
tar -xf kafka_2.12-3.6.0.tgz
mv kafka_2.12-3.6.0 /usr/local/kafka

# Setting up zookeeper.service
echo "Setting up zookeeper.service"
if [ -f "/etc/init.d/zookeeper" ]; then
    rm /etc/init.d/zookeeper
fi
cat <<'EOF' > /etc/init.d/zookeeper
#!/sbin/openrc-run
description="Apache Zookeeper server"

depend() {
    need net
    after firewall
}

start() {
    ebegin "Starting Zookeeper"
    /usr/local/kafka/bin/zookeeper-server-start.sh /usr/local/kafka/config/zookeeper.properties
    eend $?
}

stop() {
    ebegin "Stopping Zookeeper"
    /usr/local/kafka/bin/zookeeper-server-stop.sh
    eend $?
}
EOF
chmod +x /etc/init.d/zookeeper

# Setting up kafka.service
echo "Setting up kafka.service"
if [ -f "/etc/init.d/kafka" ]; then
    rm /etc/init.d/kafka
fi
cat <<'EOF' > /etc/init.d/kafka
#!/sbin/openrc-run
description="Apache Kafka Server"

depend() {
    need zookeeper
}

start() {
    ebegin "Starting Kafka"
    /usr/local/kafka/bin/kafka-server-start.sh /usr/local/kafka/config/server.properties
    eend $?
}

stop() {
    ebegin "Stopping Kafka"
    /usr/local/kafka/bin/kafka-server-stop.sh
    eend $?
}
EOF
chmod +x /etc/init.d/kafka

rc-update add zookeeper default
rc-update add kafka default

# Change ownership of the Kafka directory
chown -R nobody:nogroup /usr/local/kafka

# Start Zookeeper and Kafka
/usr/local/kafka/bin/zookeeper-server-start.sh -daemon /usr/local/kafka/config/zookeeper.properties
/usr/local/kafka/bin/kafka-server-start.sh -daemon /usr/local/kafka/config/server.properties

# Sleep for a while to allow services to start
sleep 7

echo "---------------"
if pgrep -f "kafka\.Kafka" >/dev/null; then
    echo "Kafka has been successfully installed and started"
else
    echo "Error in starting Kafka. Check logs at /usr/local/kafka/logs"
fi

echo "---------------"
echo ""
echo "If you wish to stop Kafka, run the following commands"
echo "service kafka stop"

echo "To check the status of Kafka, run the following command"
echo "service kafka status"

cd $start_dir
