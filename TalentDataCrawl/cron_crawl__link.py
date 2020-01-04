from crontab import CronTab
import os
cron = CronTab(user='haidt')
root_path = os.path.dirname(os.path.realpath(__file__))
command = "/usr/bin/python3" + os.path.join(root_path, "printfile.py")+ " > /home/my_output.txt"
job1 = cron.new(command=command)

job1.minute.every(1)
print(job1)
cron.write()