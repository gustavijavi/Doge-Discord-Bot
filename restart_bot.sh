#!/bin/bash

cd /home/pi/Doge-Discord-Bot
git pull

sudo systemctl restart discord-bot

echo "Bot restarted successfully"