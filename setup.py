import os
from setuptools import setup, find_packages


def get_version():
    try:
        return open(os.path.join('www', 'version.txt')).read().strip()
    except OSError:
        return 'n/a'


setup( name='gittip'
     , version=get_version()
     , packages=find_packages()
     , entry_points = { 'console_scripts'
                      : [ 'gittip=gittip.cli:gittip'
                        , 'payday=gittip.cli:payday'
                        , 'swaddle=gittip.swaddle:main'
                        , 'fake_data=gittip.fake_data:main'
                         ]
                       }
      )
