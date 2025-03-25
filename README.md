# Django Mini Blog

A feature-rich blog platform built with Django, implementing all required features and additional enhancements for a complete blogging experience.

## Features

### Core Requirements ✅
- User Authentication
  - Registration
  - Login/Logout
  - Password Reset
- Post Management (CRUD)
  - Create new posts
  - Read posts (list and detail views)
  - Update existing posts
  - Delete posts
- Database Integration
  - SQLite database
  - Models for posts, users, comments, etc.
- Templates & Styling
  - Bootstrap for responsive design
  - Clean and modern UI
- Admin Panel
  - Django admin interface
  - Content management

### Additional Features ✅
- Comments System
  - Add comments to posts
  - Nested comments
  - Comment moderation
- Categories and Tags
  - Organize posts by categories
  - Tag posts for better organization
- Like/Dislike System
  - Like/unlike posts
  - Like/unlike comments
- Image Uploads
  - Featured images for posts
  - Profile pictures
- Search Functionality
  - Search posts by title/content
  - Search results page
- User Profiles
  - Custom user profiles
  - Profile pictures
  - Bio information
- Pagination
  - Paginated post lists
  - Paginated search results

## Installation

1. Clone the repository:
```bash
git clone <your-repository-url>
cd django-mini-blog
```

2. Create and activate virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run migrations:
```bash
python manage.py migrate
```

5. Create superuser:
```bash
python manage.py createsuperuser
```

6. Run the development server:
```bash
python manage.py runserver
```

## Usage

1. Access the admin panel at `/admin`
2. Create categories and tags
3. Create blog posts
4. Customize user profiles
5. Interact with posts (comments, likes)

## Project Structure

```
django-mini-blog/
├── blog/                 # Main app
│   ├── models.py        # Database models
│   ├── views.py         # View logic
│   ├── urls.py          # URL patterns
│   └── forms.py         # Forms
├── templates/           # HTML templates
│   └── blog/
│       ├── base.html    # Base template
│       ├── post_list.html
│       ├── post_detail.html
│       └── ...
├── static/             # Static files
│   ├── css/
│   ├── js/
│   └── images/
└── manage.py
```

## Customization Details

1. Comments System
   - Implemented nested comments
   - Added comment moderation
   - Included comment likes

2. Categories and Tags
   - Created category management
   - Implemented tag system
   - Added category and tag detail pages

3. Like/Dislike System
   - Added post likes
   - Implemented comment likes
   - Created like/unlike functionality

4. Search Functionality
   - Implemented post search
   - Added search results page
   - Included pagination for results

## Challenges & Solutions

1. Nested Comments
   - Challenge: Implementing proper comment threading
   - Solution: Used recursive template rendering and proper model relationships

2. Like System
   - Challenge: Real-time like updates
   - Solution: Implemented AJAX calls for smooth user experience

3. Search Functionality
   - Challenge: Efficient search across multiple fields
   - Solution: Used Django's Q objects for complex queries

## Screenshots

[Add your screenshots here]

## License

This project is licensed under the MIT License. 