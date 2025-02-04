from setuptools import setup

setup(
    name="CliTool_TextToBash",
    version="1.1",
    py_modules=["cli_tool"],
    install_requires=[
        "google-generativeai",
    ],
    entry_points={
        "console_scripts": [
            "texttobash=cli_tool:main",
        ]
    },
    python_requires=">=3.6",
)
