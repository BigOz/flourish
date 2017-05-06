# Will start the simulator. Pass either "True" or "False" where appropriate.
# Look ahead depth can be any integer greater than 0. The program will not
# start if invalid input is given.

python3 src/start_simulator.py \
    --solar_panels="True" \
    --smart_battery="True" \
    --smart_home="True" \
    --look_ahead_depth=24
