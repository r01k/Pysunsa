
"""Setup module for pysunsa."""
from pathlib import Path

from setuptools import find_packages, setup

PROJECT_DIR = Path(__file__).parent.resolve()
README_FILE = PROJECT_DIR / "README.md"
VERSION = "0.0.3"


setup(
    name="pysunsa",
    version=VERSION,
    url="https://github.com/r01k/Pysunsa",
    download_url="https://github.com/r01k/Pysunsa",
    author="r01k",
    author_email="rk01k@yahoo.com",
    description="Python wrapper for Sunsa smart blind wands REST API",
    long_description=README_FILE.read_text(encoding="utf-8"),
    long_description_content_type="text/markdown",
    packages=find_packages(exclude=["test.*", "test"]),
    python_requires=">=3.12",
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "Programming Language :: Python :: 3.12",
        "Topic :: Home Automation",
    ],
)
