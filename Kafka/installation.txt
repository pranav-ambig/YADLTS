### For Installation Follow These-->

(if you donot have java 8)
sudo apt-get update

sudo apt-get install openjdk-8-jdk

java -version

(kafka installation)
chmod +x *.sh
dos2unix *.sh
source kafka.sh

### Usage

# To start Kafka
sudo systemctl start kafka

# To check the status of Kafka
sudo systemctl status kafka

# To stop kafka
sudo systemctl stop kafka
