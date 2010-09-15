.. _getting_started:

Getting Started
===============

If you haven't installed django-critic yet please visit the 
:ref:`installation` page to do so.


Basic settings
##############

The main setting you will use is :ref:`setting_rating_methods`. This is a 
tuple of dictionaries that tells django-critic what models will be 
ratable and some extra arguments about the rating method.

Here is a basic example

.. code-block:: python

	CRITIC_RATING_METHODS = (
		{'name': 'A Simple Up/Down Rating System',
		 'content_types': ['blog.entry'],
		 'options': [1, 2],
		 'allow_change': False,
		},
	)
	
This sets up blog.entry to be rated upon in a Up/Down fashion. You can 
specify multiple content types for a rating method, but you cannot specify 
the same content type for multiple rating methods.

**Bad**

.. code-block:: python

	CRITIC_RATING_METHODS = (
		{'name': 'A Simple Up/Down Rating System',
		 'content_types': ['blog.entry', 'stories.story'],
		 'options': [1, 2],
		 'allow_change': False,
		},
		{'name': '5 Star Rating System',
		 'content_types': ['blog.entry'],
		 'options': [1, 2, 3, 4 ,5],
		 'allow_change': False,
		},
	)


These 3 keys, 'name', 'content_types' and 'options' are the only required 
keys for django-critic to function. 'allow_change' is optional, 
and if it is not specified :ref:`setting_allow_change` will be used.

See more information about this setting: :ref:`setting_rating_methods`

A rating descriptor is also added to the models specified, by default the 
name of the attribute is 'ratings'. The name can be changed using the 
:ref:`setting_rating_attribute`.

Adding ratings
##############

You can add ratings by using the model manager or the rating descriptor.

Here is an example of using the RatingManager

.. code-block:: python

	RatingData.objects.add(obj, usr, opt)
	
`add` will return True|False if the rating was added successfully.

Here is an example of using the descriptor. 

.. code-block:: python

	from blog.models import Entry
	
	e = Entry.objects.get(pk=1)
	e.ratings.add(usr, opt)
	
You can also use the change method to modify a users rating. View the 
:ref:`api` page for more details.
	


Displaying
##########

Now you can simply use the :ref:`templatetag_render` template tag.

.. code-block:: django

	{% critic_render entry %}
	
Template
********

The template that is render is something you will need to create, the 
default template is blank.

Since you will know what your rating method does, the template can be 
custom made to your needs.

For example: If we wanted to create a template for the rating method we 
specified above, you know there is going to be 2 options and therefore 
we can have a select box with 2 options, one for up one for down. So your 
template could look something like this...

.. code-block:: django

	<form id="{{ instance.pk }}" action="/critic/add/" method="get" accept-charset="utf-8">
		<select name="option" id="option">
			<option value="1" {% ifequal user_rating 1 %}selected=True{% endifequal %}>Up</option>
			<option value="2" {% ifequal user_rating 2 %}selected=True{% endifequal %}>Down</option>
		</select>
		<input type="hidden" name="content_type_id" value="{{ content_type_id }}">
		<input type="hidden" name="object_id" value="{{ instance.pk }}">
		<input type="submit" name="submit" value="GO">
	</form>
	{% if user_rating %}
		Average: {{ average }}<br/>
		Total: {{ total }}
	{% endif %}
	
.. note::

	The render method will give you, "instance", "content_type_id", "method"
	and "user_rating" in the context.
	
	When adding a rating, the view will expect 'option', 'content_type_id' and 'object_id' from
	either POST or GET.

