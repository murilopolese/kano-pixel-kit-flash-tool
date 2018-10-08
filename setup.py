from setuptools import setup

install_requires = ['esptool==2.5.0', 'PyQt5==5.11.2', 'pyserial==3.4',
                    'appdirs==1.4.3']

setup(
    name='rpkflashtool',
    version='0.1.1',
    description='A simple Flasher for Kano Pixel Kit.',
    long_description='Flash your Pixel Kit with MicroPython or Kano Code firmware.',
    author='Murilo Polese',
    author_email='murilo@kano.me',
    url='https://github.com/murilopolese/kano-pixel-kit-flash-tool',
    license='MIT',
    packages=['rpkflashtool'],
    install_requires=install_requires,
    include_package_data=True,
    zip_safe=False,
    classifiers=[

    ],
    entry_points={
        'console_scripts': [
            "rpkflashtool = rpkflashtool.app:run",
        ],
    },
    options={  # Briefcase packaging options for OSX
        'app': {
            'formal_name': 'rpkflashtool',
            'bundle': 'me.kano',
        }
    }
)
