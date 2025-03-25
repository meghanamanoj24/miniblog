from .models import Post, Category

def common_context(request):
    """
    Add common context variables to all templates
    """
    return {
        'recent_posts': Post.objects.all().order_by('-created_date')[:5],
        'categories': Category.objects.all(),
    }