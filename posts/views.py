from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DetailView

from .forms import PostForm, CommentForm
from .helper import get_user_profile, check_following
from .models import Post, Comment, Group, Follow, User

pagination_count = 10


class PostListView(ListView):
    """ Gets a selection of 10 entries per page."""
    queryset = Post.objects.select_related('author', 'group').prefetch_related('comments')
    template_name = 'index.html'
    paginate_by = pagination_count
    context_object_name = 'page'


class GroupPostListView(ListView):
    """ Community page with posts."""
    paginate_by = pagination_count
    template_name = 'group.html'
    context_object_name = 'page'

    def get_queryset(self):
        group = get_object_or_404(Group, slug=self.kwargs['slug'])
        page = Post.objects.filter(group=group).select_related('author', 'group').prefetch_related('comments')
        return page


class PostCreateView(LoginRequiredMixin, CreateView):
    """
    Adds a new publication.
    After validating the form and creating a new post,
    the author is redirected to the main page.
    """
    model = Post
    template_name = 'new_post.html'
    form_class = PostForm
    success_url = reverse_lazy('index')
    extra_context = {
        'title': 'Новый пост',
        'btn_caption': 'Опубликовать'
    }

    def form_valid(self, form):
        post = form.save(commit=False)
        post.author = self.request.user
        return super().form_valid(form)


class ProfileView(ListView):
    """
    Adds a profile page with posts
    return: page "profile.html"
    """
    model = Post
    paginate_by = pagination_count
    template_name = 'profile.html'
    context_object_name = 'page'

    def get_queryset(self):
        author = get_user_profile(self.kwargs['username'])
        self.kwargs['profile'] = author
        return (
            author.posts.select_related('author', 'group').prefetch_related('comments')
        )

    def get_context_data(self, **kwargs):
        context = super(ProfileView, self).get_context_data(**kwargs)
        context['profile'] = self.kwargs['profile']
        context['following'] = check_following(self.request.user, context['profile'])
        return context


class PostDetailView(LoginRequiredMixin, DetailView):
    """
    Creates a Page for viewing a separate post
    return: page "post.html"
    """
    model = Post
    template_name = "post.html"
    form_class = CommentForm
    extra_context = {
        'form': CommentForm(),
    }

    def get_queryset(self):
        author = get_user_profile(self.kwargs['username'])
        self.kwargs['profile'] = author
        return (
            Post.objects.filter(id=self.kwargs['pk']).select_related('author', 'group').prefetch_related('comments')
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = self.kwargs['profile']
        context['following'] = check_following(self.request.user, context['profile'])
        context['comments'] = Comment.objects.filter(post_id=self.kwargs['pk']).select_related('author', 'post')
        return context

    @property
    def success_url(self):
        return reverse_lazy('post_view', kwargs={'username': self.request.user,
                                            'pk': self.object.pk})


class PostUpdateView(LoginRequiredMixin, UpdateView):
    """
       Creating a page for editing an existing post
       return: the page with the changed post.
    """
    model = Post
    form_class = PostForm
    template_name = "new_post.html"
    extra_context = {
        'title': 'Редактировать запись',
        'btn_caption': 'Сохранить'
    }

    def get_context_data(self, **kwargs):
        context = super(PostUpdateView, self).get_context_data(**kwargs)
        context['username'] = get_object_or_404(User, username=self.request.user)
        context['is_edit'] = True
        return context

    @property
    def success_url(self):
        return reverse_lazy('post_view', kwargs={'username': self.request.user,
                                            'pk': self.object.pk})


class CommentCreateView(LoginRequiredMixin, CreateView):
    """
    Creating a comment for editing an existing post
    return: the page with comment or the page for viewing the post.
    """
    model = Comment
    form_class = CommentForm
    template_name = "includes/comments.html"
    extra_context = {
        'comments_form': CommentForm()
    }

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.author = self.request.user
        self.object.post = Post.objects.get(pk=self.kwargs.get("post_id"))
        self.object.save()
        return super().form_valid(form)

    @property
    def success_url(self):
        return reverse_lazy('post_view', kwargs={'username': self.request.user,
                                            'pk': self.object.post.pk})


@login_required
def follow_index(request):
    """
    Displays posts of authors that the current user is subscribed to.
    :param request:
    :return: the page with posts of authors that the current user is subscribed to.
    """
    author = get_object_or_404(User, username=request.user)
    post_list = Post.objects.filter(author__following__user=request.user).select_related(
        'author', 'group').prefetch_related('comments')
    paginator = Paginator(post_list, pagination_count)
    page_number = request.GET.get("page")
    page = paginator.get_page(page_number)

    return render(request, "follow.html",
                  {"author": author,
                   "page": page,
                   "paginator": paginator,
                   })


@login_required
def profile_follow(request, username):
    """
    Subscribes to an interesting author.
    """
    author = get_object_or_404(User, username=username)
    follow = Follow.objects.filter(user=request.user, author=author).exists()
    if not request.user == author and follow is False:
        Follow.objects.create(user=request.user, author=author)
    return redirect("profile", username=username)


@login_required
def profile_unfollow(request, username):
    """
    Unsubscribes from the author.
    """
    author = get_object_or_404(User, username=username)
    Follow.objects.filter(user=request.user, author=author).delete()
    return redirect("profile", username=username)


def page_not_found(request, exception):  # noqa
    return render(request, "misc/404.html", {"path": request.path}, status=404)


def server_error(request):
    return render(request, "misc/500.html", status=500)
