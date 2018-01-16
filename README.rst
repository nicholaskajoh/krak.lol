Krak.lol
========
Krak.lol is a social site for comedy. It's built on the Django web framework.

Project dependencies
====================
This project will use the latest versions of its dependencies as soon as it has been tested with them.

* Django (Web dev framework)
* Pillow (Imaging library)
* BeautifulSoup4 (Screen-scraping)
* AnyMail (Email Backends)
* Django-Watson (Full-text Search)
* Django-Crontab (Scheduled Tasks)
* Django-Admin-View-Permission (Admin permissions)
* Django-REST-framework (API)

**NB: Some of these dependencies have their own dependencies.**

Run :code:`pip install -r requirements.txt` during initial setup.

Docs
====
The docs of each part of the project can be found in the READMEs of those parts.

Dev
===
The settings module contains local and production settings. In development, run: ::

  # UNIX Bash Shell
  export DJANGO_SETTINGS_MODULE=krak.settings.local

  # Windows Shell
  set DJANGO_SETTINGS_MODULE=krak.settings.local

DB
==
This project uses PostgreSQL in production. As such, it's important you use same in development to avoid unecessary issues. Install postgres on your local machine and use with the DB params in the local settings file.