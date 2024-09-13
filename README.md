# Groover

Groover is an open source script for humanizing midi drums in the Reaper Midieditor.

## Usesage:

- Change the desired settings directly in the code or use Python's graphical user interface (goover.py) outside of Reaper to make changes.
- Select the notes you want in the midi editor and run the goover.lua script in Reaper.

## Settings:
(in the groover.lua file for example, change the value of the "local timingVariation" variable)

- maxVelocity: Drummer's maximum volume. (0-127)
- minVelocity: Drummer's minimum volume. (0-127)
- velocityVariation: How much is the intensity of the drum hit change, if 10 then 20 in total.
- timingVariation: 20 = +- 20ms, So a total is 40ms.
- swingAmount: Amount of swing. (0 = no swing, 1 = full swing)
- useHandednessFeature: Use of dexterity. (true = on use/false = not in use).
- handedness: Are you right- or left-handed? (right/left)
- handSrenght: Strength Difference Between Hands.
