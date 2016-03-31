## Intro
An Ansible module which uses the datadog python library to idempotently manage Datadog dashboards. See the playbook dashboard_example.yaml for usage example.


## Getting Started
Add your datadog app and api keys to dashboard_example.yml and then simply run 'vagrant up' to get started with a Ubuntu VM with Ansible installed. The provisioning script will execute the example playbook.

## Example Output:

```
$ ansible-playbook dashboard_example.yml -i 'localhost,' --connection=local

PLAY [create datadog dashboards] **********************************************

TASK: [create cpu dashboard] **************************************************
ok: [localhost]

TASK: [check cpu dashboard idempotency] ***************************************
ok: [localhost]

TASK: [modify cpu dashboard] **************************************************
changed: [localhost]

PLAY RECAP ********************************************************************
localhost                  : ok=3    changed=1    unreachable=0    failed=0

```
