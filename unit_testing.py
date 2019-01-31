# -*- coding: utf-8 -*-
"""
Created on Mon Jan 28 14:03:48 2019

@author: winkl
"""

import unittest
from business_phonebook_functions import *

#NB: must has "test" in function name
class testFunctions(unittest.TestCase):
    def test_if_no_connection_db(self):
        self.assertTrue(getdb())
        
    def test_check_returns_business_list(self):
        self.assertIsInstance(create_business_category_list(),list)
#checking returned list not empty, if empty will return False
        self.assertTrue(create_business_category_list())
        
    def test_getting_latlong_from_user(self):
        self.assertIsNotNone(getting_latlong_from_user())
#        self.assertFalse(getting_latlong_from_user())

#checking returned list not empty, if empty will return False    
#checking one time with valid input --> list is not empty
#checking one time with invalid input --> list is empty --> Test fails        
    def test_getting_latlong_from_business(self):
        self.assertTrue(getting_latlong_from_business('Home'), list)
        self.assertTrue(getting_latlong_from_business('Dog'), list)
    
        
if __name__ == "__main__":
    unittest.main()