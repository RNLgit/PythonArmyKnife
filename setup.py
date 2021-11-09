from setuptools import setup

setup(
    name="PythonArmyKnife",
    version="0.0.1",
    description='A light weight Python utility tool work like an army knife',
    long_description=open('README.md').read(),
    classifiers=[],
    install_requires=['numpy', 'matplotlib', 'pandas', 'opencv-python', 'pillow'],
    setup_requires=[],
    scripts=[],
    python_requires='>=3.6',
    entry_points={
    },
    zip_safe=False,
    include_package_data=True
)
