Django Critic
=============

This is a settings based rating application.

Installation
------------

You can get django-crtic in a couple ways:

1. Clone the git repository `from here <http://github.com/josesoa/django-critic>`_
2. Download the latest build `here <http://pypi.python.org/pypi/django-critic/0.2>`_
3. Use PIP to install 
	* pip install django-critic


**Add critic do your INSTALLED_APPS setting.**

::

	INSTALLED_APPS = (
		...
		'critic',
		...
	)
	
**Sync the database**

::

	$ ./manage.py syncdb

**Add the urls**

::

	urlpatterns += patterns('',
		...
		(r'^critic/', include('critic.urls')),
		...
	)

Basic settings
--------------

The main setting you will use is `CRITIC_RATING_METHODS`. This is a 
tuple of dictionaries that tells critic what models will be 
ratable and some extra arguments about the rating method.

Here is a basic example

::

	CRITIC_RATING_METHODS = (
		{'name': 'A Simple Up/Down Rating System',
		 'content_types': ['blog.entry'],
		 'options': [1, 2],
		 'allow_change': True,
		 'template': 'mypath/entry_critic.html'
		},
	)
	
This sets up blog.entry to be rated upon in a Up/Down fashion. You can 
specify multiple content types for a rating method, but you cannot specify 
the same content type for multiple rating methods.

These 3 keys, 'name', 'content_types' and 'options' are the only required 
keys for django-critic to function. 'allow_change' and 'template' are optional, 
and if neither of these are not specified `CRITIC_ALLOW_CHANGE` or 
`CRITIC_DEFAULT_TEMPLATE` will be used respectfully.

See more information about this setting: `CRITIC_RATING_METHODS`

A rating descriptor is also added to the models specified, by default the 
name of the attribute is 'ratings'. The name can be changed using the 
`CRITIC_RATING_ATTRIBUTE`.

Templates
---------

The template that is render is something you will need to create, the 
default template is blank.

The template that is retrieved follows this process:

#. Check for existance of a template that is specified in `CRITIC_RATING_METHODS` for a particular object.
#. Check for existance of critic/<app>__<model>.html for a particular object.
#. Use critic/render.html if all else fails. 

Since you will know what your rating method does, the template can be 
custom made to your needs.

For example: If we wanted to create a template for the rating method we 
specified above, you know there is going to be 2 options and therefore 
we can have a select box with 2 options, one for up one for down. We also 
know that you can change your rating so there is no need to check if you  
have already rated. Your template could look something like this...

::

	<form action="{% url critic_add_rating %}" method="POST">
		<select name="option" id="option">
			<option value="1" {% ifequal user_rating 1 %}selected=True{% endifequal %}>Up</option>
			<option value="2" {% ifequal user_rating 2 %}selected=True{% endifequal %}>Down</option>
		</select>
		<input type="hidden" name="content_type_id" value="{{ content_type_id }}">
		<input type="hidden" name="object_id" value="{{ obj.pk }}">
		<input type="submit" name="submit" value="GO">
	</form>
	Average: {{ average }}<br/>
	Total: {{ total }}
	
Template context
****************

Which ever template gets rendered, you will have the following variables 
available in the context:

* **user_rating** - the rating the user has selected.
* **content_type_id** - the content type id of the object
* **obj** - the object
* **method** - the 'critic.modules.Method' instance for the object
* **average** - average rating for the object
* **total** - the total ratings for the object

Render the template
*******************

You can use the template tag `critic_render` to render the template.

::

	{% load critic_tags %}
	
	{% critic_render obj %}

Retrieve rating data via urls
-----------------------------

You can also retrieve the user rating and rating data for an object via a url. 
The output is in JSON format.

* user_rating/**<content_type_id>**/**<object_id>**/
	* Example Output: {"user_rating": 1}
* data/**<content_type_id>**/**<object_id>**/**<option>**/
	* Example Output: {"average": 3.0, "total": 1, "average_rounded": 3}
* data/**<content_type_id>**/**<object_id>**/
	* Example Output: {"average": 3.0, "total": 1, "average_rounded": 3}
	
Render via url
**************

This will render your template the same way `critic_render` does

* render/**<content_type_id>**/**<object_id>**/

**Example**

Using JQuery to load the rating template via ajax

::

	$(document).ready(function(){
		$.ajax({
			url:'{% critic_render_url obj2 %}',
			success: function(data){
				$('#box').html(data);
			}
		});
	});


**NOTE**

	The template tag `CRITIC_RENDER_URL` will retrieve the url 
	needed to render the object specified

Add ratings
-----------

The `add` view expects the following in the request.POST. Is also expects 
a logged in user.

* content_type_id
* object_id
* option

You can reverse the add url for form posting.

::

	{% url critic_add_rating %}
	/critic/add/
	
