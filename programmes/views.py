from django.shortcuts import render
from django.views.generic import (ListView,DetailView, CreateView,UpdateView,DeleteView,FormView,)
from .models import Cours,Exercice,Solution,Status
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from .forms import CoursForm,ExerciceForm, Solutionform,StatusForm
from gtts import gTTS
from django.http import HttpResponse
from django.conf import settings
import os
from django.utils import timezone
from datetime import timedelta
import pytz


class CoursList(ListView):
    model = Cours
    template_name = ('liste_cours.html')
    context_object_name = 'Courss'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        courses = self.get_queryset()
        course_dict = {course.nom_cours.lower(): reverse('detail_cours', kwargs={'slug': course.slug}) for course in
                       courses}
        context['course_dict'] = course_dict
        return context


class CoursView(DetailView):
    context_object_name = 'Cours'
    model = Cours
    template_name = 'detail_cours.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class CoursCreateView(CreateView):
    form_class = CoursForm
    model = Cours
    template_name = 'cours_create.html'

    def get_success_url(self):
        return reverse_lazy('Cours_list')

    def form_valid(self, form):
        form.instance.créer_par = self.request.user
        form.instance.fichier = self.request.FILES.get('fichier')  # Enregistrer le fichier
        form.instance.video = self.request.FILES.get('video')  # Enregistrer la vidéo
        return super().form_valid(form)


class CoursUpdateView(UpdateView):
    model = Cours
    form_class = CoursForm
    template_name = 'cours_update.html'
    success_url = reverse_lazy('Cours_list')

    def form_valid(self, form):
        form.instance.créer_par = self.request.user
        return super().form_valid(form)

class CoursDeleteView(DeleteView):
    model = Cours
    template_name = 'cours_delete.html'
    success_url = reverse_lazy('Cours_list')


import pyttsx3
import PyPDF2
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from .models import Cours


