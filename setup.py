from setuptools import setup, find_packages

setup(
    name="coffee-api",
    version="0.1.0a",
    url='http://github.com/hodgestar/coffee-api',
    license='BSD',
    description="Super-silly virtual coffee maker",
    long_description=open('README.rst', 'r').read(),
    author='Simon Cross',
    author_email='hodgestar@gmail.com',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'Flask==0.10.1',
        'Jinja2==2.7.2',
        'MarkupSafe==0.19',
        'Werkzeug==0.9.4',
        'argparse==1.2.1',
        'gunicorn==19.5.0',
        'itsdangerous==0.23',
        'wsgiref==0.1.2',
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: POSIX',
        'Programming Language :: Python',
    ],
)
