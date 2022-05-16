#!/usr/bin/python3
#Author: Samuel T. Latimer
#Date: May 10th, 2022

#The code uses SSH to view the hostname and files within /var/www
#receives input from 'ip.txt' containing a list of ip addresses
#concludes by returning the output into output.txt

import paramiko
import subprocess
#will contain either hostname or directory contents
var = ''

username = input('Enter your username: ')
password = input('Enter your password: ')

#ssh fuction to connect
def ssh_connection(ip, user, passwd, command):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(ip, username = user, password = passwd)
    ssh_session = client.get_transport().open_session()
    #checks if the connection is successful
    #records data in variable var
    if ssh_session.active:
        ssh_session.exec_command(command)
        var = (ssh_session.recv(1024))
        var = var.decode()
        #print(ssh_session.recv(1024))
        return var

#the resulting output file to insert into
with open('output.txt' ,'a+') as output:
    #contains list of ip addresses
    filename = 'ip.txt'
    ip = 'x.x.x.x'
    fh = open(filename)
    #runs through every line (ip)
    for line in fh:
        # print(line)
        #removes invisible newline
        ipssh = (line.rstrip('\n'))
        #outputs ip address
        output.write(ipssh + '\n')
        #must be strings to output
        #outputs the hostname
        output.write(str(ssh_connection(ipssh , username , password  , 'hostname')))
        output.write('\n')
        #outputs the directory contents
        output.write(str(ssh_connection(ipssh , username , password , 'ls -l /var/www')))
        output.write('\n')
        #output.write(var)
        output.write(('=' * 80) + '\n')
    fh.close()
