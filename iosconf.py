"""
ansible-filter-iosconf

Put this file into a folder named 'filter_plugins/' and read the instructions
on https://github.com/mjuenema/ansible-filter-iosconf.

(c) Markus Juenemann, 2020

"""

import ciscoconfparse

def _parse_config(config):
    return ciscoconfparse.CiscoConfParse(config.split('\n'))


def iosconf_lines(config, lineregex):
    cfg = _parse_config(config)
    return [ioscfgline.text 
            for ioscfgline in cfg.find_objects(lineregex)]
    
    
def iosconf_lines_with_child(config, parentregex, childregex):
    cfg = _parse_config(config)
    return [ioscfgline.text 
            for ioscfgline in cfg.find_objects_w_child(parentregex, childregex)]


def iosconf_lines_without_child(config, parentregex, childregex):
    cfg = _parse_config(config)
    return [ioscfgline.text 
            for ioscfgline in cfg.find_objects_wo_child(parentregex, childregex)]


def iosconf_lines_with_children(config, parentregex, childregexes):
    cfg = _parse_config(config)
    return [ioscfgline.text 
            for ioscfgline in cfg.find_objects_w_all_children(parentregex, childregexes)]


def iosconf_lines_without_children(config, parentregex, childregexes):
    cfg = _parse_config(config)
    return [ioscfgline.text 
            for ioscfgline in cfg.find_objects_w_missing_children(parentregex, childregexes)]


def iosconf_lines_with_parents(config, parentregex, childregex):
    cfg = _parse_config(config)
    return [ioscfgline.text 
            for ioscfgline in cfg.find_objects_w_parents(parentregex, childregex)]


class FilterModule(object):
    def filters(self):
        return {
            'iosconf_lines': iosconf_lines,
            'iosconf_lines_with_child': iosconf_lines_with_child,
            'iosconf_lines_without_child': iosconf_lines_without_child,
            'iosconf_lines_with_children': iosconf_lines_with_children,
            'iosconf_lines_without_children': iosconf_lines_without_children,
            'iosconf_lines_with_parents': iosconf_lines_with_parents
        }
