#!/usr/bin/python3
import ftplib

ftp = ftplib.FTP("pixie-ftp.porkbun.com")
with open("iofiles/credentials.txt", "r") as file:
    data = file.readlines()
ftp.login(data[2].replace("\n", ""),data[3].replace("\n",""))
file = open("iofiles/rolls.json", "rb")
ftp.storbinary("STOR rolls.json", file)
file.close()
print("Transfer complete")
ftp.quit()