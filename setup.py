from setuptools import setup

setup(name='go_translator',
      version='0.0.2',
      description='Machine Translation for Go',
      author='ICHIKAWA, Yuji',
      author_email='ichikawa.yuji@gmail.com',
      url='https://github.com/y-ich/go_translator',
      license='MIT',
      packages=['go_translator'],
      install_requires=[
        'requests',
        'pyquery',
        'mojimoji',
        'hanja',
        'pymongo',
        'dnspython'
      ],
      classifiers=[
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 2.7',
      ]
)
