#!/usr/bin/bash

./rolls.py

scp /home/duncan/Documents/projects/webscraping/iofiles/rolls.json pi@192.168.1.198:./schoolwork/DnD/samCampaignResults

./ftp.py