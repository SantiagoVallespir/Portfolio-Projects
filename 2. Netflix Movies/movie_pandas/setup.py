from setuptools import setup, find_packages

setup(
      author = "Santiago Vallespir",
      description = "A package for populating DataFrames with movies data",
      name = "movie_pandas",
      version = "0.1.0",
      packages = find_packages(include = ["movie_pandas", "movie_pandas.*"]),
      install_requires = ["pandas", 
                          "requests", 
                          "numpy", 
                          "urllib", 
                          "scrapy", 
                          "requests_htlm",
                          "datetime"
                          ],
      python_requires = ">=3.0"
)