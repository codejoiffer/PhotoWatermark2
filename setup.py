from setuptools import setup, find_packages
import os

# 获取项目根目录
here = os.path.abspath(os.path.dirname(__file__))

# 读取README.md作为项目描述
with open(os.path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

# 读取requirements.txt获取依赖列表
with open(os.path.join(here, 'requirements.txt'), encoding='utf-8') as f:
    requirements = f.read().splitlines()

setup(
    name='PhotoWatermark2',
    version='1.0.0',
    description='一款运行在MacOS上的图片水印工具',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='PhotoWatermark Team',
    author_email='support@photowatermark.com',
    url='https://github.com/photowatermark/PhotoWatermark2',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    include_package_data=True,
    install_requires=requirements,
    entry_points={
        'console_scripts': [
            'photowatermark=main:main',
        ],
    },
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: MacOS X :: Cocoa',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Topic :: Multimedia :: Graphics :: Editors',
    ],
    python_requires='>=3.7',
    keywords='watermark, image processing, photo editor, macos',
    project_urls={
        'Bug Reports': 'https://github.com/photowatermark/PhotoWatermark2/issues',
        'Source': 'https://github.com/photowatermark/PhotoWatermark2/',
    },
)