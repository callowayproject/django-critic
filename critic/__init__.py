__version_info__ = {
    'major': 0,
    'minor': 2,
    'micro': 4,
    'releaselevel': 'final',
    'serial': 0
}

def get_version():
    vers = ["%(major)i.%(minor)i" % __version_info__, ]

    if __version_info__['micro']:
        vers.append(".%(micro)i" % __version_info__)
    if __version_info__['releaselevel'] != 'final':
        vers.append('%(releaselevel)s%(serial)i' % __version_info__)
    return ''.join(vers)

__version__ = get_version()

class AlreadyRegistered(Exception):
    """
    An attempt was made to register a model more than once.
    """
    pass


registry = []

def register(model, critic_descriptor_attr='ratings'):
    """
    Sets the given model class up for working with critic.
    """
    from critic.managers import RatingDescriptor

    if model in registry:
        raise AlreadyRegistered("The model '%s' has already been "
            "registered." % model._meta.object_name)
    if hasattr(model, critic_descriptor_attr):
        raise AttributeError("'%s' already has an attribute '%s'. You must "
            "provide a custom critic_descriptor_attr to register." % (
                model._meta.object_name,
                critic_descriptor_attr,
            )
        )

    # Add rating descriptor
    setattr(model, critic_descriptor_attr, RatingDescriptor())

    # Finally register the model
    registry.append(model)