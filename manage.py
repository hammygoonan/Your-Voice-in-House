import unittest
import os
import coverage
from data import base, federal, qld
from flask.ext.script import Manager
from yvih import app, db, models

manager = Manager(app)

@manager.command
def test():
    """Runs the unit tests without coverage."""
    tests = unittest.TestLoader().discover('tests', pattern='*.py')
    unittest.TextTestRunner(verbosity=2).run(tests)

@manager.command
def cov():
    """Runs the unit tests with coverage."""
    cov = coverage.coverage(
        branch=True,
        include='yvih/*'
    )
    cov.start()
    tests = unittest.TestLoader().discover('tests', pattern='*.py')
    unittest.TextTestRunner(verbosity=2).run(tests)
    cov.stop()
    cov.save()
    print 'Coverage Summary:'
    cov.report()
    basedir = os.path.abspath(os.path.dirname(__file__))
    covdir = os.path.join(basedir, 'coverage')
    cov.html_report(directory=covdir)
    cov.erase()

@manager.command
def data():
    '''Run data updates'''
    data = federal.FederalData()
    data.senateCsvs()
    # data.horCsvs()
    # data = qld.QldData()
    # data.memberPage('https://www.parliament.qld.gov.au/members/current/list/MemberDetails?ID=890183913')
if __name__ == '__main__':
    manager.run()
