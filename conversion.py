def sec_to_hours(t):
    hours = int(t // 3600)
    t -= 3600 * hours
    minutes = int(t // 60)
    t -= 60 * minutes
    seconds = int(t)
    return hours, minutes, seconds


def id_to_name(name):
    return name.strip().split("#")[0]
