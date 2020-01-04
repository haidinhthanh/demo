from crontab import CronTab

cron = CronTab(user='haidt')
for job in cron:
    print(job)
cron.remove_all()