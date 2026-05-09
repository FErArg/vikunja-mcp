from setuptools import setup, find_packages

setup(
    name="vikunja_mcp",
    version="0.0.5",
    description="MCP server for Vikunja project management API",
    packages=find_packages(),
    requires_python=">=3.11",
    install_requires=[
        "fastmcp>=0.1.0",
        "requests>=2.31.0",
        "python-dotenv>=1.0.0",
    ],
    extras_require={
        "dev": [
            "pytest>=8.0.0",
            "pytest-mock>=3.12.0",
        ],
    },
)
