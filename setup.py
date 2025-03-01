from setuptools import setup, find_packages

# Read dependencies from requirements.txt
def get_requirements_from_file():
    with open("requirements.txt") as f_in:
        return f_in.read().splitlines()

setup(
    # Package metadata
    name="beamng_gym",  # Package name (used in pip install)
    version="0.1.0",    # Version
    description="Custom Gymnasium environment for BeamNG simulation",
    python_requires=">=3.7",

    # Package structure
    packages=find_packages(),  # Detect and include all Python packages
    
    # Dependencies
    install_requires=get_requirements_from_file(),  # Install required libraries

    # Include additional files
    include_package_data=True,
    package_data={
        "beamng_gym": ["config/*.json5"]  # Include JSON5 config files
    },
)
