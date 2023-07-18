from setuptools import setup

setup(
    name='clean_folder',
    version='1.0',
    description='Simple file sorter',
    url='https://github.com/IronWoodcutter/homework_mod_7/tree/main',
    author='Oleksandr Vlasov',
    license='MIT',
    packages=['clean_folder'],
    entry_points={
        'console_scripts': [
            'clean-folder = clean_folder.clean:main'
        ]
    }
)