from crontab import CronTab

cron = CronTab(user='haidt')
cron.remove_all()