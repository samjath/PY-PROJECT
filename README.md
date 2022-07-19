# PY-PROJECT

Introduction:

The following Python code can be used to make a backup of a network configuration and save it to a UNC path. The following instructions must be followed before you begin.

 

The following credential section needs to be updated

    'device_type': 'cisco_ios',
    'ip': '192.168.43.10',
    'username': 'xxxxx',
    'password': 'xxxxxx',
    'secret': 'xxxxxx',
  
Update the following UNC path with the correct location details

SaveFolder" where the configuration files saved and  SaveStaus where the backup status list located, change these two parameter with the location wehre you need to save the files. 

    
     SaveFolder = r"C:\Users\em3130\Desktop\W-FOLDER\06. Python\3. OUTPUT\1. BACKUP"
     SaveStaus = r"C:\Users\em3130\Desktop\W-FOLDER\06. Python\3. OUTPUT\1. BACKUP\BACKUP-STATUS.csv"

This parameter needs to modify if NEXUS VDC is used and child VDC backup needs to be performed.

     core_host = ('HO-CORE-01', 'AT-CORE-02')
