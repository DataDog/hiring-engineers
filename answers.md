Your answers to the questions go here.

### Level 0 (optional) - Setup an Ubuntu VM

I Amazon EC2 to create Ubuntu environment.

The machine image I used is `Ubuntu Server 16.04 LTS (HVM), SSD Volume Type` and its ID is `ami-6e1a0117`.

```
## Using AWS CLI
$ aws --version
aws-cli/1.11.155 Python/2.7.12 Darwin/16.7.0 botocore/1.7.13

## Create an instance
$ aws ec2 run-instances --image-id ami-6e1a0117 --instance-type t2.micro --key-name dd-challenge
{
    "Instances": [
        {
...
            "InstanceId": "i-0be3d85889b8b029d",
...
            "NetworkInterfaces": [
                {
...
                    "Groups": [
                        {
                            "GroupName": "default",
                            "GroupId": "sg-08897867"
...

## Adding an ingress rule to the security group to connect with SSH
$ aws ec2 authorize-security-group-ingress --group-id sg-08897867 --cidr $(curl -s checkip.amazonaws.com)/32 --protocol tcp --port 22

## Getting public hostname to connect
$ aws ec2 describe-instances --instance-id i-0be3d85889b8b029d
{
    "Reservations": [
        {
            "Instances": [
                {
...
                    "PublicDnsName": "ec2-52-34-99-226.us-west-2.compute.amazonaws.com",
...

## Avoid `UNPROTECTED PRIVATE KEY FILE` error
$ chmod 600 ~/Downloads/dd-challenge.pem

## Connect to the instance
$ ssh -i ~/Downloads/dd-challenge.pem ubuntu@ec2-52-34-99-226.us-west-2.compute.amazonaws.com
Welcome to Ubuntu 16.04.2 LTS (GNU/Linux 4.4.0-1022-aws x86_64)

...

ubuntu@ip-172-31-22-56:~$
```
