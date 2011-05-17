from setuptools import setup

setup(
    name="django-media-masher",
    version="dev",
    description="Compile JavaScript and CSS into single minified files",
    author="Matthew J. Morrison",
    author_email="mattj.morrison@gmail.com",
    include_package_data=True,
    package_dir={'':'src'},
    packages=('masher', 'masher.templatetags'),
    install_requires = (
        'south',
        'django-debug-toolbar',
        'mock',
        'unittest-xml-reporting',
        'coverage',
        'pylint',
        'nose',
        'django-nose',
    ),
)
