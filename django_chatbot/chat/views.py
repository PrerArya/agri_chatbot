from django.shortcuts import redirect, render
from django.http import JsonResponse
import uuid
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from chat.models import Chat, Session
from chat.geminiscript import *


session_titles = []
chats = []
selected_language = ''



def generate_uuid():
    return str(uuid.uuid4())

def home(request):
    if request.user.is_authenticated:
        return redirect('chatbot')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('chatbot')
        
    return render(request, 'login.html')



def register_user(request):
    if request.user.is_authenticated:
        return redirect('chatbot')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')

        if password == password2:
            user = User.objects.create_user(
                username=username,
                password=password
            )
            user.first_name = first_name
            user.last_name = last_name
            user.email = email
            user.save()

            login(request, user)
            return redirect('chatbot')
    else:
        return render(request, 'register.html')
    return render(request, 'register.html')



def user_logout(request):
    logout(request)
    return redirect('home')



@login_required(login_url='home')
def chatbot(request):
    
    if request.method == 'POST':
        global selected_language
        selected_language = request.POST.get('language')
        print(selected_language)
        return render(request, 'index.html')
    return render(request, 'index.html')



def generate_chatbot_response(message):
   
    res = chatbot_call(selected_language,message=message)
    print(res)
    return res


def get_chatbot_response(request):
    
    if request.method == 'POST':
        user_message = request.POST.get('message')
        session_titles.append(user_message)
        chatbot_response = generate_chatbot_response(user_message)
        #chats list empty
        chat = Chat(
            id=generate_uuid(),
            message=user_message,
            response=chatbot_response,
        )
        chats.append(chat)
        return JsonResponse({'response': chatbot_response})



@login_required(login_url='home')
def save_chat(request):
    session = Session(
        id=generate_uuid(),
        title=session_titles[0],
        user=request.user,
    )
    session.save()
    for chat in chats:
        chat.session = session
        chat.save()
    chats.clear()
    session_titles.clear()
    return redirect('chatbot')



@login_required(login_url='home')
def load_chats(request, session_id):
    session  = Session.objects.get(id=session_id)
    session_titles.clear()
    session_titles.append(session.title)

    user_chats = Chat.objects.filter(session=session)
    for chat in user_chats:
        chats.append(chat)

    return render(request, 'index.html', {
        'chats': user_chats,
        'load': True,
    })



@login_required(login_url='home')
def delete_session(request, session_id):
    session  = Session.objects.get(id=session_id)
    session.delete()
    return redirect('history', request.user.username)



@login_required(login_url='home')
def history(request, username):
    user = User.objects.get(username=username)
    sessions = Session.objects.filter(user=user)

    return render(request, 'chats.html', {
        'sessions': sessions,

    })



@login_required(login_url='home')
def new_chat(request):
    session_titles.clear()
    chats.clear()
    return redirect('chatbot')