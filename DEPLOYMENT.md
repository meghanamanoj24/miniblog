# Deployment Guide

This guide will help you deploy the Travel Blog to a production environment.

## Prerequisites

1. A server running Ubuntu 20.04 or later
2. Domain name pointing to your server
3. PostgreSQL database
4. Redis server
5. Nginx web server
6. SSL certificate (Let's Encrypt recommended)

## Server Setup

1. Update system packages:
```bash
sudo apt update
sudo apt upgrade
```

2. Install required packages:
```bash
sudo apt install python3-pip python3-venv postgresql nginx redis-server
```

3. Create a PostgreSQL database:
```bash
sudo -u postgres psql
CREATE DATABASE travelblog;
CREATE USER travelblog_user WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE travelblog TO travelblog_user;
\q
```

## Project Setup

1. Clone the repository:
```bash
git clone https://github.com/yourusername/travel-blog.git
cd travel-blog
```

2. Create and activate virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
pip install gunicorn psycopg2-binary redis
```

4. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your production values
```

5. Collect static files:
```bash
python manage.py collectstatic --no-input
```

6. Run migrations:
```bash
python manage.py migrate
```

## Gunicorn Setup

1. Create a systemd service file:
```bash
sudo nano /etc/systemd/system/travelblog.service
```

2. Add the following content:
```ini
[Unit]
Description=Travel Blog Gunicorn Daemon
After=network.target

[Service]
User=ubuntu
Group=www-data
WorkingDirectory=/path/to/travel-blog
ExecStart=/path/to/travel-blog/venv/bin/gunicorn \
    --workers 3 \
    --bind unix:/path/to/travel-blog/travelblog.sock \
    travelblog.wsgi:application

[Install]
WantedBy=multi-user.target
```

3. Start and enable the service:
```bash
sudo systemctl start travelblog
sudo systemctl enable travelblog
```

## Nginx Setup

1. Create Nginx configuration:
```bash
sudo nano /etc/nginx/sites-available/travelblog
```

2. Add the following content:
```nginx
server {
    listen 80;
    server_name yourdomain.com www.yourdomain.com;

    location = /favicon.ico { access_log off; log_not_found off; }
    
    location /static/ {
        root /path/to/travel-blog;
    }
    
    location /media/ {
        root /path/to/travel-blog;
    }
    
    location / {
        include proxy_params;
        proxy_pass http://unix:/path/to/travel-blog/travelblog.sock;
    }
}
```

3. Enable the site:
```bash
sudo ln -s /etc/nginx/sites-available/travelblog /etc/nginx/sites-enabled
sudo nginx -t
sudo systemctl restart nginx
```

## SSL Certificate Setup

1. Install Certbot:
```bash
sudo apt install certbot python3-certbot-nginx
```

2. Obtain SSL certificate:
```bash
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com
```

## Maintenance

1. Update application:
```bash
git pull
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --no-input
sudo systemctl restart travelblog
```

2. Monitor logs:
```bash
sudo tail -f /path/to/travel-blog/logs/error.log
```

3. Backup database:
```bash
pg_dump -U travelblog_user travelblog > backup.sql
```

## Security Checklist

- [ ] Debug mode is disabled
- [ ] Secret key is properly set
- [ ] Database credentials are secure
- [ ] SSL is properly configured
- [ ] File permissions are correct
- [ ] Firewall is configured
- [ ] Regular backups are scheduled
- [ ] Logging is properly configured
- [ ] Error pages are customized 