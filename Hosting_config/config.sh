dos2unix  ./Distributed_Load_Testing_System/orchestrator.py
dos2unix  *.sh
chmod +x *.sh
source ./kafka.sh
pip3 install -r ./requirements.txt
python3 ./Distributed_Load_Testing_System/orchestrator.py
