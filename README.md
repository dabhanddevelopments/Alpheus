### Dependencies
	sudo apt-get install mysql-server nginx python-pip python-dev build-essential git apache2 python-mysqldb
	sudo pip install --upgrade pip 

	pip install django-mptt django-tastypie django-grappelli feincms django-tastypie-swagger django-compressor django-extensions mimeparse Werkzeug numpy pandas django==1.5.1


### Symlinks
    sudo ln -s /usr/local/lib/python2.7/dist-packages/django_tastypie-0.9.13_beta-py2.7.egg/tastypie/ /srv/alpheus/tastypie

### Symlinks for production
    sudo ln -s /usr/local/lib/python2.7/dist-packages/django/contrib/admin/static/admin/ /srv/alpheus/static/admin
    sudo ln -s /usr/local/lib/python2.7/dist-packages/django/contrib/admin/templates/admin/ /srv/alpheus/templates/admin
    sudo ln -s /usr/local/lib/python2.7/dist-packages/feincms/static/feincms/ /srv/alpheus/static/feincms
    sudo ln -s /usr/local/lib/python2.7/dist-packages/feincms/templates/admin/feincms/ /srv/alpheus/templates/admin/feincms
    sudo ln -s /usr/local/lib/python2.7/dist-packages/grappelli/static/grappelli/ /srv/alpheus/static/grappelli
