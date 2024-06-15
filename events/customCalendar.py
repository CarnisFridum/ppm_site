import calendar
from .models import Event
from django.urls import reverse

class CustomHTMLCalendar(calendar.HTMLCalendar):
    def _init_(self, firstweekday=calendar.SUNDAY):
        super()._init_(firstweekday)

    def formatday(self, day, weekday, attended_events, managed_events):

        if attended_events is not None:
            attended_events = attended_events.filter(date__day=day)
        if managed_events is not None:
            managed_events = managed_events.filter(date__day=day)
        
        if day == 0:
            return '<td class="noday">&nbsp;</td>'  # day outside month
        else:
            classes = self.cssclasses[weekday]
            classes += ' border'
            formattedDay = f'<td class="{classes}"><div class="pe-2 pb-1 d-inline-block border-end border-bottom">{day}</div><p class="text-wrap text-break">'
            
            if managed_events is not None:
                for event in managed_events:
                    url = reverse('show-event', args=[event.id])
                    formattedDay  += f'<div class="alert fs-6 p-1 alert-primary" role="alert"> <a href={url}> ' + str(event) + f'</a><br>'+ f'{event.date.hour:02}'+':'+f'{event.date.minute:02}' +'</div> '#todo
            if attended_events is not None:        
                for event in attended_events:
                    url = reverse('show-event', args=[event.id])
                    formattedDay  += f'<div class="alert fs-6 p-1 alert-secondary" role="alert"> <a href={url}> ' + str(event) + f'</a><br>'+ f'{event.date.hour:02}'+':'+f'{event.date.minute:02}' +'</div> '#todo
            formattedDay+=f' </p></td>'
            return formattedDay

    def formatweek(self, theweek, attended_events, managed_events):
        """
        Return a complete week as a table row.
        """
        s = ''.join(self.formatday(d, wd, attended_events, managed_events) for (d, wd) in theweek)
        return f'<tr>{s}</tr>'

    def formatmonth(self, theyear, themonth, attended_events, managed_events, withyear=True):


        v = []
        a = v.append
        a('<table class="customCalendar table w-100">')
        a('\n')
        a(self.formatmonthname(theyear, themonth, withyear=withyear))
        a('\n')
        a(self.formatweekheader())
        a('\n')
        for week in self.monthdays2calendar(theyear, themonth):
            a(self.formatweek(week, attended_events, managed_events))
            a('\n')
        a('</table>')
        a('\n')
        return ''.join(v)
