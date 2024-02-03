#!/bin/bash
start_dir=$(pwd)
echo "Starting Kafka installation"
cd

apt-get update -y
apt-get upgrade -y

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
if [ -f "/etc/systemd/system/zookeeper.service" ]; then
    rm /etc/systemd/system/zookeeper.service
fi
touch /etc/systemd/system/zookeeper.service
chmod 777 /etc/systemd/system/zookeeper.service

echo "[Unit]" >> /etc/systemd/system/zookeeper.service
echo "Description=Apache Zookeeper server" >> /etc/systemd/system/zookeeper.service
echo "Documentation=http://zookeeper.apache.org" >> /etc/systemd/system/zookeeper.service
echo "Requires=network.target remote-fs.target" >> /etc/systemd/system/zookeeper.service
echo "After=network.target remote-fs.target" >> /etc/systemd/system/zookeeper.service
echo "" >> /etc/systemd/system/zookeeper.service
echo "[Service]" >> /etc/systemd/system/zookeeper.service
echo "Type=simple" >> /etc/systemd/system/zookeeper.service
echo "ExecStart=/usr/local/kafka/bin/zookeeper-server-start.sh /usr/local/kafka/config/zookeeper.properties" >> /etc/systemd/system/zookeeper.service
echo "ExecStop=/usr/local/kafka/bin/zookeeper-server-stop.sh" >> /etc/systemd/system/zookeeper.service
echo "Restart=on-abnormal" >> /etc/systemd/system/zookeeper.service
echo "" >> /etc/systemd/system/zookeeper.service
echo "[Install]" >> /etc/systemd/system/zookeeper.service
echo "WantedBy=multi-user.target" >> /etc/systemd/system/zookeeper.service
echo "" >> /etc/systemd/system/zookeeper.service

# Setting up kafka.service
echo "Setting up kafka.service"
if [ -f "/etc/systemd/system/kafka.service" ]; then
    rm /etc/systemd/system/kafka.service
fi
touch /etc/systemd/system/kafka.service
chmod 777 /etc/systemd/system/kafka.service

echo "[Unit]" >> /etc/systemd/system/kafka.service
echo "Description=Apache Kafka Server" >> /etc/systemd/system/kafka.service
echo "Documentation=http://kafka.apache.org/documentation.html" >> /etc/systemd/system/kafka.service
echo "Requires=zookeeper.service" >> /etc/systemd/system/kafka.service
echo "" >> /etc/systemd/system/kafka.service
echo "[Service]" >> /etc/systemd/system/kafka.service
echo "Type=simple" >> /etc/systemd/system/kafka.service
echo "Environment="JAVA_HOME=/usr/lib/jvm/java-8-openjdk-amd64"" >> /etc/systemd/system/kafka.service
echo "ExecStart=/usr/local/kafka/bin/kafka-server-start.sh /usr/local/kafka/config/server.properties" >> /etc/systemd/system/kafka.service
echo "ExecStop=/usr/local/kafka/bin/kafka-server-stop.sh" >> /etc/systemd/system/kafka.service
echo "" >> /etc/systemd/system/kafka.service
echo "[Install]" >> /etc/systemd/system/kafka.service
echo "WantedBy=multi-user.target" >> /etc/systemd/system/kafka.service
echo "" >> /etc/systemd/system/kafka.service
echo "Successfully created services"

# Change ownership of the Kafka directory
chown -R $USER:$USER /usr/local/kafka

# Start Zookeeper and Kafka
/usr/local/kafka/bin/zookeeper-server-start.sh -daemon /usr/local/kafka/config/zookeeper.properties
/usr/local/kafka/bin/kafka-server-start.sh -daemon /usr/local/kafka/config/server.properties

# Sleep for a while to allow services to start
sleep 5

echo "---------------"
echo ""
echo "If you wish to stop Kafka, run the following commands"
echo "service stop kafka"

echo "To check the status of Kafka, run the following command"
echo "service status kafka"

cd $start_dir
