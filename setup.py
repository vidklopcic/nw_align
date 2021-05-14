import atexit
import os
import sys
from distutils.core import setup
from setuptools.command.install import install


class PostInstallCommand(install):
    def run(self):
        def _post_install():
            def find_module_path():
                for p in sys.path:
                    if os.path.isdir(p) and 'nw_align_probs' in os.listdir(p):
                        return os.path.join(p, 'nw_align_probs')

            install_path = find_module_path()
            print('compiling pythran module:', install_path)
            import pythran
            pythran.compile_pythranfile(os.path.join(install_path, 'nw_align_probs.py'))

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
