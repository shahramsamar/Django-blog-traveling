from django.shortcuts import render


def BlogView(request):
    # template_name ='blog.html'
    return render(request,'blog.html')

def SingleBlogView(request):
    return render(request,'single.html')