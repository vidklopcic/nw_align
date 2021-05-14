import os
import sys
from distutils.core import setup
from setuptools.command.install import install


class PostInstallCommand(install):
    def run(self):
        install.run(self)
        print('compiling pythran module')

        def find_module_path():
            for p in sys.path:
                if os.path.isdir(p) and 'nw_align_probs' in os.listdir(p):
                    return os.path.join(p, 'nw_align_probs')

        import pythran
        install_path = os.path.join(find_module_path(), 'nw_align_probs.py')
        print('compiling pythran module:', install_path)
        pythran.compile_pythranfile(install_path)


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

    cmdclass={
        'install': PostInstallCommand,
    },
)
