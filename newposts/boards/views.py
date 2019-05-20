from django.shortcuts import render, get_object_or_404, redirect
from .models import Board, Topic, Posts
from django.http import HttpResponse
from django.contrib.auth.models import User
from .forms import NewTopicForm

# Create your views here.
def home_view(request):
	boards = Board.objects.all()
	return render(request, 'home.html',{'boards': boards})

def board_topics_view(request, pk):
	board = Board.objects.get(id=pk)
	return render(request, 'topics.html', {'board':board})

def new_topic_view(request, pk):
	board = get_object_or_404(Board, id=pk)
	user = User.objects.first()
	if request.method == 'POST':
		form = NewTopicForm(request.POST)
		if form.is_valid():
			topic = form.save(commit=False)
			topic.board = board
			topic.starter = user
			topic.save()
			post= Posts.objects.create(message=form.cleaned_data.get('message'),topic=topic, created_by=user)
			return redirect('board_topics', pk=board.pk)
	else:
		form = NewTopicForm()
	return render(request, 'new_topic.html', {'board': board, 'form': form })


	
	
