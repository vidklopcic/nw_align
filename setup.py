from setuptools import setup, find_packages, dist
import pip

pip.main(['install', 'pythran'])

from pythran import PythranExtension

setup(
    name='nw-align-probs',
    packages=find_packages('nw_align_probs'),
    package_dir={'': 'nw_align_probs'},
    version='0.4',
    license='MIT',
    description='Needleman-Wunsch alignment for text to logprobs frames from ASR models',
    author='Vid Klopcic',
    author_email='vid.klopcic@lgm.fri.uni-lj.si',
    url='https://github.com/vidklopcic/nw_align_probs',
    download_url='https://github.com/vidklopcic/nw_align_probs/archive/refs/tags/v_04.tar.gz',
    keywords=['Needleman-Wunsch', 'global alignment', 'ASR text alignment'],
    install_requires=[
        'numpy',
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Science/Research',
        'Topic :: Text Processing',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.8',
    ],
    ext_modules=[PythranExtension("nw_align_probs", ["nw_align_probs/nw_align_probs.py"])],
)
