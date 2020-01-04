from crontab import CronTab

cron = CronTab(user='haidt')

job1 = cron.new(command='python3 printfile.py')

job1.minute.every(2)
print(job1)
cron.write()