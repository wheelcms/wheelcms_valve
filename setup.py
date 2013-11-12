from setuptools import setup, find_packages
import os

version = '0.9'

setup(name='wheelcms_valve',
      version=version,
      description="A blogging application for WheelCMS",
      long_description=open("README.txt").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      classifiers=[
        "Programming Language :: Python",
        ],
      keywords='',
      author='Ivo van der Wijk',
      author_email='wheelcms@in.m3r.nl',
      url='http://github.com/wheelcms/wheelcms_valve',
      license='BSD',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=[],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          'pytest',
          'wheelcms_axle',
          'wheelcms_categories',
          'wheelcms_rss'
      ],
      entry_points={
      },

      )

