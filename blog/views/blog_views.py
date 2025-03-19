from django.shortcuts import render


def BlogView(request):
    # template_name ='blog.html'
    return render(request,'blog.html')