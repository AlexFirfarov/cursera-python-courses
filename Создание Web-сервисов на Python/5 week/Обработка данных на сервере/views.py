import json

from django.http import HttpResponse, JsonResponse
from django.views import View

from .models import Item, Review

from django.core.exceptions import ObjectDoesNotExist

from jsonschema import validate
from jsonschema.exceptions import ValidationError


SCHEMA_ADD_ITEM = {
    '$schema': 'http://json-schema.org/schema#',
    'type': 'object',
    'properties': {
        'title': {
            'type': 'string',
            'minLength': 1,
            'maxLength': 64,
            'pattern': '\D',
        },
        'description': {
            'type': 'string',
            'minLength': 1,
            'maxLength': 1024,
            'pattern': '\D',
        },
        'price': {
            'type': 'integer',
            'minimum': 1,
            'maximum': 1000000
        },
    },
    'required': ['title', 'description', 'price']
}

SCHEMA_ADD_REVIEW = {
    '$schema': 'http://json-schema.org/schema#',
    'type': 'object',
    'properties': {
        'text': {
            'type': 'string',
            'minLength': 1,
            'maxLength': 1024,
            'pattern': '\D',
        },
        'grade': {
            'type': 'integer',
            'minimum': 1,
            'maximum': 10
        },
    },
    'required': ['text', 'grade']
}


class AddItemView(View):
    """View для создания товара."""

    def post(self, request):
        try:
            data = json.loads(request.body)
            validate(data, SCHEMA_ADD_ITEM)
        except (json.JSONDecodeError, ValidationError):
            return JsonResponse({}, status=400)

        item = Item.objects.create(
            title=data['title'], description=data['description'], price=data['price'])
        return JsonResponse({"id": item.id}, status=201)


class PostReviewView(View):
    """View для создания отзыва о товаре."""

    def post(self, request, item_id):
        try:
            data = json.loads(request.body)
            validate(data, SCHEMA_ADD_REVIEW)
        except (json.JSONDecodeError, ValidationError):
            return JsonResponse({}, status=400)

        try:
            item = Item.objects.get(pk=item_id)
        except ObjectDoesNotExist:
            return JsonResponse({}, status=404)

        review = Review.objects.create(
            grade=data['grade'], text=data['text'], item=item)
        return JsonResponse({"id": review.id}, status=201)


class GetItemView(View):
    """View для получения информации о товаре.

    Помимо основной информации выдает последние отзывы о товаре, не более 5
    штук.
    """

    def get(self, request, item_id):
        try:
            item = Item.objects.get(pk=item_id)
        except ObjectDoesNotExist:
            return JsonResponse({}, status=404)

        reviews = Review.objects.filter(
            item__id=item_id).order_by('-id')[:5]
        review_list = [{'id': review.id, 'text': review.text,
                        'grade': review.grade} for review in reviews]
        response = {
            'id': item_id,
            'title': item.title,
            'description': item.description,
            'price': item.price,
            'reviews': review_list
        }
        return JsonResponse(response, status=200)
