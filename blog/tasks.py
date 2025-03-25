from django.utils import timezone
from django.db.models import Count, F
from django.db import transaction
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from .models import Post, Share

def send_milestone_notification(post, milestone, platform=None):
    """
    Send email notification when a post reaches a share milestone
    """
    subject = f'Share Milestone Reached: {post.title}'
    
    context = {
        'post_title': post.title,
        'post_url': post.get_absolute_url(),
        'milestone': milestone,
        'total_shares': post.total_shares,
        'social_reach': post.social_reach,
        'platform': platform
    }
    
    html_message = render_to_string('blog/emails/share_milestone.html', context)
    plain_message = f"""
    Your post "{post.title}" has reached a new milestone!
    
    Total Shares: {post.total_shares}
    Milestone: {milestone}
    Estimated Social Reach: {post.social_reach:,} people
    
    View your post: {post.get_absolute_url()}
    """
    
    # Send to post author
    send_mail(
        subject=subject,
        message=plain_message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[post.author.email],
        html_message=html_message
    )

def check_share_milestones(post):
    """
    Check if post has reached any share milestones
    """
    milestones = [10, 50, 100, 500, 1000, 5000, 10000]
    platform_milestones = [5, 25, 50, 100, 500]
    
    # Check total share milestones
    for milestone in milestones:
        if post.total_shares >= milestone and not post.reached_milestones.filter(milestone=milestone).exists():
            send_milestone_notification(post, milestone)
            post.reached_milestones.create(milestone=milestone, type='total')
    
    # Check platform-specific milestones
    platforms = {
        'facebook': post.facebook_shares,
        'twitter': post.twitter_shares,
        'linkedin': post.linkedin_shares,
        'whatsapp': post.whatsapp_shares,
        'pinterest': post.pinterest_shares,
        'reddit': post.reddit_shares
    }
    
    for platform, count in platforms.items():
        for milestone in platform_milestones:
            if count >= milestone and not post.reached_milestones.filter(
                milestone=milestone, 
                type='platform',
                platform=platform
            ).exists():
                send_milestone_notification(post, milestone, platform)
                post.reached_milestones.create(
                    milestone=milestone,
                    type='platform',
                    platform=platform
                )

def update_share_statistics():
    """
    Update share statistics for all posts.
    This includes:
    - Recalculating total shares
    - Updating platform-specific share counts
    - Cleaning up duplicate shares from same IP within 24h
    - Checking for reached milestones
    """
    # Get current time for reference
    now = timezone.now()
    one_day_ago = now - timezone.timedelta(days=1)
    
    with transaction.atomic():
        # Clean up duplicate shares from same IP within 24h
        shares_to_delete = []
        for share in Share.objects.filter(created_date__gte=one_day_ago).order_by('created_date'):
            if share.ip_address:
                # Check for duplicate shares from same IP for same post and platform
                duplicates = Share.objects.filter(
                    post=share.post,
                    platform=share.platform,
                    ip_address=share.ip_address,
                    created_date__gte=share.created_date - timezone.timedelta(hours=24),
                    created_date__lt=share.created_date
                )
                if duplicates.exists():
                    shares_to_delete.append(share.id)
        
        # Delete duplicate shares
        if shares_to_delete:
            Share.objects.filter(id__in=shares_to_delete).delete()
        
        # Update share counts for all posts
        posts = Post.objects.all()
        for post in posts:
            # Get share counts by platform
            share_counts = Share.objects.filter(post=post).values('platform').annotate(
                count=Count('id')
            )
            
            # Create a dictionary of platform counts
            platform_counts = {
                'facebook_shares': 0,
                'twitter_shares': 0,
                'linkedin_shares': 0,
                'whatsapp_shares': 0,
                'pinterest_shares': 0,
                'reddit_shares': 0,
                'email_shares': 0
            }
            
            # Update platform counts
            total_shares = 0
            for share in share_counts:
                platform = share['platform']
                count = share['count']
                if platform in ['copy', 'qr']:
                    continue  # Skip copy and QR code shares in total count
                total_shares += count
                if f'{platform}_shares' in platform_counts:
                    platform_counts[f'{platform}_shares'] = count
            
            # Update post with new counts
            Post.objects.filter(id=post.id).update(
                total_shares=total_shares,
                **platform_counts
            )
            
            # Check for milestones
            check_share_milestones(post)

def clean_old_share_records():
    """
    Clean up share records older than 90 days while preserving statistical data.
    """
    ninety_days_ago = timezone.now() - timezone.timedelta(days=90)
    
    with transaction.atomic():
        # Get old shares grouped by post and platform
        old_shares = Share.objects.filter(
            created_date__lt=ninety_days_ago
        ).values('post_id', 'platform').annotate(
            share_count=Count('id')
        )
        
        # Create statistical records for old shares
        for share_stat in old_shares:
            post_id = share_stat['post_id']
            platform = share_stat['platform']
            count = share_stat['share_count']
            
            # Create a single statistical record
            Share.objects.create(
                post_id=post_id,
                platform=platform,
                created_date=ninety_days_ago,
                is_statistical=True,
                statistical_count=count
            )
        
        # Delete old individual share records
        Share.objects.filter(
            created_date__lt=ninety_days_ago,
            is_statistical=False
        ).delete()

def calculate_share_trends():
    """
    Calculate share trends and update post statistics.
    This includes:
    - Daily share growth rate
    - Weekly share growth rate
    - Most active sharing platforms
    """
    now = timezone.now()
    yesterday = now - timezone.timedelta(days=1)
    last_week = now - timezone.timedelta(days=7)
    
    with transaction.atomic():
        posts = Post.objects.all()
        for post in posts:
            # Calculate daily shares
            today_shares = Share.objects.filter(
                post=post,
                created_date__date=now.date()
            ).count()
            
            yesterday_shares = Share.objects.filter(
                post=post,
                created_date__date=yesterday.date()
            ).count()
            
            # Calculate weekly shares
            this_week_shares = Share.objects.filter(
                post=post,
                created_date__gte=last_week
            ).count()
            
            # Calculate platform distribution
            platform_shares = Share.objects.filter(
                post=post,
                created_date__gte=last_week
            ).values('platform').annotate(
                count=Count('id')
            ).order_by('-count')
            
            # Update post with trend data
            post.share_trends = {
                'daily_growth': (today_shares - yesterday_shares),
                'weekly_total': this_week_shares,
                'top_platforms': [
                    {'platform': p['platform'], 'count': p['count']}
                    for p in platform_shares[:3]  # Top 3 platforms
                ]
            }
            post.save(update_fields=['share_trends']) 