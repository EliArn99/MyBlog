@login_required
def home(request):
    return render(request, 'blog/home.html', {'user': request.user})


@login_required
def profile_view(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')  # Redirect to the same profile page or another page
    else:
        form = ProfileForm(instance=request.user)

    return render(request, 'blog/profile.html', {'form': form})


@login_required
def profile_edit_view(request):
    """View to edit the user profile."""
    if request.method == 'POST':
        form = ProfileEditForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = ProfileEditForm(instance=request.user)
    return render(request, 'blog/profile_edit.html', {'form': form})


def post_list(request):
    query = request.GET.get('q', '')
    posts = Post.objects.filter(status='published')

    if query:
        posts = posts.filter(
            Q(title__icontains=query) |
            Q(categories__name__icontains=query) |
            Q(tags__name__icontains=query)
        ).distinct()

    # Pagination: 10 posts per page
    paginator = Paginator(posts, 9)  # Show 10 posts per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'blog/post_list.html', {'page_obj': page_obj, 'query': query})


def post_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user  # Set the logged-in user as the author
            post.status = 'published'  # Ensure the post is published immediately
            post.save()
            form.save_m2m()  # Save tags
            return redirect('post_list')
    else:
        form = PostForm()
    return render(request, 'blog/post_form.html', {'form': form})


@login_required
def post_edit(request, post_id):
    post = get_object_or_404(Post, id=post_id, author=request.user)
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('post_list')
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_form.html', {'form': form})
