from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from events.models import Event, Review
from django.contrib.auth.models import User
from django.views.decorators.http import require_POST
from django.http import HttpResponse
from datetime import datetime


# Create your views here.


def event_list(request):
    template_name = 'events/event_list.html'
    event_objects = Event.objects.all()
    context = {
        'event_objects': event_objects,
    }
    return render(request, template_name, context)


def event_detail(request, pk):
    template_name = 'events/event_detail.html'
    event = get_object_or_404(Event, pk=pk)
    review_objects = event.reviews.all()
    context = {
        'event': event,
        'rate': event.rate,
        'review_objects': review_objects,
    }
    return render(request, template_name, context)


@require_POST
def create_review(request):
    rate = ''
    text = ''
    user_name = ''
    formatted_date = ''

    if request.user and request.user.is_authenticated:

        event_id = request.POST.get('event_id')
        rate = request.POST.get('rate')
        text = request.POST.get('text')
        msg = ''
        event = get_object_or_404(Event, pk=event_id)
        user_id = get_object_or_404(User, pk=request.user.id)
        user_name = request.user.username
        date = datetime.now()
        formatted_date = date.strftime('%d.%m.%Y')
        review_already_created = False

        user_id_list = []
        for review in event.reviews.all():
            user_id_list.append(review.user.id)
        if user_id.id in user_id_list:
            review_already_created = True

        new_review = Review(user=user_id,
                            event=event,
                            rate=rate,
                            text=text,
                            created=formatted_date,
                            updated=formatted_date
                            )

        if review_already_created:
            validity = False
            msg = 'Вы уже оставляли отзыв к этому событию'
        elif rate == '' or text == '':
            validity = False
            msg = 'Оценка и текст отзыва - обязательные поля'
        else:
            validity = True
            new_review.save()
    else:
        validity = False
        msg = 'Отзывы могут оставлять только зарегистрированные пользователи'

    data = {
        'ok': validity, # True если отзыв создан успешно, False в противном случае,
        'msg': msg,  # Сообщение об ошибке
        'rate': rate,  # Оценка отзыва
        'text': text,  # Текст отзыва
        'created': formatted_date,  # Дата создания отзыва в формате DD.MM.YYYY
        'user_name': user_name,  # Полное имя пользователя
    }

    return JsonResponse(data)