def convert_text_to_speech(request, slug):
    if slug.startswith("solution-"):
        item = get_object_or_404(Solution, slug=slug)
    elif Exercice.objects.filter(slug=slug).exists():
        item = get_object_or_404(Exercice,slug=slug)
    elif Cours.objects.filter(slug=slug).exists():
        item = get_object_or_404(Cours, slug=slug)
    else:
        return HttpResponse("Cours ou exercice non trouvé.")

    file_path = item.fichier.path
    text = ""

    if file_path.endswith('.pdf'):
        with open(file_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            for page_number in range(len(pdf_reader.pages)):
                text += pdf_reader.pages[page_number].extract_text()
    else:
        with open(file_path, 'r', encoding='utf-8') as file:
            text = file.read()

    engine = pyttsx3.init()
    engine.setProperty('rate', 150)
    engine.setProperty('volume', 1)
    output_file = os.path.join(os.path.dirname(file_path), 'output.mp3')
    engine.save_to_file(text, output_file)
    engine.runAndWait()
    engine.stop()

    with open(output_file, 'rb') as file:
        response = HttpResponse(file.read(), content_type='audio/mpeg')
        response['Content-Disposition'] = 'inline; filename=output.mp3'
        return response


class ExerciceList(ListView):
    model = Exercice
    template_name = ('liste_exercice.html')
    context_object_name = 'Exercices'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        exercices = self.get_queryset()
        exercice_dict = {exercice.nom_exercice.lower(): reverse('exercice_detail', kwargs={'slug': exercice.slug}) for exercice in
                       exercices}
        context['exercice_dict'] = exercice_dict
        return context


class ExerciceCreateView(CreateView):
    form_class = ExerciceForm
    model = Exercice
    template_name = 'exercice_create.html'

    def get_success_url(self):
        return reverse_lazy('Exercice_list')

    def form_valid(self, form):
        form.instance.créer_par = self.request.user
        form.instance.fichier = self.request.FILES.get('fichier')  # Enregistrer le fichier
        return super().form_valid(form)

class ExerciceDetailView(DetailView):
    model = Exercice
    template_name = 'exercice_detail.html'  # Remplacez par le nom de votre template

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        exercice = self.object

        status = None
        all_status = []

        if self.request.user.is_authenticated:
            if hasattr(self.request.user, 'eleve'):
                status = Status.objects.filter(exercice=exercice, créer_par=self.request.user).first()
            elif hasattr(self.request.user, 'enseignant'):
                all_status = Status.objects.filter(exercice=exercice)


        context['status'] = status
        context['all_status'] = all_status

        return context
class ExerciceUpdateView(UpdateView):
    model = Exercice
    form_class = ExerciceForm
    template_name = 'exercice_update.html'
    success_url = reverse_lazy('Exercice_list')

    def form_valid(self, form):
        form.instance.créer_par = self.request.user
        return super().form_valid(form)
class ExerciceDeleteView(DeleteView):
    model = Exercice
    template_name = 'exercice_delete.html'
    success_url = reverse_lazy('Exercice_list')


class SolutionList(ListView):
    model = Solution
    template_name = 'liste_solution.html'
    context_object_name = 'Solutions'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        solutions = context['Solutions']
        local_tz = pytz.timezone('Africa/Tunis')
        now = timezone.now().astimezone(local_tz)

        solution_dict = {}
        for solution in solutions:
            finish_time_local = solution.exercice.finish_time.astimezone(local_tz)
            finish_time_with_buffer = finish_time_local + timedelta(minutes=1)
            solution.is_expired = finish_time_with_buffer < now
            solution_dict[solution.exercice.nom_exercice.lower()] = reverse('detail_solution',
                                                                            kwargs={'slug': solution.slug})

        context['solution_dict'] = solution_dict
        return context
class SolutionCreateView(CreateView):
    form_class = Solutionform
    model = Solution
    template_name = 'solution_create.html'

    def get_success_url(self):
        return reverse_lazy('Solution_list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.instance.créer_par = self.request.user
        form.instance.fichier = self.request.FILES.get('fichier')  # Enregistrer le fichier
        return super().form_valid(form)

class SolutionDeleteView(DeleteView):
    model = Solution
    template_name = 'solution_delete.html'
    success_url = reverse_lazy('Solution_list')

class SolutionUpdateView(UpdateView):
    model = Solution
    form_class = Solutionform
    template_name = 'Solution_update.html'
    success_url = reverse_lazy('Solution_list')

    def form_valid(self, form):
        form.instance.créer_par = self.request.user
        return super().form_valid(form)

class SolutionView(DetailView):
    context_object_name = 'Solution'
    model = Solution
    template_name = 'detail_solution.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

class StatusCreateView(CreateView):
    model = Status
    form_class = StatusForm
    template_name = 'status_create.html'

    def form_valid(self, form):
        exercice = get_object_or_404(Exercice, slug=self.kwargs['slug'])
        form.instance.exercice = exercice
        form.instance.créer_par = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('exercice_detail', kwargs={'slug': self.kwargs['slug']})
class StatusDeleteView(DeleteView):
    model = Status
    template_name = 'status_delete.html'
    context_object_name = 'status'
    def get_object(self, queryset=None):
        queryset = self.get_queryset()
        slug = self.kwargs.get('slug')
        # Filter by user and slug to ensure a unique object is retrieved
        return get_object_or_404(queryset, slug=slug, créer_par=self.request.user)
    def get_success_url(self):
        return self.object.exercice.get_absolute_url()




class StatusView(DetailView):
    context_object_name = 'Status'
    model = Status
    template_name = 'detail_status.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
class StatusUpdateView(UpdateView):
    model = Status
    fields = ['fichier']
    template_name = 'status_updat.html '

    def get_object(self, queryset=None):
        queryset = self.get_queryset()
        slug = self.kwargs.get('slug')
        # Filter by user and slug to ensure a unique object is retrieved
        return get_object_or_404(queryset, slug=slug, créer_par=self.request.user)

    def get_success_url(self):
        return self.object.exercice.get_absolute_url()




