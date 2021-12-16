# How to build the images?

## Using Windows:
In Windows Powershell execute the following command **from this directory**:

        & .\img_build.ps1

Everything will be built automatically by executing this script.

## Using Linux:

# How to set environment variables for this project (without building images)?

## Using Windows:
Please note that this step is already included if you built the images with the script above, so it is NOT necessary to do it again. 
In Windows Powershell execute the following command **from this directory**:

        & .\env.ps1

## Using Linux:
Configure environment variables CDN_REGISTRY ("localhost:5000") and CDN_HOME depending of the directory path on your own system.