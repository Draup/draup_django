import setuptools

import draup_django

with open("README.md", "r") as fh:
    long_description = fh.read()

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setuptools.setup(
    name="draup_django",
    version="1.4.0",
    author="Arpit | Teja | Kashish",
    author_email="arpit@zinnov.com",
    description=" Django Utility - Draup Labs",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Draup-Zinnov/draup_django",
    license="MIT",
    packages=setuptools.find_packages(),
    package_dir={'draup_django': 'draup_django'},
    include_package_data=True,
    install_requires=requirements,
    python_requires='>=3.0.*',
    classifiers=[
        "Framework :: Django",
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    zip_safe=False,
    keywords="django normalisation",
)