from copy import copy
from datetime import datetime

from category.models import Category
from django import template
from django.core.urlresolvers import reverse
from django.db.models import Q
from django.template import Context, Template
from poll.models import Poll
from post.models import Post


register = template.Library()


@register.inclusion_tag('mama/inclusion_tags/ages_and_stages.html',
                        takes_context=True)
def ages_and_stages(context):
    context = copy(context)
    user = context['request'].user
    if user.is_authenticated():
        profile = user.profile
        context.update({'profile': profile})
        delivery_date = profile.delivery_date
        if delivery_date:
            now = datetime.now().date()
            pre_post = 'pre' if profile.is_prenatal() else 'post'
            week = 42 - ((delivery_date - now).days / 7) if profile.is_prenatal() else (now - delivery_date).days / 7
        else:
            # Defaults in case user does not have delivery date.
            pre_post = 'pre'
            week = 21
        try:
            category = Category.objects.get(slug="my-pregnancy" if profile.is_prenatal() else "my-baby")
            context.update({
                'category': category,
            })
        except Category.DoesNotExist:
            return context

        try:
            week_category = Category.objects.get(slug="%snatal-week-%s" % (pre_post, week))
        except Category.DoesNotExist:
            context.update({
                'object_list': [],
            })
            return context
        object_list = Post.permitted.filter(Q(primary_category=week_category) |
                                            Q(categories=week_category)).distinct()
        context.update({
            'object_list': object_list,
        })
    return context


@register.inclusion_tag('mama/inclusion_tags/page_header.html', takes_context=True)
def page_header(context):
    context = copy(context)
    help_post = Post.permitted.filter(slug='mama-help')
    if help_post:
        context.update({
            'help_post': help_post[0],
        })
    return context


@register.inclusion_tag('mama/inclusion_tags/page_header.html', takes_context=True)
def pml_page_header(context):
    context = copy(context)
    help_post = Post.permitted.filter(slug='mama-help')
    links = [
        {
            'title': 'Home',
            'url': reverse('home'),
        },
        {
            'title': 'A-to-Z',
            'url': reverse('category_object_list', kwargs={'category_slug': 'mama-a-to-z'}),
        },
        {
            'title': 'Life Guides',
            'url': reverse('category_object_list', kwargs={'category_slug': 'life-guides'}),
        },
        {
            'title': 'Articles',
            'url': reverse('category_object_list', kwargs={'category_slug': 'articles'}),
        },
        {
            'title': "Moms' Stories",
            'url': reverse('category_object_list', kwargs={'category_slug': 'moms-stories'}),
        }
    ]
    if help_post:
        links.append(
            {
                'title': 'Help',
                'url': help_post[0].get_absolute_category_url(),
            }
        )
    context['links'] = links
    return context


@register.inclusion_tag('mama/inclusion_tags/topic_listing.html')
def topic_listing(category_slug, more):
    try:
        category = Category.objects.get(slug__exact=category_slug)
    except Category.DoesNotExist:
        return {}
    object_list = Post.permitted.filter(
        Q(primary_category=category) |
        Q(categories=category)
    ).filter(categories__slug='featured').distinct()
    return {
        'category': category,
        'object_list': object_list,
        'full_heading': "More %s" % category.title if more else category.title
    }


@register.inclusion_tag('mama/inclusion_tags/poll_listing.html', takes_context=True)
def poll_listing(context):
    context = copy(context)
    object_list = Poll.permitted.filter(categories__slug='featured').distinct()

    context.update({
        'object_list': object_list,
    })
    return context


@register.inclusion_tag('mama/inclusion_tags/post_listing.html', \
        takes_context=True)
def post_listing(context, category_slug):
    context = copy(context)
    try:
        category = Category.objects.get(slug__exact=category_slug)
    except Category.DoesNotExist:
        return {}
    object_list = Post.permitted.filter(Q(primary_category=category) | \
            Q(categories=category)).filter(categories__slug='featured').distinct()

    context.update({
        'category': category,
        'object_list': object_list,
    })
    return context


@register.inclusion_tag('mama/inclusion_tags/pagination.html', takes_context=True)
def pagination(context, page_obj):
    context = copy(context)
    context.update({
        'page_obj': page_obj,
        'paginator': getattr(page_obj, 'paginator', None),
    })
    if page_obj.has_previous():
        context['previous_url'] = Template("{% load jmbo_template_tags %}{% smart_query_string 'page' page_obj.previous_page_number %}").render(Context(context))
    if page_obj.has_next():
        context['next_url'] = Template("{% load jmbo_template_tags %}{% smart_query_string 'page' page_obj.next_page_number %}").render(Context(context))

    return context


@register.inclusion_tag('mama/inclusion_tags/babycenter_byline.html')
def babycenter_byline(obj):
    if obj.categories.filter(slug='bc-content'):
        return {'display': True}
    else:
        return {}
