from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Post
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
# Create your views here.

def login_view(request):
     # if post, then authenticate (user submitted username and password)
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            u = form.cleaned_data['username']
            p = form.cleaned_data['password']
            user = authenticate(username = u, password = p)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect('/user/'+u)
                else:
                    print('The account has been disabled.')
                    return HttpResponseRedirect('/login')
            else:
                print('The username and/or password is incorrect.')
                return HttpResponseRedirect('/login')
    else: # it was a get request so send the emtpy login form
        form = AuthenticationForm()
        return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/posts')

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('/posts')
        else:
            print('invalid form')
            return render('/signup')
    else:
        form = UserCreationForm()
        return render(request, 'signup.html', {'form': form})


def about(request):
  return render(request, 'about.html')

def index(request):
  return render(request, 'index.html')


def posts_index(request):
    posts = Post.objects.all()
    return render(request, 'posts/index.html', {'posts': posts})

def posts_show(request, post_id):
    post = Post.objects.get(id=post_id)
    return render(request, 'posts/show.html', {'post': post})

class PostCreate(CreateView):
  model = Post
  # fields = '__all__'
  fields = ['name', 'location', 'review', 'rating']
  success_url = '/posts'
  
  def form_valid(self, form):
      self.object = form.save(commit=False)
      self.object.user = self.request.user
      self.object.save()
      return HttpResponseRedirect('/posts/' + str(self.object.pk))

class PostUpdate(UpdateView):
  model = Post
  fields = ['name', 'location', 'review', 'rating']

  def form_valid(self, form):
    self.object = form.save(commit=False)
    self.object.save()
    # return HttpResponseRedirect('/posts/' + str(self.object.pk))
    return HttpResponseRedirect('/posts/')

@method_decorator(login_required, name='dispatch')
class PostDelete(DeleteView):
  model = Post
  success_url = '/posts'
  
@login_required
def profile(request, username):
    user = User.objects.get(username=username)
    posts = Post.objects.filter(user=user)
    return render(request, 'profile.html', {'username': username, 'posts': posts})