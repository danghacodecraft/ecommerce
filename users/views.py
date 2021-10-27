from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from store.my_module import check_session
from .forms import FormUser, FormUserProfileInfo

def users(request):
    session_status_users = check_session(request, 'sessionUser')
    session_info_users = ''
    if session_info_users:
        session_info_users = request.session.get('sessionUser')

    result_register = ''
    form_user = FormUser()
    form_profile = FormUserProfileInfo()
    if request.POST.get('btnRegister'):
        form_user = FormUser(request.POST)
        form_profile = FormUserProfileInfo(request.POST, request.FILES)
        if form_user.is_valid() and form_profile.is_valid() and form_user.cleaned_data['password'] == form_user.cleaned_data['confirm_password']:
            user = form_user.save()
            user.set_password(user.password)
            user.save()

            # Profile
            profile = form_profile.save(commit=False)
            profile.user = user
            profile.save()

            result_register = '''
                <div class="alert alert-success alert-dismissible fade show" role="alert">
                    Đăng ký thông tin thành công
                    <button type="button" class="close" data-dismiss="alert" aria-label="Close">
                        <span aria-hidden="true">&times;</span>
                    </button>
                </div>
                '''
        else:
            result_register = '''
                <div class="alert alert-danger alert-dismissible fade show" role="alert">
                    Đăng ký thông tin thất bại
                    <button type="button" class="close" data-dismiss="alert" aria-label="Close">
                        <span aria-hidden="true">&times;</span>
                    </button>
                </div>
                '''

        if request.POST.get('btnLogin'):
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                request.session['sessionUser'] = username
                return redirect('users:users')
    return render(request, 'users/users.html', {
        'form_user': form_user,
        'form-profile': form_profile,
        'result_register': result_register,
        'session_status_users': session_status_users,
        'session_info_user': session_info_users,
    })