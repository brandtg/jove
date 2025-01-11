from setuptools import setup, find_packages

setup(
    name="jove",
    version="0.0.1",
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
