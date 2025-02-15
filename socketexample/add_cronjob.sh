#!/bin/bash
# replace /path/to/your/command with cron_socket.sh's actual full path
(crontab -l 2>/dev/null; echo "* * * * * /path/to/your/command/cron_socket.sh") | crontab -
