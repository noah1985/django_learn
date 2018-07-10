from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render


# Create your views here.
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('learning_logs:index'))


def register(request):
    if request.method != 'POST':
        form = UserCreationForm()
    else:

        form = UserCreationForm(data=request.POST)

        if form.is_valid():
            new_user = form.save()

            authenticate_user = authenticate(username=new_user.username,
                                             password=request.POST['password1'])
            login(request, authenticate_user)
            return HttpResponseRedirect(reverse('learning_logs:index'))

    context = {'form': form}
    return render(request, 'users/register.html', context)