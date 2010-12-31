from setuptools import setup

setup(
    name="django-static",
    version="dev",
    description="Template application for Django and Buildout",
    author="Matthew J. MOrrison",
    author_email="mattj.morrison@gmail.com",
    package_dir={'':'example_project'},
    install_requires = (
        'south',
        'django-debug-toolbar',
    ),
)
