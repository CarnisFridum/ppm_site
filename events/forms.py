from django import forms
from django.forms import ModelForm
from .models import Venue
from .models import Event
from django.contrib.auth.models import User


class VenueForm(ModelForm):
    class Meta:
        model = Venue 
        #fields = "__all__"
        fields = ('name', 'address', 'zip_code', 'phone', 'web', 'email', 'image')
        labels = {
            'name': '',
            'address': '',
            'zip_code': '',
            'phone': '',
            'web': '',
            'email': '',
            'image': '',
        }
        widgets = {
            'name': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Venue name'}),
            'address': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Address'}),
            'zip_code': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Zip-code'}),
            'phone': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Phone'}),
            'web': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Site'}),
            'email': forms.EmailInput(attrs={'class':'form-control', 'placeholder':'Email'}),
        }


class EventForm(ModelForm):
    class Meta:
        model = Event
        #fields = "__all__"
        fields = ('name', 'date', 'venue', 'description', 'attendees', 'image')
        labels = {
            'name': '',
            'date': '',
            'venue': '',
            'description': '',
            'attendees': '',
            'image': '',
        }
        widgets = {
            'name': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Event name'}),
            'date': forms.widgets.DateTimeInput(attrs={'class':'form-control', 'type':'datetime-local', 'placeholder':'Date'}),
            'venue': forms.Select(attrs={'class':'form-control', 'placeholder':'Venue'}),
            'description': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Descrition'}),
            'attendees': forms.SelectMultiple(attrs={'class':'form-control', 'placeholder':'Attendees'}),
        }

class EventFilterForm(forms.Form):

    def __init__(self, *args, **kwargs):
        super(EventFilterForm,self).__init__(*args, **kwargs)
        self.venues = tuple(Venue.objects.values_list('id', 'name'))
        self.fields['venue'].choices = self.venues
        managerList = tuple(User.objects.values_list('id', 'username'))
        self.managers = ([None, '---'], *managerList)
        self.fields['manager'].choices = self.managers

    start_date = forms.DateField(required=False, widget=forms.widgets.DateInput(attrs={'class':'form-control', 'type':'date', 'placeholder':'Start Date'}))
    end_date = forms.DateField(required=False, widget=forms.widgets.DateInput(attrs={'class':'form-control', 'type':'date', 'placeholder':'End Date'}))
    venue = forms.MultipleChoiceField(required=False, widget=forms.SelectMultiple)
    manager = forms.ChoiceField(required=False, widget=forms.Select)



class VenueFilterForm(forms.Form):

    def __init__(self, *args, **kwargs):
        super(VenueFilterForm,self).__init__(*args, **kwargs)
        ownerList = tuple(User.objects.values_list('id', 'username'))
        self.owners = ([None, '---'], *ownerList)

        self.fields['owner'].choices = self.owners

    zip_code = forms.CharField(required=False, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Zip-code'}))
    owner = forms.ChoiceField(required=False, widget=forms.Select)





        
