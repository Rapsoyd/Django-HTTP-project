from django.shortcuts import render, get_object_or_404, redirect, HttpResponseRedirect
from legend_blog.models import Post, PostReaction, PostComment
from django.views.generic import ListView, DetailView, View, UpdateView, CreateView
from django.db.models import Count, OuterRef, Subquery
from legend_blog.forms import PostCreateForm, PostUpdateForm, RateForm, CommentForm
from django.views.decorators.http import require_POST
from django.db.models import F


class PostListView(ListView):
    model = Post
    template_name = "blog/post_list.html"
    context_object_name = "posts"
    paginate_by = 2

    def get_queryset(self):
        queryset = super().get_queryset()
        subquery = (PostReaction.objects.filter(
            post_id=OuterRef("id")).values("post_id").annotate(
            reaction_count=Count("id")).values("reaction_count"))
        queryset = queryset.annotate(reaction_count=Subquery(subquery))
        for item in queryset:
            if item.reaction_count is None:
                item.reaction_count = 0
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Главная страница"
        return context


class PostDetailView(DetailView):
    model = Post
    template_name = "blog/post_detail.html"
    context_object_name = "post"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = self.object.title
        user = self.request.user
        post = self.object
        comments = PostComment.objects.filter(post=post)
        comment_form = CommentForm
        form = RateForm()
        context["comments"] = comments
        context["form"] = form
        context["comment_form"] = comment_form
        if user.is_authenticated:
            # Получение реакции пользователя на этот пост
            post_reaction = (PostReaction.objects.select_related(
                "user", "post").filter(post=post, user=user).first())
            initial_data = {
                "rate": post_reaction.reaction
            } if post_reaction else {}
            context['initial_data'] = initial_data
        return context


@require_POST
def post_reaction(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    form = RateForm(data=request.POST)
    user = request.user
    reaction = None
    if form.is_valid():
        try:
            reaction = PostReaction.objects.filter(user=user, post=post).get()
            reaction.reaction = form.cleaned_data.get("rate")
            reaction.save()
        except PostReaction.DoesNotExist:
            reaction = form.save(commit=False)
            reaction.post = post
            reaction.user = user
        reaction.save()
    return render(request, "blog/post_detail.html", {
        "post": post,
        "form": form,
        "comment": reaction
    })


class PersonListView(ListView):
    model = Post
    template_name = "blog/person_posts.html"
    context_object_name = "posts"
    paginate_by = 2

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.is_authenticated:
            queryset = queryset.filter(author=self.request.user)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Мои посты"
        return context


class PostDeleteView(View):

    def post(self, request, post_id):
        post = get_object_or_404(Post, pk=post_id)
        if post.author == request.user:
            post.delete()
        return redirect("person_posts")


class PostCreateView(CreateView):
    model = Post
    template_name = "blog/post_create.html"
    form_class = PostCreateForm
    extra_context = {"title": "Добавление статьи на сайт"}

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect(to="/")

        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.save()
        return super().form_valid(form)


class PostUpdateView(UpdateView):
    model = Post
    template_name = "blog/post_update.html"
    form_class = PostUpdateForm

    def get_context_data(self, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = f"Обновление статьи: {self.request.user}"
        return context

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.save()
        return super().form_valid(form)


@require_POST
def post_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    comment = None
    form = CommentForm(data=request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.post = post
        comment.save()
    return render(request, "blog/comment.html", {
        "post": post,
        "form": form,
        "comment": comment
    })
