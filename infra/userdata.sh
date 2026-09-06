#!/bin/bash

dnf update -y

dnf install -y \
  docker \
  git \
  wget \
  unzip \
  jq

systemctl enable docker
systemctl start docker

usermod -aG docker ec2-user

echo "Bootstrap concluído com sucesso em $(date)" > /home/ec2-user/bootstrap.log

docker --version >> /home/ec2-user/bootstrap.log 2>&1
git --version >> /home/ec2-user/bootstrap.log 2>&1

chown ec2-user:ec2-user /home/ec2-user/bootstrap.log