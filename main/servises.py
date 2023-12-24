import requests

from virtual_university import settings
from .models import Payment


def checkout_session(course, user):
    headers = {'Authorization': f'Bearer {settings.STRIPE_API_KEY}'}

    data = [
        ('amount', course.price),
        ('currency', 'usd'),
    ]
    response = requests.post(f'{settings.STRIPE_URL}/payment_intents', headers=headers, data=data)
    if response.status_code != 200:
        raise Exception(f'error while creating payment : {response.json()["error"]["message"]}')
    return response.json()


def create_payment(course, user, session):
    Payment.objects.create(
        course=course,
        user=user,
        amount=course.price,
        paiment_intent_id=session['id']
    )
