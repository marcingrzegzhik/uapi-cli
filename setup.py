from setuptools import setup

setup(
    name="uapi-cli",
    version="1.0.0",
    py_modules=["uapi_cli"],
    install_requires=["usdk"],
    entry_points={
        "console_scripts": [
            "uapi = uapi_cli:main",
        ],
    },
)