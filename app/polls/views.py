from django.shortcuts import render, get_object_or_404 # shortcuts for common django tasks
from django.http import HttpResponseRedirect, HttpResponse
from django.template import loader
from django.urls import reverse

from .models import Choice, Question # These are models we created for the application

def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    template = loader.get_template('polls/index.html')
    context = {
        'latest_question_list': latest_question_list,
    }
    #output = ', '.join([q.question_text for q in latest_question_list])
    return render(request, 'polls/index.html', context)

def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/detail.html', {'question': question})

def results(request, question_id):
    response = "You're looking at the results of question %s."
    return HttpResponse(response % question_id)

def vote(request, question_id):
    # question holds the
    question = get_object_or_404(Question, pk=question_id) # pk is primary key, it treats question_id as the primary key of the object
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form
        # Since the initial form had an error, we want to give the user
        # another chance to fix the error and resubmit the form
        return render(request, 'poll/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a user hits
        # the Back button
        return HttpResponseRedirect(reverse('polls:results', args=(question.id)))

# Create your views here.
