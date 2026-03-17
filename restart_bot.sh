#!/bin/bash

# Kill the currently running bot process
pkill -f "python3 main.py"

# Wait for process to fully stop
sleep 2

# Start the bot again in the background
cd "$FILE_PATH"
nohup python3 main.py > bot.log 2>&1 &

echo "Bot restarted successfully"
