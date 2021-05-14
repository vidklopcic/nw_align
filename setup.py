import atexit
import os
from distutils.core import setup
from setuptools.command.install import install


class PostInstallCommand(install):
    def run(self):
        def _post_install():
            print('compiling pythran module')
            import pythran
            import nw_align_probs
            install_path = os.path.join(os.path.dirname(nw_align_probs.__file__))
            os.chdir(install_path)
            pythran.compile_pythranfile('nw_align_probs.py')

        atexit.register(_post_install)
        install.run(self)


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
