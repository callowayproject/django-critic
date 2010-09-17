.. _settings:

Settings
========

.. contents::
   :depth: 2

Below is a list of all the settings variables.

.. _setting_rating_methods:

CRITIC_RATING_METHODS
*********************

This setting is a list of dictionaries that defines all the properties 
of your rating methods.

Example:

.. code-block:: python

	CRITIC_RATING_METHODS = (
		{'name': 'A Simple Up/Down Rating System',
		 'content_types': ['blog.entry'],
		 'options': [0, 1],
		 'allow_change': True
		},
	)
	
.. _setting_module_keys:

Module Keys
###########

* **name** - String, Optional, this is a generic name so you can identify the rating method.
* **content_types** - this is a list of the models you wish to have be ratable. 
	* Format expected is 'app.model'.
* **options** - This is a list of Integers of all the options a user can select.
* **allow_change** - True|False, Optional, will allow user to change their rating
	* If not specified :ref:`setting_allow_change` will be used.
* **template** - String, location of the template to use for the content_types.
	* If not specified :ref:`setting_default_template` will be used.

.. _setting_allow_change:

CRITIC_ALLOW_CHANGE
*******************

True|False, used as a default value to determine if a user can change 
their rating for a object.

.. _setting_default_template:

CRITIC_DEFAULT_RENDER_TEMPLATE
******************************

The location of the default template. Default location is 'critic/render.html'

.. _setting_rating_attribute:

CRITIC_RATING_ATTRIBUTE
***********************

The name of the attribute that will be added to the object for easy access 
to the ratings