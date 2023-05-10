import setuptools

with open("README.md", "r") as f:
    long_description = f.read()

setuptools.setup(
    include_package_data=True,
    name="fyers_token_manager_v2",
    version="0.0.1",
    description="Fyers Token Manager",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/krunaldodiya/fyers_token_manager",
    author="Krunal Dodiya",
    author_email="kunal.dodiya1@gmail.com",
    packages=setuptools.find_packages(),
    install_requires=[
        "requests",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
)
