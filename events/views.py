from django.shortcuts import render, redirect
import calendar
from calendar import HTMLCalendar
from .customCalendar import CustomHTMLCalendar
from datetime import datetime
from dateutil.relativedelta import relativedelta
from django.http import HttpResponseRedirect
from .models import Event,Venue
from django.contrib.auth.models import User
from .forms import VenueForm, EventForm, EventFilterForm, VenueFilterForm
from django.contrib import messages
from django.db.models import Value
# Create your views here.


def attend_event(request, event_id):
    event = Event.objects.get(pk=event_id)
    event.attendees.add(request.user)


    messages.success(request, ("Event attended"))
    return redirect('show-event', event_id)


def disattend_event(request, event_id):
    event = Event.objects.get(pk=event_id)
    event.attendees.remove(request.user)


    messages.success(request, ("Event disattended"))
    return redirect('show-event', event_id)

def delete_event(request, event_id):
    event = Event.objects.get(pk=event_id)
    event.delete()

    messages.success(request, ("Event deleted"))
    return redirect('list-event')


def delete_venue(request, venue_id):
    venue = Venue.objects.get(pk=venue_id)
    venue.delete()
    messages.success(request, ("Venue deleted"))

    return redirect('list-venue')

def update_venue(request, venue_id):
    venue = Venue.objects.get(pk=venue_id)
    form = VenueForm(request.POST or None, request.FILES or None, instance = venue)
    if form.is_valid():
        form.save()
        messages.success(request, ("Venue updated"))
        return redirect('list-venue')

    return render(request,
        'events/update_venue.html', {
        'venue': venue,
        'form': form,
        })

def update_event(request, event_id):
    event = Event.objects.get(pk=event_id)
    form = EventForm(request.POST or None, request.FILES or None, instance = event)
    if form.is_valid():
        form.save()
        messages.success(request, ("Event updated"))
        return redirect('list-event')

    return render(request,
        'events/update_event.html', {
        'event': event,
        'form': form,
        })

def add_event(request):
    submitted = False
    if request.method == "POST":
        form = EventForm(request.POST, request.FILES)
        if form.is_valid():
            form.instance.manager = request.user
            form.save()
            return HttpResponseRedirect('/add_event?submitted=True')
    else:
        form = EventForm
        if 'submitted' in request.GET:
            submitted = True
    return render(request,
        'events/add_event.html', {
        'form': form,
        'submitted':submitted,
        })

def search_result(request, search_type):
    if request.method == "POST":
        searched = request.POST['searched']
        search_type = request.POST['search_type']
        if search_type == "venues":
            results_list = Venue.objects.filter(name__contains=searched) if searched else Venue.objects.all() 
        else:
            results_list = Event.objects.filter(name__contains=searched) if searched else Event.objects.all()

        return render(request,
            'events/search_results.html', {
            'searched': searched,
            'search_type': search_type,
            'results_list': results_list,
            })
    else:
        return render(request,
            'events/search_results.html', {})


def show_venue(request, venue_id, year=datetime.now().year, month=datetime.now().strftime('%B')):
    

    month = month.title()
    month_number = list(calendar.month_name).index(month)
    month_number = int(month_number)

    if month_number + 1 <= 12:
        new_month_number = month_number + 1
        new_year = year
    else:
        new_month_number = 1
        new_year = year + 1
    new_month = calendar.month_name[new_month_number]

    if month_number - 1 >= 1:
        old_month_number = month_number - 1
        old_year = year
    else:
        old_month_number = 12
        old_year = year - 1
    old_month = calendar.month_name[old_month_number]


    myEvents = Event.objects.filter(venue_id=venue_id).filter(date__year=year).filter(date__month=month_number)

    cal = CustomHTMLCalendar().formatmonth(
        year,
        month_number,
        myEvents,
        None)

    venue = Venue.objects.get(pk=venue_id)
    
    owner=False
    if venue.owner == request.user:
        owner=True

    return render(request,
        'events/show_venue.html', {
        'new_year': new_year,
        'old_year': old_year,
        'venue': venue,
        "new_month": new_month,
        "old_month": old_month,
        "cal": cal,
        'owner': owner,
        })

def show_user(request, user_id):
    user = User.objects.get(pk=user_id)

    attended_events = Event.objects.filter(attendees=user).exclude(date__lt=datetime.now())
    attended_events = attended_events.order_by('date')
    owned_venues = Venue.objects.filter(owner=user)
    owner=False
    if user == request.user:
        owner=True

    return render(request,
        'events/show_user.html', {
        'attended_events': attended_events,
        'owned_venues': owned_venues,
        'user': user,
        'owner': owner,
        })

def show_event(request, event_id):
    event = Event.objects.get(pk=event_id)
    owner=False
    if event.manager == request.user:
        owner = True
    attended = False
    if request.user in event.attendees.all():
        attended = True
    return render(request,
        'events/show_event.html', {
        'event': event,
        'owner': owner,
        'attended': attended,
        })

def add_venue(request):
    submitted = False
    if request.method == "POST":
        form = VenueForm(request.POST, request.FILES)
        if form.is_valid():
            form.instance.owner = request.user
            form.save()
            return HttpResponseRedirect('/add_venue?submitted=True')
    else:
        form = VenueForm
        if 'submitted' in request.GET:
            submitted = True
    return render(request,
        'events/add_venue.html', {
        'form': form,
        'submitted':submitted,
        })
        
