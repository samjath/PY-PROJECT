import re
import csv
import time
import os
from argparse import ArgumentParser
from netmiko import ConnectHandler
import  datetime 

def Today():
    day=time.strftime('%d')
    month=time.strftime('%m')
    year=time.strftime('%Y')
    today=day+"-"+month+"-"+year
    return today

def SSH_Connect():
    ssh_connect = ConnectHandler(**Device)
    print ("Connection established to %s"%Device['ip'])
    time.sleep(1)
    ssh_connect.enable()
    time.sleep(1)
    ssh_connect.check_enable_mode(check_string='#')
    ssh_connect.save_config('write mem')
    print ("Saving the configurations on %s"%Device['ip'])
    ssh_connect.send_command('terminal len 0')   

def File_Ops():
    
    SaveDir = os.path.join(SaveFolder,hostname)
    if os.path.exists(SaveDir):
        Newdir = SaveDir
    else:
        os.makedirs(SaveDir)
        Newdir = SaveDir
    SaveDirF = os.path.join(Newdir,outputfile)
    time.sleep(1)
    with open(SaveDirF,'a') as save_file:
        save_file.write(output)
        save_file.write('\n')
    
    CsvData = ({'Date': day,'Hostname': hostname, 'IP Add': Device['ip'],'Status': 'None'})
    if output.isascii():
    
        CsvData['Status'] = 'Yes'
    else:
        CsvData['Status'] = 'No'
    
    with open(SaveStaus, 'a', newline='') as csvfile:
        fieldnames = [ 'Date','Hostname','IP Add','Status' ]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writerow(CsvData)

    print('>>>Command Executed Sucessfuly, exiting terminal.....')
    print('************************************END************************************')
   
        
if __name__ == "__main__":
     SaveFolder = r"C:\Users\em3130\Desktop\W-FOLDER\06. Python\3. OUTPUT\1. BACKUP"
     SaveStaus = r"C:\Users\em3130\Desktop\W-FOLDER\06. Python\3. OUTPUT\1. BACKUP\BACKUP-STATUS.csv"
     commands_list = ('show run')
     core_host = ('HO-CORE-01', 'AT-CORE-02')
     hostname_Commands = ('show run | i hostname', 'show run | grep hostname')
     IPaddrP = r"IP_Input_ssh.txt"
     day=Today()
     Device = {
    'device_type': 'cisco_ios',
    'ip': '192.168.43.10',
    'username': 'xxxxx',
    'password': 'xxxxxx',
    'secret': 'xxxxxx',
     }
     with open(IPaddrP, 'r') as IPrf:
         IPadd = IPrf.read()
         IPaddr = IPadd.split(',')
         for IP in IPaddr:
             Device['ip']=IP.strip("\n")
             outputfile= day +'.txt'
             try:
                 ssh_connect = ConnectHandler(**Device)
                 print('************************************START************************************')
                 print ("Connection established to %s"%Device['ip'])
                 time.sleep(1)
                 ssh_connect.enable()
                 time.sleep(1)
                 ssh_connect.check_enable_mode(check_string='#')
                 ssh_connect.save_config('write mem')
                 print ("Saving the configurations on %s"%Device['ip'])
                 ssh_connect.send_command('terminal len 0')   

                 
                 for hostname_comm in hostname_Commands:
                     host = ssh_connect.send_command(hostname_comm)
                     if re.search('^hostname',host):
                         break

                 match = re.search('[A-Z\d]+-[A-Z\d]*.[A-Z\d]+[\d]?.',host)
                 hostname = match.group(0)
                 print('>>> Command Executing on %s: '%hostname + commands_list )
                 output = ssh_connect.send_command(commands_list)
                 print ("Backup has been completed on %s"%hostname)
                 File_Ops()
                 for core in core_host:
                     if hostname == core:
                         hostname_slice = hostname[:3] + 'SVR' + hostname[3:]
                         changeVDC = "switchto vdc %s" %hostname_slice
                         ssh_connect.send_command(changeVDC, expect_string=r"#")
                         print('Changing VDC to SVRCORE........')
                         ssh_connect.save_config('write mem')
                         ssh_connect.send_command("terminal len 0", expect_string=hostname_slice)
                         print('>>> Command Executing on %s: '%hostname_slice + commands_list )
                         output = ssh_connect.send_command("show run", expect_string=hostname_slice)
                         print ("Backup has been completed on %s"%hostname_slice)
                         File_Ops()
                     else:
                         continue

                 ssh_connect.disconnect()

             except:  
                 print("Could't connect to %s"%Device['ip'])
                 CsvData = ({'Date': day,'Hostname': 'NONE', 'IP Add': Device['ip'],'Status': 'No'})
                 
                 with open(SaveStaus, 'a', newline='') as csvfile:
                     fieldnames = [ 'Date','Hostname','IP Add','Status' ]
                     writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                     writer.writerow(CsvData)
						 
