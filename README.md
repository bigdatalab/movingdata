# Uncovering the Perfect Place: Optimising Workflow Engine Deployment in the Cloud

## Technology overview
**Amazon AWS** is used to host the workflow orchestrator and run the analysis tools.

**PlanetLab** runs simple RESTful web services which receive an image, write it to the disk and retransmit it again. 

## Required tools
### AWS toolkit
To set up the Amazon AWS toolkit, follow the official guide: [http://aws.amazon.com/developertools/351](http://aws.amazon.com/developertools/351) and configure the toolkit with your AWS account credentials.

### PlanetLab
In order to set up the PlanetLab toolkit, follow the official getting started guide: [https://www.planet-lab.org/doc/guides/user](https://www.planet-lab.org/doc/guides/user)


### Python
Install [Python 2.7.3](http://www.python.org), [pip](https://pypi.python.org/pypi/pip) and [virtualenv](http://www.virtualenv.org/en/latest/)

## Setup
### Python
Set up a new *virtualenv* by following the getting started guide on [virtualenv](http://www.virtualenv.org/en/latest/) and then run `pip install -r requirements.txt`. This will install all requirements for the project.

Then take some time to edit `config.py` and put in your AWS credentials and an API key from [ipinfodb](http://ipinfodb.com/ip_location_api.php).

### AWS
Follow the Amazon AWS console instructions to create a key pair and a security group. The key pair and security group have to be copied to all AWS regions.

Configure the parameters in `script/add_keypair` and then, from the main directory, run `sh scripts/add_keypair`. This will copy the keypair to all regions

Similarly, the command `python script/copy_security_groups.py` can be used to copy all security groups to all AWS regions.

### PlanetLab
The PlanetLab setup files live in `eg/planetlab`. 

The file `eg/planetlab/nodes.txt` contains a list of PlanetLab nodes where the test web service workflows can be executed. When the project was started, a command was used to retrieve this list of nodes from the PlanetLab [comon](http://comon.cs.princeton.edu) service. However, as of March 2013, this service does not respond to requests and thus the list of live nodes cannot be queried anymore. Since PlanetLab nodes tend to go offline, it might be possible that none of the nodes defined in `nodes.txt` work.

The script file `eg/planetlab/pl.sh` is used to control the web services hosted on PlanetLab. 

`sh eg/planetlab/pl.sh deploy` copies the file in `eg/planetlab/cs4098/server.py` to every node defined in `nodes.txt`.

`sh eg/planetlab/pl.sh install` installs the Python dependencies on all nodes.

`sh eg/planetlab/pl.sh start` starts the web service on every node (accessible via HTTP on port 31415).

`sh eg/planetlab/pl.sh stop` stops the web service on every node.

## Workflow analysis
All the commands should be executed from the `deploy` directory.

### Defining Workflows
A sample workflow, which was used for the IEEE Conference Paper, is included. It loads the workflow specification from plain-text files in the `ieee/inputs` directory. Every line of these files contains a separate node in the workflow. The data source is defined in `deploy/ieee_test_workflow.py`.

### Generating random workflows
`python generator.py N` generates a random sequential workflow with N nodes (with replacement). It uses the nodes list in `eg/planetlab/nodes.txt` as a source. The workflow specification will be printed to *STDOUT*. 

For example, if a new workflow should be generated for the sample workflow, the following command could be used:

    python generator.py 5 > ../ieee/inputs/wf1.txt

### Running the preanalysis tool
`python ieee_analyzer.py WF.txt` runs the workflow specified in `ieee/inputs/WF.txt`. All logs are displayed in *STDERR*. *STDOUT* is automatically redirected to `ieee/outputs/WF.txt_pre`. This file contains the output of the analysis tool.

For example, if the workflow generated above should be analysed, the following command could be used:
    
    python ieee_analyzer.py wf1.txt

The result table can then be found in `ieee/outputs/wf1.txt_pre`.

### Executing the workflow
`python ieee_runner.py WF.txt REGION1,REGION2,..` runs the workflow specified in `ieee/inputs/WF.txt` in AWS EC2 regions REGION1 and REGION2. Similarly to the analysis tool, logs are displayed in *STDERR* and *STDOUT* is redirected to `ieee/outputs/WF.txt_output`.

For example, if the workflow generated above should be executed in the regions *us-east-1* and *us-west-2* and timed, the following command could be used:

    python ieee_runner.py wf1.txt us-east-1,us-west-2

The result table can then be found in `ieee/outputs/wf1.txt_output`.

## Running unit tests
Unit tests for the DAG implementation were written using the _testify_ framework. The tests can be invoked by simply running this command from the root directory:

    testify tests