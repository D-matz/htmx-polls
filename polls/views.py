from django.db.models import F, Q
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import logout
from django.utils.timezone import now
from django.contrib.auth.decorators import login_required
from django.middleware.csrf import get_token

from .models import Choice, Question
from .forms import QuestionForm, ChoiceForm

from time import sleep

def search_polls(request):
    query = request.GET.get('search', '')
    polls = []
    if query:
        if len(query) > 1:
            # Search in both Question and Choice models
            polls = Question.objects.filter(
                Q(question_text__icontains=query) |
                Q(choice__choice_text__icontains=query)
            ).distinct()
        context = {"questions": polls, "page_number": 9999999}
        return render(request, "polls/qlist.html", context)
    return load_more_questions(request, 0)

def create(request):
    if request.method == 'POST':
        q_form, c_form = QuestionForm(request.POST), ChoiceForm(request.POST)
        print(q_form, c_form)
        if q_form.is_valid() and c_form.is_valid():
            question = q_form.save(commit=False)
            question.pub_date = now()
            question.save()
            for choice_text in request.POST.getlist('choice_text'):
                if choice_text != "":
                    Choice.objects.create(question=question, choice_text=choice_text)
            context = {'questions': [question], 'page_number': 0}
            return render(request, "polls/qlist.html", context)
    else:
        q_form, c_form = QuestionForm(), ChoiceForm()
    return render(request, 'polls/create.html', {'q_form': q_form, 'c_form': c_form})

def get_question_list(page_number):
    start = (page_number - 1) * 5
    end = page_number * 5
    return Question.objects.filter(pub_date__lte=timezone.now()).order_by("-pub_date")[start:end]

def index(request):
    latest_question_list = get_question_list(1)
    q_form, c_form = QuestionForm(), ChoiceForm()
    context = {"questions": latest_question_list, 'q_form': q_form, 'c_form': c_form, "page_number": 1}
   # sleep(1)
    return render(request, "polls/index.html", context)

def load_more_questions(request, pagenum):
    nextpage = pagenum + 1
    more_question_list = get_question_list(nextpage)
    context = {"questions": more_question_list, "page_number": nextpage}
    return render(request, "polls/qlist.html", context)

def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, "polls/results.html", {"question": question})

def see_results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return HttpResponseRedirect(reverse("polls:results", args=(question.id,)))

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    print("hello 1", request.POST)
    try:
        selected_choice = question.choice_set.get(pk=request.POST["choice"])
        print("choice", selected_choice)
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(
            request,
            "polls/results.html",
            {
                "question": question,
                "error_message": "You didn't select a choice.",
            },
        )
    else:
        selected_choice.votes = F("votes") + 1
        selected_choice.save()
        return HttpResponseRedirect(reverse("polls:results", args=(question.id,)))

def user_signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('polls:index')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})

def user_logout(request):
    logout(request)
    #return render(request, "registration/userinfo.html")
    return redirect('polls:index')

def user_login(request):
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            print(username, password, form)
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
#                return render(request, "registration/userinfo.html")
                return redirect('polls:index')
    else:
        form = AuthenticationForm()
    return render(request, "registration/login.html", {"form": form})

def csrf(request):
    token = get_token(request)
    return render(request, "registration/csrf.html")
