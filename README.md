sudo apt-get install mysql-server nginx python-pip python-dev build-essential git apache2 python-mysqldb

$ sudo pip install --upgrade pip 

### Install Django
Some dependencies only work with Django 1.4, so that is what we use for now. Download from https:/.djangoproject.com/download/1.4.5/tarball

    tar xzvf Django-1.4.5.tar.gz
    cd Django-1.4.5
    sudo python setup.py install

### Install django-mptt
    git clone git://github.com/django-mptt/django-mptt.git django-mptt
    cd django-mptt
    sudo python setup.py install

### Install FeinCMS
    sudo pip install feincms

### Install Grappelli
    sudo pip install django-grappelli


### Install Tastypie
    sudo apt-get install python-dateutil python-mimeparse
    git clone https://github.com/toastdriven/django-tastypie.git
    cd django-tastypie
    sudo python setup.py install

### Symlinks
    sudo ln -s /usr/local/lib/python2.7/dist-packages/django_tastypie-0.9.13_beta-py2.7.egg/tastypie/ /srv/alpheus/tastypie

### Symlinks for production
    sudo ln -s /usr/local/lib/python2.7/dist-packages/django/contrib/admin/static/admin/ /srv/alpheus/static/admin
    sudo ln -s /usr/local/lib/python2.7/dist-packages/django/contrib/admin/templates/admin/ /srv/alpheus/templates/admin
    sudo ln -s /usr/local/lib/python2.7/dist-packages/feincms/static/feincms/ /srv/alpheus/static/feincms
    sudo ln -s /usr/local/lib/python2.7/dist-packages/feincms/templates/admin/feincms/ /srv/alpheus/templates/admin/feincms
    sudo ln -s /usr/local/lib/python2.7/dist-packages/grappelli/static/grappelli/ /srv/alpheus/static/grappelli
