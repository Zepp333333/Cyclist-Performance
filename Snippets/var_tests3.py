#  Copyright (c) 2021. Sergei Sazonov. All Rights Reserved
import calendar
import zipfile

import pandas as pd
import datetime


YEAR_RANGE = [i for i in range(2015, 2040)]

cal = calendar.Calendar()
c = cal.monthdatescalendar(2021, 3)

# print(calendar.month(2021, 4))

cal_dict = {}

for year in YEAR_RANGE:
    year_cal = cal.yeardatescalendar(year)
    cal_dict[year] = {}
    for month in year_cal:
        cal_dict[year] = {month: {}}
        for week in month:
            cal_dict[year][month] = {week:{}}
            for day in week:
                if not day.strftime("%A") in cal_dict:
                    cal_dict[year][month][week][day.strftime("%A")] = [day]
                else:
                    cal_dict[year][month][week][day.strftime("%A")].append(day)

for w in c:
    for d in w:
        if not d.strftime("%A") in cal_dict :
            cal_dict[d.strftime("%A")] = [d]
        else:
            cal_dict[d.strftime("%A")].append(d)

df = pd.DataFrame(cal_dict)
