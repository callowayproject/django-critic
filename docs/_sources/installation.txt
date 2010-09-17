.. _installation:

Installation
============

Getting django-critic
*********************

You can get django-crtic in a couple ways:

1. Clone the git repository `from here <http://github.com/josesoa/django-critic>`_
2. Download the latest build `here <http://pypi.python.org/pypi/django-critic/0.2>`_
3. Use PIP to install from our opensource site pypi 
	* pip install django-critic


Installing
**********

Add critic do your INSTALLED_APPS setting.

.. code-block:: python

	INSTALLED_APPS = (
		...
		'critic',
		...
	)
	
Sync the database::

	$ ./manage.py syncdb

Add the urls

.. code-block:: python

	urlpatterns += patterns('',
		...
		(r'^critic/', include('critic.urls')),
		...
	)