sudo apt-get update
sudo apt-get install openjdk-8-jdk
dos2unix  ./Distributed_Load_Testing_System/orchestrator.py
dos2unix  *.sh
chmod +x *.sh
source ./kafka.sh
sudo systemctl start kafka
pip3 install -r ./requirements.txt
./Distributed_Load_Testing_System/orchestrator.py