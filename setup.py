from setuptools import setup

setup(name='toxic',
      version='0.0',
      description='Package for analyzing toxic comments',
      url='https://github.com/mlmasters/toxic-comments',
      author='Matthew Chatham',
      author_email='matthew.a.chatham@gmail.com',
      license='MIT',
      packages=['toxic', 'toxic/common'],
      zip_safe=False)