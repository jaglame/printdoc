from setuptools import setup
setup(
    name = "printdoc",
    version = "0.0.1",
    packages = ["printdoc"],

    # Dependencias que se instalarán.
    install_requires = [
        "uwsgi",
        "requests"
    ]
)


