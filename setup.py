from setuptools import setup, find_packages

setup(
    name="netzeus_cli",
    version="0.0.1",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "click==8.0.4",
        "click-plugins==1.1.1",
        "python-dotenv==0.19.2",
        "loguru==0.6.0",
        "requests==2.28.1",
    ],
    entry_points="""
        [console_scripts]
        netzeus-cli=netzeus_cli.cli:cli
    """,
)