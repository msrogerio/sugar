from lib2to3.pgen2 import driver
from config import setUpFirefox


class Driver():
    driver = None
    def newInstanceDriver(self):
        self.driver = setUpFirefox()

driver = Driver()