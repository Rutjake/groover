# Groover v1.1

Groover is an open source script for humanizing midi drums in the Reaper Midi editor.

## How to use:

Stand-alone:
- Download groover.exe, groover.lua, preset.json, settings.json and help.md from dist directory.

Source code:
- Download groover.py, groover.lua, preset.json, settings.json and help.md from root directory.
  (requires Python to be installed)

Use:
- Change the desired settings directly in the code or use Python gui (groover.py or groover.exe) outside of Reaper to make changes.
- Select the notes you want in the midi editor and run the goover.lua script in Reaper.

## Settings:
(in the groover.lua file change the value of the ("local timingVariation") variable for example or use the gui )

- maxVelocity: Drummer's maximum volume. (0-127)
- minVelocity: Drummer's minimum volume. (0-127)
- velocityVariation: How much is the intensity of the drum hit change, if 10 then 20 in total.
- timingVariation: 20 = +- 20ms, So a total is 40ms.
- swingAmount: Amount of swing. (0 = no swing, 1 = full swing)
- useHandednessFeature: Use of handedness. (true = on use, false = not in use).
- handedness: Are you right- or left-handed? (right/left)
- handSrenght: Strength Difference Between Hands.

Tips:

- Handedness is great for fills simulating the drum hit, but it can also be used in double bass drum parts to simulate different feet.

- The presets are made to speed up the editing process.
