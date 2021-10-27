from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from polls.form import CreateUserForm


def signup(request):
    form = CreateUserForm()

    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.save()
            login(request, user)
            return redirect('polls:index')
    else:
         form = CreateUserForm()
    context = {'form':form}
    return render(request,
                  'registration/signup.html',
                  {'form':form})
