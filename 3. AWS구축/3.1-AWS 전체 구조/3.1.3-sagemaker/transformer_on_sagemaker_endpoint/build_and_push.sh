#!/bin/bash
set -v
set -e
# This script shows how to build the Docker image and push it to ECR to be ready for use
# by SageMaker.

# The argument to this script is the image name. This will be used as the image on the local
# machine and combined with the account and region to form the repository name for ECR.
image=$1

if [ "$image" == "" ]
then
    echo "Use image name transformer"
    image="transformer"
fi

# Get the account number associated with the current IAM credentials
account=$(aws sts get-caller-identity --query Account --output text)

if [ $? -ne 0 ]
then
    exit 255
fi

# Get the region defined in the current configuration
region=$(aws configure get region)
#regions=$(aws ec2 describe-regions --all-regions --query "Regions[].{Name:RegionName}" --output text)

#for region in $regions; do

#aws s3 cp s3://aws-solutions-${region}/spot-bot-models/cars/model.tar.gz ./
#tar zxvf model.tar.gz
# TODO: update regional location based on https://amazonaws-china.com/releasenotes/available-deep-learning-containers-images/

fullname="${account}.dkr.ecr.${region}.amazonaws.com/${image}:latest"
registry_uri="${registry_id}.dkr.ecr.${region}.amazonaws.com"

echo ${fullname}

# If the repository doesn't exist in ECR, create it.
aws ecr describe-repositories --repository-names "${image}" --region ${region} || aws ecr create-repository --repository-name "${image}" --region ${region}


# Get the login command from ECR and execute it directly
aws ecr get-login-password --region "${region}" | docker login --username AWS --password-stdin "${account}".dkr.ecr."${region}".amazonaws.com

aws_access_key_id=$(echo $AWS_ACCESS_KEY_ID)
aws_secret_access_key=$(echo $AWS_SECRET_ACCESS_KEY)

# Build the docker image, tag with full name and then push it to ECR
docker build -t ${image} -f Dockerfile . --build-arg REGISTRY_URI=${registry_uri} --build-arg AWS_ACCESS_KEY_ID=${aws_access_key_id} --build-arg AWS_SECRET_ACCESS_KEY=${aws_secret_access_key} --build-arg AWS_DEFAULT_REGION=${region}
docker tag ${image} ${fullname}
docker push ${fullname}

#done