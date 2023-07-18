from setuptools import setup

setup(
    name='clean_folder',
    version='1.0',
    description='Simple file sorter',
    url='http://github.com/dummy_user/useful',
    author='Oleksandr Vlasov',
    license='MIT',
    packages=['clean_folder'],
    entry_points={
        'console_scripts': [
            'clean-folder = clean_folder.clean:main'
        ]
    }
)