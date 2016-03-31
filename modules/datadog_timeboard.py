#!/usr/bin/python
import json
import os
import sys

try:
    from datadog import initialize, api
except ImportError:
    print "failed=True msg='datadog required for this module'"
    sys.exit(1)

# Check if a timeboard with the same title exists and return its id. Return -1 if doesn't exist.
def get_timeboard_id(title):
    timeboards = api.Timeboard.get_all()['dashes']
    for timeboard in timeboards:
        if title == timeboard['title']:
            return timeboard['id']
    return -1

def timeboards_match(id, title, description, graphs):
    existing = api.Timeboard.get(id)['dash']
    return (existing['title'], existing['description'], existing['graphs']) == (title, description, graphs)

def main():

    module=AnsibleModule(
        argument_spec=dict(
            app_key=dict(),
            api_key=dict(),
            state=dict(default='present', choices=['present', 'absent']),
            src=dict(),
            title=dict(),
            description=dict(),
        )
    )

    app_key = module.params['app_key']
    api_key = module.params['api_key']
    state = module.params['state']
    template = module.params['src']
    template = os.path.realpath(template)
    timeboard_title = module.params['title']
    timeboard_description = module.params['description']

    try:
        initialize(api_key, app_key) # Do not mute exceptions.

        # Load the json timeboard template.
        try:
            with open(template) as data_file:
                timeboard_graphs = json.load(data_file)
        except Exception as e:
            module.fail_json(msg="Could not load timeboard template json: " + e.strerror)

        # Check if a board with the same title exists and get its id.
        timeboard_id = get_timeboard_id(timeboard_title)

        # Create a new timeboard if no id.
        if timeboard_id == -1:
            try:
                response = api.Timeboard.create(title=timeboard_title, description=timeboard_description, graphs=timeboard_graphs)
            except Exception as e:
                module.fail_json(msg=e)
            module.exit_json(changed=True)
        else:
            # Check if existing needs to be updated.
            if timeboards_match(timeboard_id, timeboard_title, timeboard_description, timeboard_graphs):
                module.exit_json(changed=False)
            else:
                try:
                    response = api.Timeboard.update(timeboard_id, title=timeboard_title, description=timeboard_description, graphs=timeboard_graphs)
                except Exception as e:
                    module.fail_json(msg='Could not update timeboard: ' + str(e.message))
                module.exit_json(changed=True)
    except Exception as e:
        module.fail_json(msg="Unexpected failiure: " + str(e.message))

# this is magic, see lib/ansible/module_common.py
#<<INCLUDE_ANSIBLE_MODULE_COMMON>>

main()
