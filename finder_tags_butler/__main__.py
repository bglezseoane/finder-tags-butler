# -*- coding: utf-8 -*-

###########################################################
# Finder Tags Butler
#
# Synchronize Mac OS Finder tags between several machines
#
# Copyright 2020 Borja González Seoane
#
# Contact: garaje@glezseoane.es
###########################################################

"""Finder Tags Butler main entrypoint."""

from finder_tags_butler import controller_layer

if __name__ == "__main__":
    # Delegate to the controller
    controller_layer.main()
