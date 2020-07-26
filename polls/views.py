from django.shortcuts import render,get_object_or_404
from .models import Question, Choice, Voter
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.views import generic
from django.utils import timezone
from django.db.models import F,Count

class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        return Question.objects.annotate(count_choice = Count('choice')).exclude(count_choice = 1).filter(pub_date__lte = timezone.now(), choice__isnull = False).order_by('-pub_date')[:5]

class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'

    def get_queryset(self):
        return Question.objects.annotate(count_choice = Count('choice')).exclude(count_choice = 1).filter(pub_date__lte = timezone.now(), choice__isnull = False)

class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'

    def get_queryset(self):
        return Question.objects.annotate(count_choice = Count('choice')).exclude(count_choice = 1).filter(pub_date__lte = timezone.now(), choice__isnull = False)

def vote(request, question_id):
    question = get_object_or_404(Question,pk = question_id)
    if Voter.objects.filter(question_id=question_id, user_id=request.user.id).exists():
        return render(request, 'polls/detail.html', {'question': question ,'error_message': "Sorry, but you have already voted."})
    try:
        selected_choice = question.choice_set.get(pk = request.POST['choice'])
    except(KeyError,Choice.DoesNotExist):
        return render(request, 'polls/detail.html',{'question':question,'error_message': "You didn't select a choice!",})
    else:
        selected_choice.votes = F('votes') + 1
        selected_choice.save()
        selected_choice.refresh_from_db()
        for choice in question.choice_set.all():
            question.total_votes+=choice.votes
        for choice in question.choice_set.all():
            choice.percentage = int(round((choice.votes/question.total_votes)*100))
            choice.save()
        print(selected_choice.percentage)
        v = Voter(user=request.user, question = question)
        v.save()
        return HttpResponseRedirect(reverse('polls:results',args = (question.id,)))




