from setuptools import find_packages, setup

package_name = 'my_farobot_controller_screen'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='akos',
    maintainer_email='ajanvari@gmail.com',
    description='Farobot controller GUI',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'farobot_controller = my_farobot_controller_screen.my_controller_gui:main',
        ],
    },
)
