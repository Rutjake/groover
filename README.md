# Groover v1.2
<img src="/screen/GrooverGui.JPG" height="400">
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

## Tips:

- Use a Drumkit preset for the entire drum track.

- Handedness is great for fills to simulating the drum hit, but it can also be used in double bass drum parts to simulate different feet.

- The handedness is also useful with the hi-hat and ride cymbal to make it groovy and human by adding accents in the right places. For example, right-handedness to the 8th beat and left-handedness to the 4th beat.

- The presets are made to speed up the editing process.

- In presets "Tom" setting is made for fills, preset works well in snare fills also.
