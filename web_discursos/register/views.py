from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Persona, Discurso
from django.shortcuts import redirect
from django import forms
from django.views import View
from django.utils import timezone
from django.db.models import Q, Count,Max, Subquery, OuterRef
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

class HomePageView(View):
    template_name = 'register/base.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)


class PersonaListView(ListView):
    model = Persona
    template_name = 'persona_list.html'  # Ajusta el nombre del template
    #paginate_by = 10
    context_object_name = 'personas'

class PersonaDetailView(DetailView):
    model = Persona
    ordering = ['-nombre_apellido']
    template_name = 'register/persona_detail.html'  # Ajusta el nombre del template
    
    # Historial:
    def get(self, request, *args, **kwargs):
        persona_id = kwargs.get('pk')
        print("Valor de persona_id:", persona_id) # para ver si funciona
        try:
            persona = Persona.objects.get(pk=persona_id)
            discursos = Discurso.objects.filter(persona=persona_id)
        except Persona.DoesNotExist:
            persona = None
            discursos = []
       
        context = {'persona': persona, 'discursos': discursos}
        return render(request, self.template_name, context)
     

class PersonaCreateView(CreateView):
    model = Persona
    fields = ['nombre_apellido']  # Añade o ajusta según sea necesario
    success_url = reverse_lazy('register:persona-list')

    def form_valid(self, form):
        # Additional logic if needed
        return super().form_valid(form)

class PersonaUpdateView(UpdateView):
    model = Persona
    #template_name = 'persona_form.html'  # Ajusta el nombre del template
    fields = ['nombre_apellido']  # Añade o ajusta según sea necesario

    success_url = reverse_lazy('register:persona-list')

    def form_valid(self, form):
        # Additional logic if needed
        return super().form_valid(form)

class PersonaDeleteView(DeleteView):
    model = Persona
    #template_name = 'persona_confirm_delete.html'  # Ajusta el nombre del template
    success_url = reverse_lazy('register:persona-list')  # Ajusta según la URL de la lista de personas

class DiscursoListView(ListView):
    model = Discurso
    ordering = ['-fecha']
    #paginate_by = 10 

    def get_queryset(self):
        orden = self.request.GET.get('orden', '-fecha')  # Cambia el campo de orden según tus necesidades
        busqueda = self.request.GET.get('q', '')  # Cambia 'q' por el nombre del campo de búsqueda en el formulario

        queryset = Discurso.objects.order_by(orden)

        if busqueda:
            queryset = queryset.filter(
                Q(tema__icontains=busqueda) | Q(fecha__icontains=busqueda) | Q(persona__nombre_apellido__icontains=busqueda)
            ).order_by(orden)

        return queryset

class DiscursoDetailView(DetailView):
    model = Discurso
    #template_name = 'discurso_detail.html'  # Ajusta el nombre del template

class DiscursoCreateView(CreateView):
    model = Discurso
    #template_name = 'discurso_form.html'  # Ajusta el nombre del template
    fields = ['persona', 'fecha', 'tema']  # Añade o ajusta según sea necesario

    success_url = reverse_lazy('register:discurso-list')

    def form_valid(self, form):
        # Additional logic if needed
        return super().form_valid(form)

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        # Configurar el formato de fecha para el campo 'fecha'
        form.fields['fecha'].widget = forms.DateInput(attrs={'type': 'date'}, format='%Y-%m-%d')
        return form
        

class DiscursoUpdateView(UpdateView):
    model = Discurso
    #template_name = 'discurso_form.html'  # Ajusta el nombre del template
    fields = ['persona', 'fecha', 'tema']  # Añade o ajusta según sea necesario

    success_url = reverse_lazy('register:discurso-list')

    def form_valid(self, form):
        # Additional logic if needed
        return super().form_valid(form)
    
    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        # Configurar el formato de fecha para el campo 'fecha'
        form.fields['fecha'].widget = forms.DateInput(attrs={'type': 'date'}, format='%Y-%m-%d')
        return form

class DiscursoDeleteView(DeleteView):
    model = Discurso
    #template_name = 'discurso_confirm_delete.html'  # Ajusta el nombre del template
    success_url = reverse_lazy('register:discurso-list')  # Ajusta según la URL de la lista de discursos

# Aca iría la logica para los que no tienen discurso en año actual: 
class PersonasSinDiscursosView(View):
    template_name = 'register/personas_sin_discursos.html'
    
    def get(self, request, *args, **kwargs):
        # Obtén el año actual
        current_year = timezone.now().year

        # Subconsulta para obtener las personas con discursos en el año actual
        personas_con_discursos = Persona.objects.filter(
            discurso__fecha__year=current_year
        ).values('id').distinct()

        # Filtra las personas que no tienen discursos en el año actual
        personas_sin_discursos = Persona.objects.exclude(
            id__in=Subquery(personas_con_discursos)
        )

        context = {'personas_sin_discursos': personas_sin_discursos}
        return render(request, self.template_name, context)


# Historia y Busqueda de Personas:
