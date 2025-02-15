#!/bin/bash
# replace /path/to/your/command with your script's actual full path
(crontab -l 2>/dev/null; echo "* * * * * /path/to/your/command/cron_socket.sh") | crontab -
