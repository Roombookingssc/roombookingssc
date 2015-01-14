from django.shortcuts import render,get_object_or_404,redirect
from django.core.urlresolvers import reverse
from django.utils.safestring import mark_safe
from django.utils import timezone
from django.http import Http404
from events import models

def home(request):
    '''
    The homepage for events. 
    Redirects to current month calender
    '''
    now=timezone.now()
    year=now.year
    month=now.month
    return redirect('event_month',year=year,month=month)

def event_add(request):
    '''Adds an event'''
    data={}
    template='events/event_add.html'
    if request.method=='GET':
        data['form']=models.NewForm()
        data['schform']=models.ScheduleFormset()
        return render(request,template,data)
    elif request.method=='POST':
        form=models.NewForm(request.POST)
        schform=models.ScheduleFormset(request.POST)
        if form.is_valid() and schform.is_valid():
            n=form.save()
            s=schform.save()
            template='events/successful.html'
            data['event']=n
            return render(request,template,data)
        else:
            data['form']=form
            data['schform']=schform
            return render(request,template,data)
def event_month(request,year,month):
    '''
    monthly calender for the month's events
    '''
    if type(year)!=type(0):
        year=int(year)#convert
    if type(month)!=type(0):
        month=int(month)#convert
    #validate month and year data
    if month not in range(1,13):#1 to 12 both inclusive
        raise Http404#not found    
    #generate event calender and move on
    data={}
    template='events/month.html'
    ev=models.Event.objects.order_by('start')
    ev=ev.filter(start__year=year,start__month=month,approved=True)
    cal=models.EventCalender(ev).formatmonth(year,month)
    data['events_calender']=mark_safe(cal)
    data['event_photos']=models.Photo.objects.order_by('event__start')
    nmonth=month+1
    nyear=year
    if nmonth>12:
        nyear+=1
        nmonth=1

    data['next']=reverse('event_month',args=[nyear,nmonth])
    pmonth=month-1
    pyear=year
    if pmonth<1:
        pmonth=12
        pyear-=1
    data['last']=reverse('event_month',args=[pyear,pmonth])
    #----------roomdata
    schedules=[]
    sc=models.Schedule.objects.filter(event=ev).order_by('location')
    data['schedules']=sc
    return render(request,template,data)
def event_detail(request,nick):
    '''
    event details
    '''
    data={}
    template='events/event.html'
    obj=get_object_or_404(models.Event,nickname=nick)
    
    schedules=models.Schedule.objects.filter(event=obj)
    posters=models.Poster.objects.filter(event=obj)
    photos=models.Photo.objects.filter(event=obj)

    data['event']=obj
    data['schedules']=schedules
    data['posters']=posters
    data['photos']=photos
    
    return render(request,template,data)
