from setuptools import setup

setup(
    name="CliTool_TextToBash",
    version="1.1",
    py_modules=["CliTool_TextToBash"],
    entry_points={
        "console_scripts": [
            "CliTool_TextToBash=CliTool_TextToBash:main",
        ]
    },
)
