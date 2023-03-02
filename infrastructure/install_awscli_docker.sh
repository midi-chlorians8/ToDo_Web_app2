#! /bin/bash

# install aws cli to test s3 connection
sudo apt install unzip -y
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
unzip awscliv2.zip
sudo ./aws/install
aws --version



# install docker and docker-compose
sudo apt-get update -y
sudo apt-get install -y  \
    ca-certificates \
    curl \
    gnupg \
    lsb-release 
    
echo adawdw 1
curl  -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o  /usr/share/keyrings/docker-archive-keyring.gpg 

echo adawdw 2

echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu \
  $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
  
  
echo adawdw 3

sudo apt-get update -y
sudo apt-get install docker-ce docker-ce-cli containerd.io  -y

echo adawdw 4 
#sh -c docker version

echo No Docker Sudo

sudo groupadd docker
sudo usermod -aG docker $USER

cd /home/ubuntu 
touch file2

echo Install Docker Compose

sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
docker-compose --version


#git clone https://github.com/midi-chlorians8/ToDo_Web_app.git
git clone https://github.com/midi-chlorians8/ToDo_Web_app2.git
cd ToDo_Web_app2/
touch i_am_here

#newgrp docker #Для того чтоб сразу приминился носудо докер 
echo Succes installed Docker and Docker Compose


sudo su
chmod +x /home/ubuntu/check_git_1.sh
#sudo docker-compose up -d
bash check_git_1.sh > output.txt
# download and install wordpress end enviedronment
#bash init-letsencrypt.sh > result_init_letsencrypt.txt

chmod +x /home/ubuntu/init-letsencrypt.sh
#touch file3