def list_venue(request):
    venue_list = Venue.objects.all()
    form = VenueFilterForm(request.POST)

    if form.is_valid():
        if form.cleaned_data['zip_code'] != '':
            if form.cleaned_data['owner'] != '':
                venue_list = Venue.objects.filter(zip_code__contains=form.cleaned_data['zip_code']).filter(owner=form.cleaned_data['owner'])
            else:
                venue_list = Venue.objects.filter(zip_code__contains=form.cleaned_data['zip_code'])

        else:
            if form.cleaned_data['owner'] != '':
                venue_list = Venue.objects.filter(owner=form.cleaned_data['owner'])
            
    return render(request,
        'events/venue_list.html', {
        'form': form,
        'venue_list': venue_list,
        })


def list_event(request):
    event_list = Event.objects.all()

    form = EventFilterForm(request.POST)
    if form.is_valid():
        
        if form.cleaned_data['start_date'] is not None:
            if form.cleaned_data['end_date'] is not None:
                if form.cleaned_data['venue']:
                    if form.cleaned_data['manager'] != '':
                        event_list = Event.objects.filter(date__gt=form.cleaned_data['start_date']).filter(date__lt=form.cleaned_data['end_date']).filter(venue__in=form.cleaned_data['venue']).filter(manager=form.cleaned_data['manager'])
                    else:
                        event_list = Event.objects.filter(date__gt=form.cleaned_data['start_date']).filter(date__lt=form.cleaned_data['end_date']).filter(venue__in=form.cleaned_data['venue'])
                else:
                    if form.cleaned_data['manager'] != '':
                        event_list = Event.objects.filter(date__gt=form.cleaned_data['start_date']).filter(date__lt=form.cleaned_data['end_date']).filter(manager=form.cleaned_data['manager'])
                    else:
                        event_list = Event.objects.filter(date__gt=form.cleaned_data['start_date']).filter(date__lt=form.cleaned_data['end_date'])
            else:
                if form.cleaned_data['venue']:
                    if form.cleaned_data['manager'] != '':
                        event_list = Event.objects.filter(date__gt=form.cleaned_data['start_date']).filter(venue__in=form.cleaned_data['venue']).filter(manager=form.cleaned_data['manager'])
                    else:
                        event_list = Event.objects.filter(date__gt=form.cleaned_data['start_date']).filter(venue__in=form.cleaned_data['venue'])

                else:
                    if form.cleaned_data['manager'] != '':
                        event_list = Event.objects.filter(date__gt=form.cleaned_data['start_date']).filter(manager=form.cleaned_data['manager'])
                    else:
                        event_list = Event.objects.filter(date__gt=form.cleaned_data['start_date'])
        else:
            if form.cleaned_data['end_date'] is not None:
                if form.cleaned_data['venue']:
                    if form.cleaned_data['manager'] != '':
                        event_list = Event.objects.filter(date__lt=form.cleaned_data['end_date']).filter(venue__in=form.cleaned_data['venue']).filter(manager=form.cleaned_data['manager'])
                    else:
                        event_list = Event.objects.filter(date__lt=form.cleaned_data['end_date']).filter(venue__in=form.cleaned_data['venue'])
                else:
                    if form.cleaned_data['manager'] != '':
                        event_list = Event.objects.filter(date__lt=form.cleaned_data['end_date']).filter(manager=form.cleaned_data['manager'])
                    else:
                        event_list = Event.objects.filter(date__lt=form.cleaned_data['end_date'])
            else:
                if form.cleaned_data['venue']:
                    if form.cleaned_data['manager'] != '':
                        event_list = Event.objects.filter(venue__in=form.cleaned_data['venue']).filter(manager=form.cleaned_data['manager'])
                    else:
                        event_list = Event.objects.filter(venue__in=form.cleaned_data['venue'])
                else:
                    if form.cleaned_data['manager'] != '':
                        event_list = Event.objects.filter(manager=form.cleaned_data['manager'])

    return render(request,
        'events/event_list.html', {
        'form': form,
        'event_list': event_list,
        })


def home(request, year=datetime.now().year, month=datetime.now().strftime('%B')):

    if request.user.is_authenticated:

        my_events = Event.objects.filter(manager=request.user).exclude(date__lt=datetime.now()).annotate(relevance=Value(1))
        my_events = my_events.union(Event.objects.filter(attendees=request.user).exclude(date__lt=datetime.now()).exclude(manager=request.user).annotate(relevance=Value(2)))
        my_events = my_events.order_by('relevance', 'date')
        my_venues = Venue.objects.filter(owner=request.user)

        month = month.title()
        month_number = list(calendar.month_name).index(month)
        month_number = int(month_number)

        if month_number + 1 <= 12:
            new_month_number = month_number + 1
            new_year = year
        else:
            new_month_number = 1
            new_year = year + 1
        new_month = calendar.month_name[new_month_number]

        if month_number - 1 >= 1:
            old_month_number = month_number - 1
            old_year = year
        else:
            old_month_number = 12
            old_year = year - 1
        old_month = calendar.month_name[old_month_number]

        managed_events = Event.objects.filter(manager=request.user).filter(date__year=year).filter(date__month=month_number)
        attended_events = Event.objects.filter(attendees=request.user).filter(date__year=year).filter(date__month=month_number).exclude(id__in=managed_events)
        


        cal = CustomHTMLCalendar().formatmonth(
            year,
            month_number,
            attended_events,
            managed_events)

        return render(request,
            'events/home.html', {
            "year": year,
            "new_year": new_year,
            "old_year": old_year,
            "month": month,
            "new_month": new_month,
            "old_month": old_month,
            "month_number": month_number,
            "cal": cal,
            "my_events": my_events,
            "my_venues": my_venues,
            })
    else:
        return render(request,
            'events/home.html', {})