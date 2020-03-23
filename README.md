# ansible-filter-iosconf

Ansible Jinja2 filters for extracting lines from Cisco IOS-style configurations. The filters require 
[*ciscoconfparse*](https://pypi.org/project/ciscoconfparse/) but the implemented API is somewhat different.
Only a small subset of the features of [*ciscoconfparse*](https://pypi.org/project/ciscoconfparse/) are 
implemented in *ansible-filter-iosconf*.

* ``iosconf_lines``
* ``iosconf_lines_with_child``
* ``iosconf_lines_without_child``
* ``iosconf_lines_with_childdren``
* ``iosconf_lines_without_childdren``
* ``iosconf_lines_with_parents``

The filters are meant to be used in conjunction with the ``ansible_net_config`` fact and the ``set_fact`` module. Check
the examples below for details.

Depending on the version of Ansible, ``ansible_net_config`` may not be populated by default. It is therefore
best to run the ``ios_facts`` (or equivalent module for other platforms) and explicitly list ``config`` under the ``gather_subset`` option.

```yaml
- name: Gather the configuration and some other facts.
  ios_facts:
    gather_subset:
      - config, hardware, interfaces   # or simply 'all'
```

The examples below work on the following IOS configuration fragment.
```
!
hostname router01
!
tacacs-server host 192.0.2.34
tacacs-server host 192.1.2.35
tacacs-server host 192.1.2.36
!
interface Ethernet2/0
 description Unprotected interface, facing towards Internet
 ip address 192.0.2.14 255.255.255.240
 no ip unreachables
 ntp disable
 no mop enable
 mtu 900
!
interface Ethernet2/1
 description Protected interface, facing towards DMZ
 ip address 192.0.2.17 255.255.255.240
 no mop enable
 
ip access-list extended LIST1
 allow ip host 10.1.1.1 host 10.99.99.99
 allow ip host 10.9.9.9 host 10.99.99.99
 allow ip host 10.1.1.1 host 192.168.1.1
!
ip access-list extended LIST2
 allow ip host 10.1.1.1 host 10.99.99.99
 allow ip host 10.1.1.1 host 172.16.1.1
```

## ``iosconf_lines``

The ``iosconf_lines`` filter extracts lines that match a regular expression.

The example below filters for any Tacacs+ servers in the ``192.1.2.*`` network and remove those.

```yaml
- name: Extract Tacacs+ server definitions
  set_fact: 
    old_tacacs_servers: "{{ ansible_net_config | iosconf_lines(r'^tacacs-server host 192\.1\.2\.') }}"

- name: Delete any Tacacs+ servers in the 192.1.2.0/24 network.
  ios_config:
    lines: "no {{ item }}"
  with_items: old_tacacs_servers
```

Using the ``iosconf_lines`` filter makes this playbook idempotent as the ``no ...`` command is only executed
if there are configuration lines that match the regular expression. Without the ``iosconf_lines`` it would be much
more difficult to achieve the same.
## ``iosconf_lines_with_child``
## ``iosconf_lines_without_child``
## ``iosconf_lines_with_childdren``
## ``iosconf_lines_without_childdren``
## ``iosconf_lines_with_parents``

 
