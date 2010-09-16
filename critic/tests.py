"""
django-critic: tests
"""

from django.test import TestCase
from django.db import models
from django.contrib.auth.models import User
from critic.models import RatingData

class TestSample(models.Model):
    name = models.TextField()
    something = models.IntegerField(default=1)
    
    def __unicode__(self):
        return self.name
        
class TestProduct(models.Model):
    name = models.CharField(max_length=20)
    desc = models.TextField()
    
    def __unicode__(self):
        return self.name

from critic.modules import METHODS, Method

# Setup up the methods.
METHODS['critic.testsample'] = Method(
    name="Up/Down", options=[1,2], change=True)
    
METHODS['critic.testproduct'] = Method(
    name="5 Star", options=[1,2,3,4,5], change=False)

class CriticTestCase(TestCase):
    """
    The main tests for django-critic.
    """
    fixtures = ['test_data.json']
    def setUp(self):
        """
        Set up some initial data.
        """
        self.sample = TestSample.objects.create(name="Testing")
        self.product = TestProduct.objects.create(name="My Product")
        self.bob = User.objects.get(pk=1)
        self.jim = User.objects.get(pk=2)
        self.jane = User.objects.get(pk=3)

    def test_add_rating(self):
        """
        This test will ensure adding a rating works.
        """
        # This will test to make sure adding a rating works.
        self.assertTrue(RatingData.objects.add(self.sample, self.bob, 1))
        
        # This will test changing a user's rating
        self.assertTrue(RatingData.objects.add(self.sample, self.bob, 2))
        
        # This should not allow a option that is not a valid choice.
        self.assertFalse(RatingData.objects.add(self.sample, self.bob, 3))
        
        # This should be false if no user is supplied.
        self.assertFalse(RatingData.objects.add(self.sample, None, 1))
        
    def test_change_rating(self):
        """
        This test will ensure changing a rating works.
        """
        RatingData.objects.add(self.sample, self.bob, 0)
        
        # The method assigned to sample content type allows changes.
        self.assertTrue(RatingData.objects.add(self.sample, self.bob, 1))
        
        # The first time we add a rating to product, everything should be ok.
        self.assertTrue(RatingData.objects.add(self.product, self.bob, 1))
        
        # The method assigned to product content type does not allow changes.
        self.assertFalse(RatingData.objects.add(self.product, self.bob, 2))
        
    def test_user_rating(self):
        """
        This will test retrieving the user rating
        """
        RatingData.objects.add(self.sample, self.bob, 1)
        
        self.assertEqual(RatingData.objects.user_rating(self.sample, 
            self.bob), 1)
        
        self.assertNotEqual(RatingData.objects.user_rating(self.sample, 
            self.bob), 0)
            
    def test_average(self):
        """
        This will test the rating average
        """
        RatingData.objects.add(self.product, self.bob, 3)
        RatingData.objects.add(self.product, self.jim, 2)
        RatingData.objects.add(self.product, self.jane, 1)
        
        # The average for the product should be 2
        self.assertEqual(RatingData.objects.average(self.product), 2)
        
    def test_total(self):
        """
        This will test the rating total
        """
        RatingData.objects.add(self.product, self.bob, 3)
        RatingData.objects.add(self.product, self.jim, 2)
        RatingData.objects.add(self.product, self.jane, 1)
        
        # The total should be 3
        self.assertEqual(RatingData.objects.total(self.product), 3)
        
        # The total for each option should be 1
        self.assertEqual(RatingData.objects.total(self.product, 3), 1)
        self.assertEqual(RatingData.objects.total(self.product, 2), 1)
        self.assertEqual(RatingData.objects.total(self.product, 1), 1)
