from distutils.core import setup
import setuptools

setuptools.dist.Distribution(dict(setup_requires='pythran'))

from pythran.dist import PythranExtension, PythranBuildExt

setup(
    name='nw-align-probs',
    packages=['nw_align_probs'],
    version='0.3',
    license='MIT',
    description='Needleman-Wunsch alignment for text to logprobs frames from ASR models',
    author='Vid Klopcic',
    author_email='vid.klopcic@lgm.fri.uni-lj.si',
    url='https://github.com/vidklopcic/nw_align_probs',
    download_url='https://github.com/vidklopcic/nw_align_probs/archive/refs/tags/v_03.tar.gz',
    keywords=['Needleman-Wunsch', 'global alignment', 'ASR text alignment'],
    install_requires=[
        'pythran',
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
    cmdclass={"build_ext": PythranBuildExt}
)
