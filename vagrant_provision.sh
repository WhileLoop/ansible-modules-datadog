#!/bin/sh
sudo apt-get update
sudo apt-get install -y python-pip
sudo -H pip install -r /vagrant/requirements.txt

cd /vagrant/
ansible-playbook dashboard_example.yml -i 'localhost,' --connection=local
