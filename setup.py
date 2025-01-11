from setuptools import setup, find_packages

with open("README.md") as f:
    long_description = f.read()

setup(
    name="jove",
    version="0.0.2",
    author="Greg Brandt",
    author_email="brandt.greg@protonmail.com",
    description="A terminal-focused alternative to Jupyter notebooks.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/brandtg/jove",
    packages=find_packages(),
    install_requires=[
        # TODO Anything?
    ],
    extras_require={
        "dev": [
            "pytest==8.3.3",
            "black==24.8.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "jove = jove.workspace:main",
        ]
    },
    test_suite="tests",
    include_package_data=True,
)
