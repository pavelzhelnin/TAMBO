import setuptools

try:
    from pyfiglet import Figlet
    f = Figlet(font='speed')
    long_message = f.renderText('TAMBO')
except:
    long_message = 'TAMBO'

version = "0.0.1"

setuptools.setup(
    name="TAMBO", 
    version=version,
    author="Zhelnin, P. et al.",
    author_email="pzhelnin@g.harvard.edu",
    description="Simulation for the TAMBO experiment",
    long_description=long_message,
    #long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    install_requires=['numpy>=1.16.6',
                      'scipy>=1.2.3',
                      ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
    python_requires='>=3.1',
    package_data={"tambo.resources."         : ["*.txt"],
                  }    
)