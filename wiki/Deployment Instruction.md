## Deployment Instruction
1. [Docker Deployment](#docker-deployment)
	1. [Prerequisite](#1-prerequisite)
	2. [Create Folder](#2-create-folder)
	3. [Get PCSMS docker resources](#3-get-pcsms-docker-resources)
		- [ContainerFile](#containerfile)
		- [NGINX Files](#nginx-files)
		- [PWD File](#pwd-file)
		- [Apps Json File](#apps-json-file)
	4. [Encode apps.json To Base64](#4-encode-appsjson-to-base64)
	5. [Build Image](#5-build-image)
	6. [Start Services](#6-start-services)
	7. [Check Site Logs](#7-check-site-logs)
	8. [Check and Navigate Browser](#8-check-and-navigate-browser)
2. [Docker Prod Commands](#docker-prod-commands)
	- [Stop Prod Container Services](#stop-prod-container-services)
	- [Start Prod Container Services](#start-prod-container-services)
	- [List Prod Containers](#list-prod-containers)
	- [Enter Prod Shell](#enter-prod-shell)
	- [Enter MariaDB](#enter-mariadb)

### Docker Deployment
##### 1. Prerequisite
	- Ubuntu Server with Docker Engine and jq

##### 2. Create Folder
	- mkdir pcsms_docker

##### 3. Get PCSMS docker resources

	NOTE: check your environment and change all <env> and <account_token> accordingly (dev, stg or prod)

##### Docker Container File: 
##### ContainerFile:
	- curl "http://ec2-52-32-195-219.us-west-2.compute.amazonaws.com/api/v4/projects/851/repository/files/docker%2FContainerfile?ref=resources&&private_token=<account_token>" | jq -r '.content' |      base64 -d > Containerfile

##### nginx Files:
	- mkdir -p resources && curl "http://ec2-52-32-195-219.us-west-2.compute.amazonaws.com/api/v4/projects/851/repository/files/docker%2Fresources%2Fnginx-entrypoint.sh?ref=resources&&private_token=glpat-<account_token>" | jq -r '.content' |      base64 -d > resources/nginx-entrypoint.sh
	- mkdir -p resources && curl "http://ec2-52-32-195-219.us-west-2.compute.amazonaws.com/api/v4/projects/851/repository/files/docker%2Fresources%2Fnginx-template.conf?ref=resources&&private_token=<account_token>" | jq -r '.content' |      base64 -d > resources/nginx-template.conf
		
##### PWD File:
	- curl "http://ec2-52-32-195-219.us-west-2.compute.amazonaws.com/api/v4/projects/851/repository/files/docker%2Fpwd-dev.yml?ref=resources&&private_token=<account_token>" | jq -r '.content' | base64 -d > pwd-<env>.yml
		
##### Apps Json File:
	- curl "http://ec2-52-32-195-219.us-west-2.compute.amazonaws.com/api/v4/projects/851/repository/files/docker%2Fapps-dev.json?ref=resources&&private_token=<account_token>" | jq -r '.content' | base64 -d > apps-<env>.json

##### 4. Encode apps.json To Base64
	- export APPS_JSON_BASE64=$(base64 -w 0 apps-<env>.json)
	- check APPS_JSON_BASE64 value
		- echo $APPS_JSON_BASE64

##### 5. Build Image
	- docker build \
		--build-arg=FRAPPE_PATH=https://github.com/frappe/frappe \
		--build-arg=FRAPPE_BRANCH=version-14 \
		--build-arg=PYTHON_VERSION=3.10.12 \
		--build-arg=NODE_VERSION=16.20.2 \
		--build-arg=APPS_JSON_BASE64=$APPS_JSON_BASE64 \
		--tag=pcsms-<env>:latest \
		--file=Containerfile .

##### 6. Start Services
	- sudo docker compose -p pcsms-<env> -f pwd-<env>.yml up -d

##### 7. Check Site Logs
	- sudo docker logs pcsms-<env>-create-site-1 -f

##### 8. Check and Navigate Browser
	Dev
		- https://devpcsms.xurpasenterprise.com/
	STG
		- https://devpcsms.xurpasenterprise.com/
	PROD
		- https://devpcsms.xurpasenterprise.com/
### Docker Prod Commands

##### - Stop Prod Container Services
	- go to root folder of pcsms_docker
	- sudo docker compose -p pcsms-<env> down
	- you should see the list of containers being remove 

##### - Start Prod Container Services
	- go to root folder of pcsms_docker
	- sudo docker compose -p pcsms-<env> -f pwd-<env>.yml up -d
	- you should see the list of containers being started 

##### - List Prod Containers
    - sudo docker ps --filter name=pcsms-<env>

##### - Enter Prod Shell
	- make sure the pcsms docker container/services already started
	- sudo docker exec -it pcsms-<env>-backend-1 bash
##### - Connect to MariaDB Container
	- make sure the pcsms docker container/services already started
	- sudo docker exec -it pcsms-<env>-db-1 bash
	- login to mysql:
		- Root
			- check mysql root password
				- $echo $MYSQL_ROOT_PASSWORD
			- mysql -u root -p
		- app db credentials
			- exit to Mariadb Container
			- Enter Prod Shell
			- Check credentials
				- less /home/frappe/frappe-bench/sites/frontend/site_config.json
			- enter to mariadb container again then execute mysql command
				- mysql -u <db_name> -p