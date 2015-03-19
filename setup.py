from setuptools import setup, find_packages
setup(
    name="loaddata_incremental",
    packages=find_packages(),
    version='0.1',
    description="Load your django fixtures incrementally",
    license="MIT",
    author="Christopher Schäpers",
    author_email="christopher@schaepers.it",
    url="https://github.com/Kondou-ger/django-loaddata-incremental",
    download_url="https://github.com/Kondou-ger/django-loaddata-incremental/tarball/0.1",
    install_requires=[
        'django>=1.6',
    ],
    keywords=["django", "fixtures"],
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ],
)
