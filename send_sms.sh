#!/bin/sh


while [ 0 -lt 1 ]
do
#  echo "started script" >> /tmp/logs/crontab/test.log
#  /Library/Frameworks/Python.framework/Versions/3.10/bin/python3.10 /Users/vgavelis/projects/python/bike_sharing/manage.py session_sms_command >> /tmp/logs/crontab/test.log
  /Library/Frameworks/Python.framework/Versions/3.10/bin/python3.10 /Users/vgavelis/projects/python/bike_sharing/manage.py session_sms_command
#  echo "ended script" >> /tmp/logs/crontab/test.log
  sleep 60
done
