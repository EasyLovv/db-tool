from setuptools import setup
import pathlib

here = pathlib.Path(__file__).parent

install_requires = [
    'click==7.0',
    'tqdm==4.40.2',
    'sqlalchemy==1.3.11',
    'psycopg2==2.8.4',
    'python-dateutil==2.8.1'
]

dev_requires = [
    'pre-commit==1.20.0'
]

setup(
    name="db_tools",
    version="0.1",
    packages=["db_tools"],
    url="",
    install_requires=install_requires,
    author="Taras Protsenko",
    author_email="easylovv@gmail.com",
    maintainer="Taras Protsenko",
    maintainer_email="easylovv@gmail.com",
    description="The tools for rule the db.",
    entry_points={"console_scripts": ["dbtool=db_tools.__main__:main"]},
    include_package_data=True,
    extras_require={"dev": dev_requires},
    long_description=(here / "README.md").read_text("utf-8").strip(),
    long_description_content_type="text/markdown",
)
