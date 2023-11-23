## For Installation Follow These-->

>[!NOTE]
>If you donot have java 8
```bash
sudo apt-get update
sudo apt-get install openjdk-8-jdk
java -version
```
> kafka installation(download kafka.sh)
```bash
chmod +x *.sh
dos2unix *.sh
source kafka.sh
```
## Usage

### To start Kafka
```bash
sudo systemctl start kafka
```
### To check the status of Kafka
```bash
sudo systemctl status kafka
```
### To stop kafka
```bash
sudo systemctl stop kafka
```
