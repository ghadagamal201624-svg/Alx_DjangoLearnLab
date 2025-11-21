libraryproject
# تكوين Nginx لفرض HTTPS

# 1. HTTP Redirect Block (يستمع إلى المنفذ 80 ويوجه إلى HTTPS)
server {
    listen 80;
    server_name example.com www.example.com; # استبدل بالنطاق الخاص بك

    # توجيه دائم إلى HTTPS
    return 301 https://$host$request_uri;
}

# 2. HTTPS Block (يستمع إلى المنفذ 443 ويوفر الشهادات)
server {
    listen 443 ssl;
    server_name example.com www.example.com;

    # مسار الشهادات
    ssl_certificate /path/to/your/certificate.crt; 
    ssl_certificate_key /path/to/your/private.key;

    # تشغيل تطبيق Django (عادةً عبر Gunicorn أو uWSGI)
    location / {
        include proxy_params;
        proxy_pass http://127.0.0.1:8000; # المنفذ الداخلي لتطبيق Django
    }
}