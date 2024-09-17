
Topics:

- How to use
- Settings
- Tips

How to use:

- Change the desired settings directly in the groover.lua code or use Python gui (groover.py or groover.exe) outside of Reaper to make changes.
- Select the notes you want in the midi editor and run the goover.lua script in Reaper.

Settings:

(in the groover.lua file change the value of the ("local timingVariation") variable for example or use the gui )

- maxVelocity: Drummer's maximum volume. (0-127)
- minVelocity: Drummer's minimum volume. (0-127)
- velocityVariation: How much is the volume of the drum hit change, if the setting is 10, then the total is 20.
- timingVariation: 20 = +- 20ms, So a total is 40ms.
- swingAmount: Amount of swing. (0 = no swing, 1 = full swing)
- useHandednessFeature: Use of handedness. (true = on use, false = not in use).
- handedness: Are you right- or left-handed? (right/left)
- handSrenght: Strength Difference Between Hands.

Tips:

- Handedness is great for fills simulating the drum hit, but it can also be used in double bass drum parts to simulate different feet.

- The handedness is also useful with the hi-hat and ride cymbal to make it groovy and human by adding accents in the right places. For example, right-handedness to the 8th beat and left-handedness to the 4th beat.

- The presets are made to speed up the editing process, even though they are based on the feel of a well-known 80s metal drummer, they just are a good basis for editing.

- In presets "Tom" setting are made for fills, preset works well in snare fills also.

Original Repository: https://github.com/rutjake/groover/
