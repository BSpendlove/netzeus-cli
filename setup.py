from setuptools import setup, find_packages

with open("README.md", "r") as fs:
    long_description = fs.read()

setup(
    name="netzeus_cli",
    version="0.0.1",
    description="CLI Tool built by Network Engineers for Network Engineers",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "click==8.0.4",
        "click-plugins==1.1.1",
        "python-dotenv==0.19.2",
        "loguru==0.6.0",
        "requests==2.28.1",
        "pydantic==1.10.2",
    ],
    entry_points="""
        [console_scripts]
        netzeus-cli=netzeus_cli.cli:cli
    """,
)
