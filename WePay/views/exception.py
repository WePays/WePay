from django.shortcuts import render


def handler404(request, *args, **argv):
    print('hello hoya')
    response = render(request, 'exception/404.html')
    print('Im comming')
    response.status_code = 404
    return response
