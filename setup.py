from setuptools import find_packages, setup

setup(
    name='changesetdb',
    version='0.0.1',
    packages=find_packages(),
    include_package_data=False,
    zip_safe=False,
    install_requires=[
        'Click',
        'psycopg2'
    ],
    entry_points='''
        [console_scripts]
        changesetdb=changesetdb:cli
    ''',
    test_suite='nose2.collector.collector',
    tests_require=['nose2']
)
