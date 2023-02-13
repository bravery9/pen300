git clone https://github.com/HavocFramework/Havoc.git
sudo apt install build-essential
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt update
sudo apt install python3.10 python3.10-dev

cd Havoc/Teamserver

go mod download golang.org/x/sys  
go mod download github.com/ugorji/go

# Install MUSL C Compiler

cd Havoc/Teamserver & ./Install.sh

# Build Binary

cd Havoc/Teamserver & make

cd Havoc/Teamserver & ./teamserver -h

# Run the teamserver
sudo ./teamserver server --profile ./profiles/havoc.yaotl -v --debug
