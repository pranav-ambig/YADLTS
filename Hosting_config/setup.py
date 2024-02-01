import subprocess

# Update package list
subprocess.run(["sudo", "apt-get", "update"])

# Install openjdk-8-jdk
subprocess.run(["sudo", "apt-get", "install", "openjdk-8-jdk"])

# Convert files using dos2unix
subprocess.run(["dos2unix", "./Distributed_Load_Testing_System/orchestrator.py"])
subprocess.run(["dos2unix", "*.sh"])

# Make shell scripts executable
subprocess.run(["chmod", "+x", "*.sh"])

# Start Kafka service
subprocess.run(["sudo", "systemctl", "start", "kafka"])

# Install Python dependencies
subprocess.run(["pip3", "install", "-r", "./requirements.txt"])

# Run the orchestrator.py script
subprocess.run(["./Distributed_Load_Testing_System/orchestrator.py"])
