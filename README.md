# ansible-filter-iosconf

Ansible Jinja2 filters for extracting lines from Cisco IOS-style
configurations. The filters require [*ciscoconfparse*](https://pypi.org/project/ciscoconfparse/)
but the implemented API is somewhat different. Only a small subset of the
features of *ciscoconfparse*](https://pypi.org/project/ciscoconfparse/) are 
implemented in *ansible-filter-iosconf*.

* ``iosconf_lines``
* ``iosconf_lines_with_child``
* ``iosconf_lines_without_child``
* ``iosconf_lines_with_childdren``
* ``iosconf_lines_without_childdren``
* ``iosconf_lines_with_parents``

The filters are meant to be used in conjunction with the 
``ansible_network_config`` fact. Depending on the version of Ansible,
``ansible_network_config`` may not be populated by default. It is therefore
best to run the ``ios-facts`` (or equivalent module for other platforms)
and explicitly list ``config`` under the ``gather_subset`` option.

```yaml
- name: Gather only the config and default facts
  ios_facts:
    gather_subset:
      - config, hardware, interfaces   # or simply 'all'
```

## ``iosconf_lines``
## ``iosconf_lines_with_child``
## ``iosconf_lines_without_child``
## ``iosconf_lines_with_childdren``
## ``iosconf_lines_without_childdren``
## ``iosconf_lines_with_parents``

 