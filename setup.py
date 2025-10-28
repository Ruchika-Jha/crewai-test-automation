from setuptools import setup, find_packages

setup(
    name="crewai-automation",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "crewai>=0.1.32",
        "langchain>=0.1.0",
        "langchain-openai>=0.0.2",
        "python-dotenv>=1.0.0",
        "azure-devops>=7.1.0b4",
        "jinja2>=3.1.2",
        "openai>=1.3.7"
    ],
)