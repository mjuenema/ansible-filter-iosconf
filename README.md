# ansible-filter-iosconf

## Overview

**This project is currently in the planning stage**

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

## Installation

Install [*ciscoconfparse*](https://pypi.org/project/ciscoconfparse/) and then put the file ``iosconf.py`` into a folder named 'filter_plugins/'.

## Examples

The examples below work on the following IOS configuration fragment.
```
!
hostname router01
!
tacacs-server host 192.0.2.34
tacacs-server host 192.1.2.35
tacacs-server host 192.1.2.36
!
interface FastEthernet2/0
 description Unprotected interface, facing towards Internet
 ip address 192.0.2.14 255.255.255.240
 no ip unreachables
 ntp disable
 no mop enable
 mtu 900
!
interface FastEthernet2/1
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

The ``iosconf_lines_with_child`` filter finds sections matching a regular expression that contain a child line 
that matches a second regular expression. 

The code below ensures that no Fast Ethernet interfaces has an explicit MTU configured.

```yaml
- name: Find Fast Ethernet interfaces with explicit MTU
  set_fact: 
    if_with_mtu: "{{ ansible_net_config | iosconf_lines_with_child(r'interface FastEthernet', r'mtu \d+'}}"
    
- name: Delete the explicit MTU from Fast Ethernet interfaces
  ios_config:
    lines: "no mtu"
    parents: "{{ item }}"
  with_items: if_with_mtu
```

## ``iosconf_lines_without_child``

The ``iosconf_lines_without_child`` filter is effectively the opposite to the ``iosconf_lines_with_child`` filter. It
returns a list of sections that match a regular expressions but *do not* have a child line that match a second regular expression. This can be used to amend sections that are missing a setting.

```yaml
- name: Find Fast Ethernet interfaces that do not have NTP disabled.
  set_fact: 
    if_not_ntp_disable: "{{ ansible_net_config | iosconf_lines_with_child(r'interface FastEthernet', r'ntp disabled'}}"
    
- name: Disable NTP on all Fast Ethernet interfaces
  ios_config:
    lines: "ntp disable"
    parents: "{{ item }}"
  with_items: if_not_ntp_disable
```

## ``iosconf_lines_with_childdren``

The ``iosconf_lines_with_children`` (multiple children) is a variation of ``iosconf_lines_with_child`` (single child) where
the list of returned sections must contain all child regular expressions.

```yaml
- name: Find Fast Ethernet interfaces that have IP unreachables and mop disabled.
  set_fact: 
    found: "{{ ansible_net_config | iosconf_lines_with_children(r'^interface', [r'no ip unreachables', r'no mop enable'])
 ```

## ``iosconf_lines_without_children``

The ``iosconf_lines_without_children`` returns section lines that contain none of the child regular expressions.

```yaml
- name: Find Fast Ethernet interfaces that have neither IP unreachables nor NTP disabled.
  set_fact: 
    found: "{{ ansible_net_config | iosconf_lines_without_children(r'^interface', [r'no ip unreachables', r'no ntp disable'])
 ```

## ``iosconf_lines_with_parent``

The ``iosconf_lines_with_parents`` filter returns children of a section. The filter is actually a bit too powerful as the 
first regular expression can match multiple sections, making it impossible to know what parent a returned line belongs to. 
In most cases (I can think of, anyway) is recommended to ensure that the first regular expression only matches a single s
section as shown in the following example.

```yaml
- name: Find entries with 10.99.99.99 in access list LIST1
  set_fact: 
    acl_entries: "{{ ansible_net_config | iosconf_lines_with_parent(r'^ip access-list extended LIST1$', r'10\.99\.99\.99'}}"

- name: Delete any access list entries referring to 10.99.99.99
  ios_config:
    lines: "no {{ item }}"
    parents: ip access-list extended LIST1
  with_items: acl_entries
```
