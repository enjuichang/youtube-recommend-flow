#
# common
# NOTE: not to be use independtly
#

HIDE ?= @
SHELL := /bin/bash
ANSIBLE := docker run -it --rm -v ${HOME}/.ssh:/root/.ssh --workdir ${PWD} --env-file ./.env  -v ${HOME}:${HOME} docker.brainllc.net/brain/ansible:ansible
SERVICE_NAME ?= $(DOCKER_CONTAINER)

deploy.prod: .deps
	$(HIDE)$(ANSIBLE) --version
	$(HIDE)$(ANSIBLE) all -i $(SWARM_PRODUCTION)  -m shell --args 'make $(SERVICE_NAME).start chdir=$(SWARM_NAME)/docker_deploy/infrakit' -uubuntu --become

show.prod: .deps
	$(HIDE)$(ANSIBLE) all -i $(SWARM_PRODUCTION) -m shell --args 'make $(SERVICE_NAME).show chdir=$(SWARM_NAME)/docker_deploy/infrakit' -uubuntu

deploy.staging: .deps
	$(HIDE)$(ANSIBLE) --version
	$(HIDE)$(ANSIBLE) all -i $(SWARM_STAGING) -m shell --args 'make $(SERVICE_NAME)-staging.start chdir=$(SWARM_NAME)/docker_deploy/infrakit' -uubuntu --become

show.staging: .deps
	$(HIDE)$(ANSIBLE) all -i $(SWARM_STAGING) -m shell --args 'make $(SERVICE_NAME)-staging.show chdir=$(SWARM_NAME)/docker_deploy/infrakit' -uubuntu
