def getDayName(a, b):
    initial = 0
    days = b
    months = a
    if days == 1 and months == 1:
        initial = 0
    elif months >= 2:
        months 

    day_list = ['FRI', 'SAT', 'SUN', 'MON', 'TUE', 'WED', 'THU']

    the_day = initial + days

    day_name = day_list[(the_day % 7) - 1]

    print(day_name)
    answer = ""

    return answer

getDayName(5, 24)
