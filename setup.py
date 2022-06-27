from setuptools import setup, find_packages
import os


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(name='scratch-python',
      version='0.1.3-alpha',
      description='A framework for creating Scratch blocks and projects with Python.',
      long_description_content_type="text/markdown",
      long_description=open('README.md').read(),
      author='Ethan Porcaro',
      author_email='ethan@ethanporcaro.com',
      license='MIT',
      url='https://github.com/IfanSnek/PyScratch',
      packages=find_packages(),
      package_data={'pyscratch': ['block_name_mapping.csv', 'scratchtext.ebnf']},
      include_package_data=True,
      entry_points={
          'console_scripts': ['scratchtext=pyscratch.main:cli'],
            },
      install_requires=['lark~=1.1.2']
      )
