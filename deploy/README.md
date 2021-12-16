# How to deploy the docker containers?

## Using Windows:
In Windows Powershell execute the following command **from this directory**:

        & .\app_start.ps1

All the containers will be deployed automatically by executing this script.
## Using Linux:
In terminal execute the following command **from this directory**:

        img_build.sh [NAME OF THE APP TO DEPLOY]

The containers must be deployed by stating the name of the app to start.

# How to set environment variables for this project? (without deploying the containers)
Please note that this step is already included if you deployed the containers with the script above, so it is NOT necessary to do it again. 
 

## Using Windows:
In Windows Powershell execute the following command **from this directory**:

        & .\env.ps1

## Using Linux:
Configure environment variables CDN_REGISTRY ("localhost:5000") and CDN_HOME depending of the directory path on your own system.