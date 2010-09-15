.. _api:

API
===

.. contents::
   :depth: 2

.. _api_rating_manager:

Rating Manager
**************

.. _api_manager_add:

add
---

Arguments expected: 

* **obj** - the object instance
* **usr** - the authenticated user
* **opt** - the option value the user selected.

Returns:

* True or False, if the add was successful

.. _api_manager_change:

change
------

The :ref:`api_model_manager_add` already handles changes so this method 
is simply here for connivence and it calls the :ref:`api_model_manager_add` method.

Arguments expected:

* **obj** - the object instance
* **usr** - the authenticated user
* **opt** - the option value the user selected.

Returns:

* True or False, if the change was successful

.. _api_manager_user_rating:

user_rating
-----------

Returns the value the user selected for the supplied object

Arguments expected:

* **obj** - the object instance
* **usr** - the authenticated user

Returns:

* Integer - the value the supplied user selected.

.. _api_manager_average:

average
-------

Returns the average value for the supplied object.

Arguments expected:

* **obj** - the object instance

Returns:

* Number - the average for the supplied object.

.. _api_manager_total:

total
-----

Returns the total amout of ratings for the supplied object. Optionl argument 
'opt' can return the total ratings for a particular option.

Arguments expected:

* **obj** - the object instance
* **opt** - the option value *OPTIONAL*

Returns:

* Number - the total about of ratings for the supplied object/option

Rating Discriptor
*****************

A descriptor is added a the models that will be rate-able. The descriptor 
returns a manager and works the same as :ref:`api_rating_manager` but does not
require the object to be passed in.

add
---

Arguments expected: 

* **usr** - the authenticated user
* **opt** - the option value the user selected.

change
------

Arguments expected:

* **usr** - the authenticated user
* **opt** - the option value the user selected.

user_rating
-----------

* **usr** - the authenticated user

average (property)
------------------

This takes no arguments and returns the average for the instance

**Example**

::

	>>> obj.ratings.average
	>>> 3.5

total (property)
----------------

This takes no arguments and returns the total for the instance.

**Example**

::

	>>> obj.ratings.total
	>>> 213
	
data (property)
---------------

This returns detailed information about the rating options for an instance.

* **percentage** - the percentage of a option
* **total** - total amount of votes for a option

**Example**

::

	>>> p = Product.objects.get(pk=1)
	>>> p.ratings.data
	>>> {'1': {'percentage': 0, 'total': 0},
	 '2': {'percentage': 0, 'total': 0},
	 '3': {'percentage': 0, 'total': 0},
	 '4': {'percentage': 100, 'total': 1},
	 '5': {'percentage': 0, 'total': 0}}
	