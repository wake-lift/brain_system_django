import os

from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import render
from dotenv import load_dotenv

from .forms import FeedbackForm

load_dotenv(dotenv_path=settings.BASE_DIR / '.env')


def feedback(request):
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        context = {'form': form}
        if form.is_valid():
            email_message = '\n\n'.join(
                f'{key}: {value}' for key, value in form.cleaned_data.items()
            )
            send_mail(
                subject='Новое сообщение в обратной связи',
                message=email_message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=os.getenv('RECIPIENT_LIST').split(),
                fail_silently=True,
            )
            form.save()
            context['form_saved'] = True
    else:
        form = FeedbackForm()
        context = {'form': form}
        context['form_saved'] = False
    return render(request, 'common_pages/feedback.html', context)


def page_not_found(request, exception):
    return render(request, 'common_pages/404.html', status=404)


def csrf_failure(request, reason=''):
    return render(request, 'common_pages/403csrf.html', status=403)


def forbidden(request, exception):
    return render(request, 'common_pages/403.html', status=403)


def bad_request(request, exception):
    return render(request, 'common_pages/400.html', status=400)


def internal_server_error(request):
    return render(request, 'common_pages/500.html', status=500)
