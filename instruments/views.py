from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .forms import InstrumentForm
from .models import Instrument
from django.db.models import Count, Q
  

@login_required
def list(request):
   # instruments = Instrument.objects.all()

    instruments = Instrument.objects.annotate(
        inscripciones_activas=Count(
            'detailacademicinscription',
            filter=Q(detailacademicinscription__id_academic_period__is_active=True)
        )
    )
    
    if request.method == 'GET':
        return render(request, 'instruments/instruments_list.html', {
            'form': InstrumentForm,
            'instruments': instruments
        }) 
    else:
        try:
            form = InstrumentForm(request.POST)
            new_instrument = form.save(commit=False)
            new_instrument.save()
            return redirect(reverse('instruments:list'))
        except ValueError:
            return render(request, 'instruments/instruments_list.html', {
                'form': InstrumentForm,
                'error': 'Ha habido un error al registrar la nueva cátedra.'
            }) 

