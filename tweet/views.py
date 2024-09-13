from django.shortcuts import render
from .models import Tweet
from .forms import TweetForm,UserRegistrationForm
from django.shortcuts import get_object_or_404,redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login,authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login

# Create your views here.
def index(request):
    return render(request, 'index.html')

def tweet_list(request):
    tweets=Tweet.objects.all().order_by('-created_at')
    return render(request, 'tweet_list.html',{'tweets':tweets})

def tweet_create(request):
    if request.method=="POST":
       form=TweetForm(request.POST, request.FILES)
       if form.is_valid():
           tweet=form.save(commit=False)
           tweet.user=request.user
           tweet.save()
           return redirect('tweet_list')

    else:
        form= TweetForm()
    return render(request,'tweet_form.html',{'form':form})

def tweet_edit(request,tweet_id):
    tweet=get_object_or_404(Tweet,pk=tweet_id,user=request.user)
    if request.method=='POST':
        form=TweetForm(request.POST, request.FILES,instance=tweet)
        if form.is_valid():
           tweet=form.save(commit=False)
           tweet.user=request.user
           tweet.save()
           return redirect('tweet_list')
        
    else:
        form=TweetForm(instance=tweet)
    return render(request,'tweet_form.html',{'form':form})

def tweet_delete(request ,tweet_id):
    tweet = get_object_or_404(Tweet, pk=tweet_id, user=request.user)
    if request.method=='POST':
        tweet.delete()
        return redirect('tweet_list')
    return render(request,'tweet_confirm_delete.html',{'tweet':tweet})
    

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password1'])
            user.save()
            login(request, user)  # Pass both request and user
            return redirect('tweet_list')
    else:
        form = UserRegistrationForm()
    return render(request, 'registration/register.html', {'form': form})

def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)  
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)  
            if user is not None:
                login(request, user)  
                return redirect('tweet_list') 
            else:
                form.add_error(None, 'Invalid username or password')  
    else:
        form = AuthenticationForm() 

    return render(request, 'registration/login.html', {'form': form})
    