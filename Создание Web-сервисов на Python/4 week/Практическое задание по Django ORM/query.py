from datetime import datetime

from django.db.models import Q, Count, Avg
from pytz import UTC

from .models import User, Blog, Topic


def create():
    u1 = User(first_name='u1', last_name='u1')
    u1.save()

    u2 = User(first_name='u2', last_name='u2')
    u2.save()

    u3 = User(first_name='u3', last_name='u3')
    u3.save()

    blog1 = Blog(title='blog1', author=u1)
    blog1.save()

    blog2 = Blog(title='blog2', author=u1)
    blog2.save()

    blog1.subscribers.add(u1, u2)
    blog1.save()

    blog2.subscribers.add(u2)
    blog2.save()

    topic_1 = Topic(title='topic1', blog=blog1, author=u1)
    topic_1.save()

    topic_2 = Topic(title='topic2_content', blog=blog1, author=u3, created='2017-01-01')
    topic_2.save()

    topic_1.likes.add(u1, u2, u3)
    topic_1.save()


def edit_all():
    users = User.objects.all()
    for user in users:
        user.first_name = 'uu1'
        user.save()


def edit_u1_u2():
    u1_u2 = User.objects.filter(Q(first_name='u1') | Q(first_name='u2'))
    for user in u1_u2:
        user.first_name = 'uu1'
        user.save()


def delete_u1():
    u1 = User.objects.get(first_name='u1')
    u1.delete()


def unsubscribe_u2_from_blogs():
    u2 = User.objects.get(first_name='u2')
    for blog in Blog.objects.all():
        blog.subscribers.remove(u2)
        blog.save()


def get_topic_created_grated():
    return Topic.objects.filter(created__gt='2018-01-01')


def get_topic_title_ended():
    return Topic.objects.filter(title__endswith='content')


def get_user_with_limit():
    return User.objects.all().order_by('-pk')[:2]


def get_topic_count():
    return Blog.objects.annotate(topic_count=Count('topic')).order_by('topic_count')


def get_avg_topic_count():
    return Blog.objects.annotate(topic_count=Count('topic')).aggregate(avg=Avg('topic_count'))


def get_blog_that_have_more_than_one_topic():
    return Blog.objects.annotate(topic_count=Count('topic')).filter(topic_count__gt=1)


def get_topic_by_u1():
    return Topic.objects.filter(author__first_name='u1')


def get_user_that_dont_have_blog():
    return User.objects.exclude(blog__author__isnull=False).order_by('pk')


def get_topic_that_like_all_users():
    user_count = User.objects.all().count()
    return Topic.objects.annotate(like_count=Count('likes')).filter(like_count=user_count)


def get_topic_that_dont_have_like():
    return Topic.objects.annotate(like_count=Count('likes')).filter(like_count=0)
