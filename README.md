# nonno-care

## Getting Started

### Prerequisites
* [AWS Command Line Interface](https://aws.amazon.com/cli/)
* [Python3.6](https://www.python.org/)
    * [boto3](https://boto3.amazonaws.com/v1/documentation/api/latest/index.html)
    * [numpy](https://numpy.org/)
    * [sagemaker](https://pypi.org/project/sagemaker/)

## Installing
Install the python libraries:
```bash
$ pip3 install -r ml_training/requirements.txt
$ pip3 install -r wirlband_simulator/requirements.txt
```

## Deployment
Choose a suitable AWS region and start training the Sagemaker Model submitting an existing S3 bucket:
```bash
$ BUCKET=sample-bucket-name
$ bash train_model.sh $BUCKET
```
and then deploy the stack resources : 
```bash
$ REGION=sample-region
$ bash deploy.sh $REGION $BUCKET
```

## Running Example
Before starting the simulator, verify an email address in order to receive notifications:
```bash
$ bash verify_email.sh receiver@example.com
```
and by clicking on the link you receive, then update the *EMAIL* field in
the [config.ini](wirlband_simulator/config.ini) configuration file.

Finally start the simulator, for example, to simulate 2 sample users:
```bash
$ cd wirlband_simulator/
wirlband_simulator$ python3 simulator.py 2
```
otherwise to simulate a batch of 500 users:
```bash
$ bash start_sensors.sh 2
```

In the end to stop the simulation:
```bash
$ bash stop_sensors.sh
```

## Authors

* **Falvo Simone**
* **Pietrangeli Aldo**

## License
This project is licensed under the GNU GPL v3.0 License - see the [LICENSE](LICENSE) file for details


## Acknowledgments
[E. Casilari and J. A.Santoyo-Ramón, “UMAFall: Fall Detection
Dataset (Universidad de Malaga),” 6 2018.](https://figshare.com/articles/UMA_ADL_FALL_Dataset_zip/4214283)
