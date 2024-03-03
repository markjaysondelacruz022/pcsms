**Development Setup Instruction**
- [Set up Ubuntu WSL System](#set-up-ubuntu-wsl-system)
    - [Set up Ubuntu WSL System](#set-up-ubuntu-wsl-system)
	- [Setup Option](#setup-option)
		- [Manual](#manual)
			- [Ubuntu WSL Manual Setup](#ubuntu-wsl-manual-setup)
			- [Frappe Bench Manual Setup](#frappe-bench-manual-setup)
		- [Docker](#cocker)
			- [Docker Setup (VS Code)](#docker-setup-vs-code)

## Development Instruction
### Set up Ubuntu WSL System
#### 1. Install Ubuntu WSL 
	Available in Microsoft Store

#### 2. Enable Windows Subsystem for Linux
	- Open “Turn Windows feature on and off”
	- Check "Windows Subsystem for Linux”

### Setup Option

### Manual

### Ubuntu WSL Manual Setup
1. [Ubuntu WSL Setup Instruction](#ubuntu-wsl-setup-instruction)
	- [Set up Ubuntu WSL System](#set-up-ubuntu-wsl-system)
		1. [Open Ubuntu Terminal](#1-open-ubuntu-terminal)
		2. [Install git, curl and nano](#2-install-git-curl-and-nano)
		3. [Install Python 3.10](#3-install-python-310)
		4. [Install Maria DB](#4-install-maria-db)
		5. [Install Redis Server](#5-install-redis-server)
		6. [Create User](#6-create-user)
		7. [Switch to user](#7-switch-to-user)
		8. [Install Node 16](#8-install-node-16)
		9. [Install Frappe Bench](#9-install-frappe-bench)
2. [Ubuntu Encountered Errors](#ubuntu-encountered-errors)
	1. [System has not been booted with systemd as init system (PID 1). Can't operate](#1-system-has-not-been-booted-with-systemd-as-init-system-pid-1-cant-operate)

##### 1. Open Ubuntu Terminal
	Open powershell and type‘wsl -d ubuntu’ or open the Ubuntu app
	sudo apt update 
	sudo apt -y upgrade

##### 2. Install git, curl and nano
		sudo apt install git
		git –version - check version
		sudo apt install curl
		curl –version - check version
		sudo apt install nano
		nano –version - check version

##### 3. Install Python 3.10
		sudo apt install python3.10 python3.10-dev python3-pip python3.10-venv -y
		python3  -V - check version

##### 4. Install Maria DB
		sudo apt install mariadb-server
		(optional)sudo mysql_secure_installation 
			- Note: set a password for root user to avoid error creating a frappe site
		sudo systemctl start mariadb - start mariadb service
		sudo systemctl status mariadb - check mariadb status
		sudo systemctl enable mariadb - set mariadb running upon boot up

##### 5. Install Redis Server
		sudo apt install -y redis-server
		sudo systemctl start redis-server - start redis-server
		sudo systemctl status redis-server - check redis-server status
		sudo systemctl enable redis-server - set redis-server running upon boot up

##### 6. Create User
		sudo adduser frappe 
		sudo usermod -a -G sudo frappe

##### 7. Switch to user
		sudo su - frappe
		cd /home/frappe

##### 8. Install Node 16
		curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.38.0/install.sh | bash
		Restart wsl
			- exit
			- wsl -t ubuntu - stop services
			- wls -d ubuntu  - open ubuntu
		nvm install 16
		node --version - check version
		nvm alias default 16 - set default node version

##### 9. Install Frappe Bench
		sudo pip3 install frappe-bench
		Type ‘bench’ to check if already install



### Ubuntu Encountered Errors 
##### 1. System has not been booted with systemd as init system (PID 1). Can't operate.
		Fix:
			- sudo nano /etc/wsl.conf
			- add script:
				[boot]
				systemd=true
			Save (ctrl s to save then ctrl x to exit)
			Restart wsl
				- Exit
				- wsl -t ubuntu  - stop services
				- wls -d ubuntu  - open ubuntu

### Frappe Bench Manual Setup
1. [Frappe Bench Setup Instruction](#frappe-bench-setup-instruction)
	- [Create Frappe Bench](#create-frappe-bench)
		1. [Bench Initialization Command](#1-bench-initialization-command)
		2. [Get Apps for Frappe Bench](#2-get-apps-for-frappe-bench)
		3. [Create New Site](#3-create-new-site)
		4. [Install Apps to Created Site](#4-install-apps-to-created-site)
		5. [Use Created Site](#5-use-created-site)
		6. [Build Bench](#6-build-bench)

    - [Add Custom App from Git](#add-custom-app-from-git)

        7. [Git Clone](#7-git-clone)        
        8. [Install App from Git Clone](#8-install-app-from-git-clone)
2. [Other Useful Frappe Commands](#other-useful-frappe-commands)
	1. [Migrate Updates](#migrate-updates)
	2. [Export Fixtures](#export-fixtures)
	3. [Export Customization](#export-customization)
3. [Other Useful Git Commands](#other-useful-git-commands)
	1. [Updating Files from Repository](#updating-files-from-repository)
	2. [Branching](#branching)
	3. [Merging](#merging)

----

### Frappe Bench Setup Instruction

#### - Create Frappe Bench
##### 1. Bench Initialization Command 
        bench init  pasig-lgu --frappe-path https://github.com/frappe/frappe --frappe-branch version-14 --python python3.10

> *Note: where 'pasig-lgu' is the bench name*

***Run the following commands inside created bench folder (in this case pasig-lgu)***

##### 2. Get Apps for Frappe Bench
	    - bench get-app --branch version-14 erpnext --resolve-deps
		- bench get-app payments --resolve-deps

##### 3. Create New Site
	    bench new-site pcsms.local
> *Note: where 'pcsms.local' is the site name*

##### 4. Install Apps to Created Site
		bench --site pcsms.local install-app erpnext
		bench --site pcsms.local install-app payments

##### 5. Use Created Site
		bench use pcsms.local

##### 6. Build Bench
		bench start

----

#### - Add Custom App from Git
##### 7. Git Clone
        bench get-app http://ec2-52-32-195-219.us-west-2.compute.amazonaws.com/jamie.castro/pcsms.git

##### 8. Install App from Git Clone
        bench --site pcsms.local install-app pcsms

---

### Other Useful Frappe Commands 
##### 1. Migrate Updates
        bench --site pcsms.local migrate
##### 2. Export Fixtures
        bench --site pcsms.local export-fixtures
##### 3. Export Customization
        1. make sure developer mode is set to 1 or true
            a. bench set-config -g developer_mode true
            b. restart bench
        2. refresh site (Web)
        3. go to customization view
        4. click actions
        5. select export customization
        6. fill-in module -> select pasig-lgu
        7. click submit

---

### Other Useful Git Commands 
##### 1. Updating Files from Repository
        git remote set-branches upstream "*"
        git fetch -v --depth=1
        git pull

##### 2. Branching
        1. git checkout main
        2. git checkout -b [FEATURE-BRANCH]
        3. git push --set-upstream upstream [FEATURE-BRANCH]

##### 3. Merging
        1. git fetch
        2. git pull
        3. git pull upstream main
        4. git push upstream [FEATURE-BRANCH]

## Docker        

## Docker Setup (VS Code)
1. [Docker Setup Instruction](#docker-setup-instruction)
	1. [Install Docker](#1-install-docker)
	2. [Enable Docker in Ubuntu WSL](#2-enable-docker-in-ubuntu-wsl)
	3. [Open Ubuntu Terminal](#3-open-ubuntu-terminal)
	4. [Create User](#4-create-user)
	5. [Switch to user](#5-switch-to-user)
	6. [Clone frappe docker from official repo](#6-clone-frappe-docker-from-official-repo)
	7. [Copy Devcontainer And VScode Example](#7-copy-devcontainer-and-vscode-example)
	8. [Install Dev Container in VS Code](#8-install-dev-container-in-vs-code)
	9. [Reopen DevContainer](#9-reopen-devcointaner)
	10. [Create apps.json](#10-create-appsjson)
	11. [Install Frappe and Project App](#11-install-frappe-and-project-app)
	12. [Bench Start](#12-bench-start)
2. [Docker Development Commands](#docker-development-commands)
	1. [Stop Container Services](#1-stop-container-services)
	2. [Start Container Services](#2-start-container-services)
	3. [List Containers](#3-list-containers)
	4. [Enter Shell](#4-enter-shell)

### Docker Setup Instruction
##### 1. Install Docker
	- can be downloaded from docker site(#https://www.docker.com/products/docker-desktop)

##### 2. Enable Docker in Ubuntu WSL
	- Open docker desktop
	- Go to settings(gear icon at the top right of the app)
	- Click Resources
	- Select WSL integration
	- Check the "Enable integration with my default WSL distro" option

##### 3. Open Ubuntu Terminal
	Open powershell and type‘wsl -d ubuntu’ or open the Ubuntu app

##### 4. Create User
		sudo adduser frappe 
		sudo usermod -a -G sudo frappe

##### 5. Switch to user
		sudo su - frappe
		cd /home/frappe
##### 6. Clone frappe docker from official repo
		- git clone https://github.com/frappe/frappe_docker pcsms_docker
		- cd pcsms_docker

##### 7. Copy Devcontainer And VScode Example
		- cp -R devcontainer-example .devcontainer
		- cp -R development/vscode-example development/.vscode

##### 8. Install Dev Container in VS Code
		- Open Vscode 
		- go to plugins
		- Install Dev Container plugin

##### 9. Reopen DevContainer
		- In Vscode, in lower left, open remote window
		- type "Reopen DevContainer"
		- wait for 5-10mins to setup devcontainer

##### 10. Create apps.json
		- create apps.json file and add the project app:
			- [
                    {
                        "url": "https://github.com/frappe/payments.git",
                        "branch": "version-14"
                    },
                    {
                        "url": "https://github.com/frappe/erpnext.git",
                        "branch": "version-14"
                    },
                    {
                        "url": "http://<username>:<token>@ec2-52-32-195-219.us-west-2.compute.amazonaws.com/jamie.castro/pcsms.git",
                        "branch": "dev"
                    }
			  ]
		- take note of the branch, it should be a develop branch
        - must be whitelisted to access pcsms git url

##### 11. Install Frappe and Project App
		- ./installer.py -t version-14 -p 3.10 -n v16 -j apps.json -v

##### 12. Bench Start
		- cd frappe-bench
		- nvm use 16
		- bench start
		- navigate to browser http://development.localhost:8000

### Docker Development Commands

##### 1. Stop Container Services
	- go to root folder of psg_lgu_docker
	- sudo docker-compose -p pcsms_docker_devcontainer -f .devcontainer/docker-compose.yml down
	- you should see the list of containers being remove 

##### 2. Start Container Services
	- go to root folder of psg_lgu_docker
	- sudo docker-compose -p pcsms_docker_devcontainer -f .devcontainer/docker-compose.yml up -d
	- you should see the list of containers being started 

##### 3. List Containers
    - sudo docker ps --filter name=pcsms_docker_devcontainer

##### 4. Enter Shell
    - if not using vs code, this can be use for opening the dev container
	- make sure the services already started
    - go to root folder of psg_lgu_docker
	- list all containers
	- look for image frappe/bench:latest then get its name, it is usually 'pcsms_docker_devcontainer-frappe-1'
	- sudo docker exec -w /workspace/development -it pcsms_docker_devcontainer-frappe-1 bash
	- 'exit' to exit the devcontainer shell
