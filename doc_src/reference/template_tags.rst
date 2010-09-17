.. _templatetags:

Template Tags
=============

.. _templatetag_user_rating:

critic_user_rating
******************

Retrieves the user's rating for a specified object

**Syntax**

.. code-block:: django

	{% critic_user_rating [object] as [varname] %}
	
**Example**
	
.. code-block:: django

    {% critic_user_rating story as user_rating %}

	You have rated this story a {{ user_rating }}
	
.. _templatetag_render:
	
critic_render
*************

Renders some template for a specific object.

**Syntax**

.. code-block:: django

	{% critic_render [object] %}
	
**Example**

.. code-block:: django

    {% critic_render entry %}

.. _templatetag_render_url:

critic_render_url
*****************

When given a object, a url for rendering the rating method will be returned.
This is simply here for convenience.

**Syntax**

.. code-block:: django

	{% critic_render_url [object] %}
	
**Example**

.. code-block:: django

	{% critic_render_url [object] %}
	
**Output Example**

.. code-block:: html

	/critic/render/11/2/