from datetime import datetime


def get_instance_time_iso_format():
    dt_now = datetime.now()
    dt_utc_now = datetime.utcnow()
    delta = dt_now - dt_utc_now
    hh, mm = divmod((delta.days * 24 * 60 * 60 + delta.seconds + 30) // 60, 60)
    dateString = "%s%+02d:%02d" % (dt_now.isoformat(), hh, mm)
    dateString = dateString[0:19]+"Z"
    return dateString
