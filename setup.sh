#!/bin/bash
# this script sets up a clean ubuntu machine with the necessary dependencies to run any of the pipelines in this repo

echo -e "\nCreating swapfile...\n"
# create a swapfile. here we use 4GB but adjust as necessary
fallocate -l 4G /swapfile
chmod 600 /swapfile
mkswap /swapfile
swapon /swapfile
# make swap permanent
echo '/swapfile none swap sw 0 0' | sudo tee -a /etc/fstab

echo -e "\nInstalling dependencies...\n"

export NEEDRESTART_MODE=a
export DEBIAN_FRONTEND=noninteractive

apt-get update -y
apt-get install -y \
    libpq-dev \
    python3-dev \
    python3-pip \
    python3-venv \
    build-essential \
    libsqlite3-dev \
    zlib1g-dev

echo -e "\nInstalling miniforge...\n"

wget -O Miniforge3.sh "https://github.com/conda-forge/miniforge/releases/latest/download/Miniforge3-$(uname)-$(uname -m).sh"
bash Miniforge3.sh -b -p "${HOME}/conda"
rm Miniforge3.sh

echo -e 'source "${HOME}/conda/etc/profile.d/conda.sh"' >> ~/.bashrc 
echo -e 'source "${HOME}/conda/etc/profile.d/mamba.sh"' >> ~/.bashrc 
source ~/.bashrc

echo -e "\nCreating environment...\n"

mamba env create -f environment.yml 

echo -e "\nActivating environment...\n"

mamba activate pika-datasets

echo -e "\nSetting up rclone config...\n"

cp rclone.conf "/${USER}/.config/rclone/rclone.conf"