from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import View

from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Profile
from .forms import LoginForm, UserRegistrationForm,UserEditForm,ProfileEditForm
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.views.generic import CreateView



def custom_logout(request):
    logout(request)
    return render(request, 'registration/logged_out.html')



def user_login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            print(data)
            user = authenticate(request,
                                username=data['username'],
                                password=data['password'])

            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponse('Muvaffaqiyatli login amalga oshirildi')
                else:
                    return HttpResponse('Sizning profilingiz faol emas')
            else:
                return HttpResponse('Login va parolda xatolik bor!')
    else:
        form = LoginForm()
    return render(request, 'registration/login.html', {"form": form})


@login_required
def dashbord_view(request):
    user = request.user
    profil_info = Profile.objects.get(user=user)
    context = {
        'user':user,
        "profile":profil_info
    }

    return render(request,'pages/user_profile.html', context)






def user_register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(
                user_form.cleaned_data["password"]
            )
            new_user.save()
            Profile.objects.create(user=new_user)
            context = {
                "new_user":new_user
            }

            return render(request,"account/register_done.html/", context=context)


    else:
        user_form = UserRegistrationForm()
        context = {
            "user_form":user_form
        }
        return render(request,'account/register.html',{"user_form": user_form})



class SignUpView(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy("login")
    template_name = 'account/register.html'





@login_required
def edit_user(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user, data=request.POST)
        profile_form = ProfileEditForm(instance=request.user.profile,
                                       data=request.POST,
                                       files=request.FILES)

        print("User form valid:", user_form.is_valid())
        print("Profile form valid:", profile_form.is_valid())

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('user_profile')  # Sahifaga qaytarish
        #print("Profile form errors:", profile_form.errors)


    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)

    return render(request, 'account/profile_edit.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })
    #print("Profile form errors:", profile_form.errors)



class EditUserView(LoginRequiredMixin,View):

    def get(self, request):
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)

        return render(request, 'account/profile_edit.html', {
            'user_form': user_form,
            'profile_form': profile_form
        })

    def post(self, request):
        user_form = UserEditForm(instance=request.user, data=request.POST)
        profile_form = ProfileEditForm(instance=request.user.profile,
                                       data=request.POST,
                                       files=request.FILES)

        print("User form valid:", user_form.is_valid())
        print("Profile form valid:", profile_form.is_valid())

        # Form errors
        if not user_form.is_valid():
            print("User Form Errors:", user_form.errors)
        if not profile_form.is_valid():
            print("Profile Form Errors:", profile_form.errors)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('user_profile')  # Sahifaga qaytarish













