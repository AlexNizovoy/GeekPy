import calendar
import locale as _locale


# Python2:
# use default (C) locale
# _locale.setlocale(_locale.LC_ALL, 'C')

# Python3:
# use default (C) locale
# _locale.setlocale(_locale.LC_ALL, 'C')
# use user's preferred locale -> locale.getlocale()
# _locale.setlocale(_locale.LC_ALL, '')
# Ukrainian calendar
_locale.setlocale(_locale.LC_ALL, 'Russian_Russia')
# make html-table and save to file
html = calendar.HTMLCalendar(firstweekday=0)
with open('calendar.html', 'wb') as f:
    f.write(html.formatyearpage(2018, width=3, css='calendar.css'))

print(calendar.TextCalendar(calendar.MONDAY).formatyear(2018, 2, 1, 1, 3))
