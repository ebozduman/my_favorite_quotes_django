from django.shortcuts import render, redirect
from django.contrib import messages
from .models import User
from .models import Quote

def index(request):
    return render(request, 'login_reg/index.html')

def register_process(request):
    postData = {
        'first_name' : request.POST['first_name'],
        'alias' : request.POST['alias'],
        'email' : request.POST['email'],
        'password' : request.POST['password'],
        'conf_pwd' : request.POST['conf_pwd']
    }
    ret = User.objects.register(postData)
    if ret['success']:
        id = User.objects.get(email=postData['email']).id
        request.session['id'] = id
        return redirect('/show_home')
    else:
        for msg in ret['msg_list']:
            messages.error(request, msg)
        return redirect('/')

def login_process(request):
    postData = {
        'email' : request.POST['email'],
        'password' : request.POST['password']
    }
    ret = User.objects.login(postData)
    if ret['success']:
        id = User.objects.get(email=postData['email']).id
        request.session['id'] = id
        return redirect('/show_home')
    else:
        for msg in ret['msg_list']:
            messages.error(request, msg)
        return redirect('/')

def show_home(request):
    print "Entered show_home"
    if 'id' in request.session:
        user_id = request.session['id']
        user = User.objects.get(id=user_id)
        quotes_list = Quote.objects.all()
        print "quotes_list", quotes_list
        fav_quotes_list = user.quote_set.all()
        print "fav_quotes_list", fav_quotes_list
        if fav_quotes_list:
            quotes_to_exclude=[q.quote_text for q in fav_quotes_list]
            quotes_list = Quote.objects.exclude(quote_text__in=quotes_to_exclude)
        print "quotes_list after exclude: ", quotes_list
        for quote in quotes_list:
            print "quote.id = ", quote.id
            print "quote.pk = ", quote.pk
            print "quote.quote_text = ", quote.quote_text
            if not quote.quoted_by:
                quote.quoted_by ='Unknown Source'
            print "quote.quoted_by = ", quote.quoted_by
            print "quote.poster_id = ", quote.poster_id
            print "quote.poster_alias = ", quote.poster_alias
        context = {
            'user': user,
            'quotes_list': quotes_list,
            'favorites_list': fav_quotes_list
        }
        return render(request, 'login_reg/show_home.html', context)
    else:
        print "else"
        return redirect('/')

def add_quote(request):
    print "Entered add_quote"
    print "request.session[id]", request.session['id']
    postData = {
        'quote_text' : request.POST['quote_textarea'],
        'quoted_by' : request.POST['quoted_by'],
        'user_id' : request.session['id']
    }
    ret = Quote.objects.add_quote(postData)
    print ret
    if not ret['success']:
        print "Failure of add quote"
        for msg in ret['msg_list']:
            messages.error(request, msg)
    return redirect('/show_home')

def add_show_my_favorites(request):
    print "Entered add_show_my_favorites"
    postData={
        'user_id': request.session['id'],
        'quote_id': request.POST['quote_id']
    }
    favorites_list = Quote.objects.add_fav(postData)
    print favorites_list
    for f in favorites_list:
        print "f.quoted_by", f.quoted_by
        print "f.quote_text", f.quote_text
    context = {
        'favorites_list': favorites_list,
        'count': favorites_list.count()
    }
    return redirect('/show_home')

def remove_from_my_list(request):
    postData={
        'user_id': request.session['id'],
        'quote_id': request.POST['quote_id']
    }
    favorites_list = Quote.objects.remove_from_my_list(postData)
    for f in favorites_list:
        print "f.quoted_by", f.quoted_by
        print "f.quote_text", f.quote_text
    context = {
        'favorites_list': favorites_list,
    }
    return redirect('/show_home')

def show_poster_favorites(request, poster_id):
    postData={
        # 'user_id': request.session['id'],
        'poster_id': poster_id
    }
    poster = User.objects.get(id=poster_id)
    poster_list = Quote.objects.get_poster_list(postData)
    for p in poster_list:
        print "p.quoted_by", p.quoted_by
        print "p.quote_text", p.quote_text
    context = {
        'poster_alias' : poster.alias,
        'poster_list': poster_list,
        'count': poster_list.count(),
    }
    return render(request, 'login_reg/show_poster_list.html', context)

def logout(request):
    print "logout"
    request.session.flush()
    return index(request)
