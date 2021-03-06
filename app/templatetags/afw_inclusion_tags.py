from copy import copy
from datetime import datetime

from django.conf import settings
from django import template
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.urlresolvers import reverse
from django.db.models import Q
from django.template import Context, Template

from category.models import Category
from poll.models import Poll
from post.models import Post
from livechat.models import LiveChat

from app.templatetags.moms_stories_inclusion_tags \
    import your_story_competition


register = template.Library()


@register.inclusion_tag('app/inclusion_tags/topic_listing.html', takes_context=True)
def topic_listing(context, category_slug, more, limit=0):
    context = copy(context)
    try:
        category = Category.objects.get(slug__exact=category_slug)
    except Category.DoesNotExist:
        return {}
    object_list = Post.permitted.filter(
        Q(primary_category=category) |
        Q(categories=category)
    ).filter(categories__slug='featured').distinct()
    if limit:
        object_list = object_list[:limit]
    context.update({
        'category': category,
        'object_list': object_list,
        'full_heading': "More %s" % category.title if more else category.title
    })
    return context


@register.inclusion_tag('app/inclusion_tags/poll_listing.html', takes_context=True)
def poll_listing(context):
    context = copy(context)
    object_list = Poll.permitted.filter(categories__slug='featured').distinct()

    context.update({
        'object_list': object_list,
    })
    return context


@register.inclusion_tag('app/inclusion_tags/post_listing.html', \
        takes_context=True)
def post_listing(context, category_slug):
    result = _get_content_object_list(context, category_slug)
    result['object_list'] = result['object_list'][:2]
    return result


@register.inclusion_tag(
    'app/inclusion_tags/stories_listing.html', takes_context=True)
def stories_listing(context, category_slug):
    result = _get_content_object_list(context, category_slug)
    # Trim to 3 objects, or provide empty list if it doesn't have one.
    if 'object_list' in result:
        result['object_list'] = result['object_list'][:5]
    else:
        result['object_list'] = []
    competition = your_story_competition({})
    if competition:
        result.update(competition)
    return result


def _get_content_object_list(ctx_dict, category_slug):
    ctx_dict = copy(ctx_dict)
    try:
        category = Category.objects.get(slug__exact=category_slug)
    except Category.DoesNotExist:
        return ctx_dict
    object_list = Post.permitted.filter(
        Q(primary_category=category) | Q(categories=category),
        categories__slug='featured').distinct()

    ctx_dict.update({
        'category': category,
        'object_list': object_list.order_by('-publish_on'),
    })
    return ctx_dict


@register.inclusion_tag('app/inclusion_tags/pagination.html', takes_context=True)
def pagination(context, page_obj):
    context = copy(context)
    context.update({
        'page_obj': page_obj,
        'paginator': getattr(page_obj, 'paginator', None),
    })

    pages = []
    for page in page_obj.paginator.page_range:
        pages.append({
            'number': page ,
            'url': Template("{% load jmbo_template_tags %}{% smart_query_string 'page' " + str(page) + " %}").render(Context(context))
        })
    page_number = page_obj.number - 1
    if page_number < 3:
        slice_start = 0
    else:
        slice_start = page_number - 2
    if page_number + 2 >= len(pages):
        slice_start = len(pages) - 5
    context['pages'] = pages[slice_start: slice_start + 5]
    if page_obj.has_previous():
        context['previous_url'] = Template("{% load jmbo_template_tags %}{% smart_query_string 'page' page_obj.previous_page_number %}").render(Context(context))
    if page_obj.has_next():
        context['next_url'] = Template("{% load jmbo_template_tags %}{% smart_query_string 'page' page_obj.next_page_number %}").render(Context(context))

    return context


@register.inclusion_tag('app/inclusion_tags/vlive_object_comments.html', takes_context=True)
def vlive_object_comments(context, obj):
    def can_comment(obj, request):
        """
        Determine if user can comment.
        We don't use ModelBase.can_comment since that unnecessarily traverses to base.
        """
        # can't comment if commenting is closed
        if obj.comments_closed:
            return False

        # can't comment if commenting is disabled
        if not obj.comments_enabled:
            return False

        # anonymous users can't comment if anonymous comments are disabled
        if not request.user.is_authenticated() and not \
                obj.anonymous_comments:
            return False

        # can't comment if user is banned
        if request.user.is_authenticated() and request.user.profile.banned:
            return False

        return True

    def get_paginated_comments(obj, request):
        from django.contrib.comments.models import Comment
        from django.contrib.contenttypes.models import ContentType
        ctype = ContentType.objects.get_for_model(obj)
        comments = list(Comment.objects.filter(
            content_type=ctype,
            object_pk=obj.pk,
            is_public=True,
            is_removed=False,
            site__pk=settings.SITE_ID
        ).select_related('user').order_by('-submit_date'))

        paginator = Paginator(comments, 5)
        page = request.GET.get('page')

        try:
            page_comments = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            page_comments = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            page_comments = paginator.page(paginator.num_pages)

        return page_comments, len(comments)

    request = context['request']
    comments, count = get_paginated_comments(obj, request)
    context.update({
        'object': obj,
        'page_comments': comments,
        'comment_count': count,
        'can_render_comment_form': can_comment(obj, request),
    })

    return context


@register.inclusion_tag('app/includes/comments_include_no_likes.html', takes_context=True)
def mama_object_comments(context, obj):
    def can_comment(obj, request):
        """
        Determine if user can comment.
        We don't use ModelBase.can_comment since that unnecessarily traverses to base.
        """
        # can't comment if commenting is closed
        if obj.comments_closed:
            return False

        # can't comment if commenting is disabled
        if not obj.comments_enabled:
            return False

        # anonymous users can't comment if anonymous comments are disabled
        if not request.user.is_authenticated() and not \
                obj.anonymous_comments:
            return False

        return True

    def get_paginated_comments(obj, request):
        from django.contrib.comments.models import Comment
        from django.contrib.contenttypes.models import ContentType
        ctype = ContentType.objects.get_for_model(obj)
        comments = Comment.objects.filter(
            content_type=ctype,
            object_pk=obj.pk,
            is_public=True,
            site__pk=settings.SITE_ID
        ).order_by('-submit_date')

        page = request.GET.get('page')

        # if a specific page is requested, show many comments, paged
        if page:
            paginator = Paginator(comments, 5)
            try:
                page_comments = paginator.page(page)
            except PageNotAnInteger:
                # If page is not an integer, deliver first page.
                page_comments = paginator.page(1)
            except EmptyPage:
                # If page is out of range (e.g. 9999), deliver last page of results.
                page_comments = paginator.page(paginator.num_pages)

            return page_comments
        else:
            #if no specific page has been requested, only show the first five comments
            paginator = Paginator(comments, 5)
            return paginator.page(1)

    request = context['request']
    comments = get_paginated_comments(obj, request)
    context.update({
        'object': obj,
        'comments': comments,
        'can_comment': can_comment(obj, request),
    })
    return context
