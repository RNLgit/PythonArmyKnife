from setuptools import setup
from platform import system

required_packages = ['numpy', 'matplotlib', 'pandas', 'opencv-python']

if system() == 'Darwin':
    required_packages += []
elif system() == 'Windows':
    required_packages += ['pythonnet']
elif system() == 'Linux' or 'Linux' in system():
    required_packages += []


setup(
    name="PythonArmyKnife",
    version="0.0.1",
    description='A light weight Python utility tool work like an army knife',
    long_description=open('README.md').read(),
    classifiers=[],
    install_requires=required_packages,
    setup_requires=[],
    scripts=[],
    python_requires='>=3.6',
    entry_points={
    },
    zip_safe=False,
    include_package_data=True
)
