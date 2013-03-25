# Moving Data

## Required tools

### AWS toolkit
To set up the Amazon AWS toolkit, follow the official guide: [http://aws.amazon.com/developertools/351](http://aws.amazon.com/developertools/351) and configure the toolkit with your AWS account credentials.

### PlanetLab
In order to set up the PlanetLab toolkit, follow the official getting started guide: [https://www.planet-lab.org/doc/guides/user](https://www.planet-lab.org/doc/guides/user)


### Python
Install [Python 2.7.3](http://www.python.org), [pip](https://pypi.python.org/pypi/pip) and [virtualenv](http://www.virtualenv.org/en/latest/)

## Setup
### Python
A *virtualenv* is already included with the source - therefore from the root directory of the repository simply run `. ./activate`. This loads the Python environment and will have all necessary dependencies installed.

Then take some time to edit `config.py` and put in your AWS credentials and an API key from [ipinfodb](http://ipinfodb.com/ip_location_api.php).

### AWS
Follow the Amazon AWS console instructions to create a key pair and a security group. The key pair and security group have to be copied to all AWS regions.

Configure the parameters in `script/add_keypair` and then, from the main directory, run `sh scripts/add_keypair`. This will copy the keypair to all regions

Similarly, the command `python script/copy_security_groups.py` can be used to copy all security groups to all AWS regions.

### PlanetLab


### PlanetLab setup


### Pre-deployer setup


