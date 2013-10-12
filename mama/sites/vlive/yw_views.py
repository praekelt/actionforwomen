from django.views.generic.edit import FormView
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404

from mama.sites.vlive.yw_forms import PMLYourStoryForm
from jmboyourwords.models import YourStoryCompetition


class PMLYourStoryView(FormView):
    form_class = PMLYourStoryForm
    template_name = 'yourwords/your_story.html'

    def get(self, request, *args, **kwargs):
        self.competition_id = int(kwargs['competition_id'])
        return super(PMLYourStoryView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(PMLYourStoryView, self).get_context_data(**kwargs)
        competition = get_object_or_404(
            YourStoryCompetition, 
            pk=self.competition_id)
        context['competition'] = competition
        return context

    def get_initial(self):
        initial = super(PMLYourStoryView, self).get_initial()
        initial['next'] = reverse('moms_stories_object_list')
        user = self.request.user
        initial['name'] = user.username
        initial['email'] = user.email
        return initial

    def form_valid(self, form):
        competition = get_object_or_404(
            YourStoryCompetition, 
            pk=self.competition_id)
        instance = form.save(commit=False)
        instance.user = self.request.user
        instance.your_story_competition = competition
        instance.save()
        return super(PMLYourStoryView, self).form_valid(form)

    def get_success_url(self):
        return reverse('moms_stories_object_list')
