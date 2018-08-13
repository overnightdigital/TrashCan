#!/usr/bin/python
import SmartTrash as trash
import Simulator as simulator
import config

trash.main(simulator.get_SimulatedValue(), config.oauth_credentials_for_device1, config.device_id1)