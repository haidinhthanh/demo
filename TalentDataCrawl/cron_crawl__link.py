from crontab import CronTab

cron = CronTab(user='haidt')

job1 = cron.new(command='python3 printfile.py')

job1.hour.every(2)
print(job1)