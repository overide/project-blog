from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from django.views.generic.edit import FormView, FormMixin
from django.db.models import Count
# from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Post
from taggit.models import Tag
from .forms import EmailPostForm, CommentForm


class PostDetailView(DetailView, FormMixin):
    template_name = 'blog/post/detail.html'
    form_class = CommentForm
    success_url = '.'
    context_object_name = 'post'
    slug_url_kwarg = 'post'

    def get_queryset(self):
        post = Post.objects.filter(slug=self.kwargs['post'],
                                   status='published',
                                   publish__year=self.kwargs['year'],
                                   publish__month=self.kwargs['month'],
                                   publish__day=self.kwargs['day'],)
        return post

    def get_context_data(self, **kwargs):
        context = super(PostDetailView, self).get_context_data(**kwargs)
        del context['form']
        post_tag_id = self.get_queryset()[0].tags.values_list('id', flat=True)
        similar_posts = Post.objects.filter(tags__in=post_tag_id)\
            .exclude(id=self.get_queryset()[0].id)
        similar_posts = similar_posts.annotate(same_tags=Count('tags'))\
            .order_by('-same_tags', '-publish')[:4]
        context['comment_form'] = self.get_form()
        context['comments'] = self.get_queryset()[0].comments.filter(active=True)
        context['similar_posts'] = similar_posts
        return context

    def form_valid(self, form):
        new_comment = form.save(commit=False)  # new comment, form form object
        new_comment.post = self.get_queryset()[0]
        new_comment.save()
        return super(PostDetailView, self).form_valid(form)

    # Because we are extending FormMixin, we have explicitly define
    # post method, object, form
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)


class PostListView(ListView):
    context_object_name = 'posts'
    # page_obj default name for page context object
    paginate_by = 5
    template_name = 'blog/post/list.html'

    def get_context_data(self, **kwargs):
        context = super(PostListView, self).get_context_data(**kwargs)
        if self.kwargs.get('post_tag', False):
            context['tag'] = self.kwargs['post_tag']
        return context

    def get_queryset(self):
        if self.kwargs.get('post_tag', False):
            tags = get_object_or_404(Tag, slug=self.kwargs['post_tag'])
            queryset = Post.objects.filter(status='published', tags__in=[tags])
        else:
            queryset = Post.published.all()

        return queryset


class PostShareView(FormView):
    template_name = 'blog/post/share.html'
    success_url = '.'
    form_class = EmailPostForm

    def get(self, request, *args, **kwargs):
        post = get_object_or_404(Post, id=self.kwargs[
                                 'post_id'], status='published')
        context = self.get_context_data()
        context['sent'] = False
        context['post'] = post
        return render(self.request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        return super(PostShareView, self).post(request, *args, **kwargs)

    def form_valid(self, form):
        post = get_object_or_404(Post, id=self.kwargs[
                                 'post_id'], status='published')
        # build a complete URL including HTTP schema and hostname
        post_url = self.request.build_absolute_uri(post.get_absolute_url())
        sent = form.send_email(post, post_url)
        context = self.get_context_data()
        context['sent'] = sent
        context['post'] = post
        context['cd'] = form.cleaned_data
        return render(self.request, self.template_name, context)

    def form_invalid(self, form):
        self.post = get_object_or_404(
            Post, id=self.kwargs['post_id'], status='published')
        return super(PostShareView, self).form_invalid(form)


# def post_list(request):
#     object_list = Post.published.all()
#     paginator = Paginator(object_list, 5)  # 5 post on each page
#     page = request.GET.get('page')
#     try:
#         page = paginator.page(page)
#     except PageNotAnInteger:
#         # If page is not an integer, deliver the first page
#         page = paginator.page(1)
#     except EmptyPage:
#         # If page is out of range deliver last page of result
#         page = paginator.page(paginator.num_pages)

#     return render(request,
#                   'blog/post/list.html',
#                   {'page': page},)


# def post_detail(request, year, month, day, post):
#     post = get_object_or_404(Post, slug=post,
#                              status='published',
#                              publish__year=year,
#                              publish__month=month,
#                              publish__day=day)
#     return render(request,
#                   'blog/post/detail.html',
#                   {'post': post})