#!/bin/bash

python sensor_shock.py &
python sensor_movement.py &
python client.py &
