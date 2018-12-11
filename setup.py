from setuptools import find_packages, setup

setup(name='nbplayer',
      version="0.0.1",
      description='A console notebook player',
      long_description="A console notebook player",
      author='Douglas S. Blank',
      author_email='doug.blank@gmail.com',
      url='https://github.com/Calysto/nbplayer',
      install_requires=["jupyter", "notebook"],
      packages=find_packages(include=['nbplayer']),
      include_data_files = True,
      classifiers=[
          'Framework :: IPython',
          'License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)',
          'Programming Language :: Python :: 3',
      ]
)
