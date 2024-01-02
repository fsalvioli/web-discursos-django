from django.urls import path
from .views import PersonaListView, PersonaDetailView, PersonaCreateView, PersonaUpdateView, PersonaDeleteView
from .views import DiscursoListView, DiscursoDetailView, DiscursoCreateView, DiscursoUpdateView, DiscursoDeleteView
from .views import HomePageView, PersonasSinDiscursosView

app_name = 'register'

urlpatterns = [
    # Home:
    path('', HomePageView.as_view(), name='home'),
    
    # URLs para personas
    path('personas/', PersonaListView.as_view(), name='persona-list'),
    path('personas/<int:pk>/', PersonaDetailView.as_view(), name='persona-detail'),
    path('personas/nueva/', PersonaCreateView.as_view(), name='persona-create'),
    path('personas/<int:pk>/editar/', PersonaUpdateView.as_view(), name='persona-update'),
    path('personas/<int:pk>/eliminar/', PersonaDeleteView.as_view(), name='persona-delete'),

    # URLs para discursos
    path('discursos/', DiscursoListView.as_view(), name='discurso-list'),
    path('discursos/<int:pk>/', DiscursoDetailView.as_view(), name='discurso-detail'),
    path('discursos/nuevo/', DiscursoCreateView.as_view(), name='discurso-create'),
    path('discursos/<int:pk>/editar/', DiscursoUpdateView.as_view(), name='discurso-update'),
    path('discursos/<int:pk>/eliminar/', DiscursoDeleteView.as_view(), name='discurso-delete'),

    # Otras URLs:
    #path('buscar_personas_sin_discursos/', BuscarPersonasSinDiscursosView.as_view(), name='buscar_personas_sin_discursos'),
    path('personas_sin_discursos/', PersonasSinDiscursosView.as_view(), name='personas_sin_discursos'),

    # Busqueda e Historial:
    #path('buscar-persona/', BuscarPersonaView.as_view(), name='buscar-persona'),
    #path('historial-discursos/', HistorialDiscursosView.as_view(), name='historial-discursos'),
]
