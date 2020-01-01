from crontab import CronTab
cron = CronTab(tabfile='filename.tab')

cron = CronTab(tab="""* * * * * command""")