import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="python-pixel-control", # Replace with your own username
    version="1.0.0",
    author="John Wickham",
    author_email="john@wjwickham.com",
    description="Script for controlling connected WS2812B addressable LEDs.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/JohnWickham/python-pixel-control",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)