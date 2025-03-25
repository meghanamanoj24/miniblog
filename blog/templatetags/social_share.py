from django import template
from django.urls import reverse
from urllib.parse import quote_plus

register = template.Library()

@register.inclusion_tag('blog/includes/social_share_buttons.html', takes_context=True)
def social_share_buttons(context, post):
    request = context['request']
    current_url = request.build_absolute_uri(reverse('blog:post-detail', args=[post.slug]))
    title = quote_plus(post.title)
    
    return {
        'facebook_url': f"https://www.facebook.com/sharer/sharer.php?u={current_url}",
        'twitter_url': f"https://twitter.com/intent/tweet?text={title}&url={current_url}",
        'linkedin_url': f"https://www.linkedin.com/shareArticle?mini=true&url={current_url}&title={title}",
        'whatsapp_url': f"https://api.whatsapp.com/send?text={title}%20{current_url}",
        'email_url': f"mailto:?subject={title}&body=Check%20out%20this%20article:%20{current_url}",
        'post': post,
    } 