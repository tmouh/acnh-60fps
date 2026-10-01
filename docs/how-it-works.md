# How it works

## Why plain 60 FPS runs the game at double speed

Animal Crossing: New Horizons updates its world once per frame. Movement speeds, timers, gravity, animation steps and text printing are all written as "per update" amounts tuned for 30 updates a second. Unlock 60 FPS and every one of them is applied twice as often, so the whole game runs twice as fast.

There is no single global speed setting to turn down. The fix is to rescale every per-update amount the game uses, one system at a time.

## The three parts

**1. 60 FPS enabler** (`enabler_sdk.pchtxt`)
- One line in the game's SDK module (`sdk`): present a frame on every display refresh instead of every second one. This module is the same in 3.0.0 to 3.0.3, so one file serves all four.

**2. Parameter file** (`romfs/Pack/StaticParam.pack`)
- The game keeps most tuning values in this file: player movement, cameras, insects, fish, villager activity, weather and water.
- 1,323 values in 100 files are rescaled, each in place: same file size, same structure.
- Full list: [parameters.md](parameters.md) and [parameters.csv](parameters.csv).

**3. SpeedFix code patches** (`speedfix_main.pchtxt` for 3.0.3; `speedfix_main_302.pchtxt`, `speedfix_main_301.pchtxt` and `speedfix_main_300.pchtxt` for 3.0.2, 3.0.1 and 3.0.0: the same changes at each version's addresses)
- About 770 code and data patches (4-byte words) for places where the speed is fixed in code rather than in the parameter file, such as:
  - literal frame rates (30 per second, 1/30 s)
  - fixed update counts
  - per-update physics
- Covers, among others: the default animation step of models, dialogue text and the villager voices, the UI animation clock, particle effects, hops, the vaulting pole, warp pipes, the camera, villager wait timers (also in shops, the museum and Happy Home Paradise), fishing, items falling from trees, holding a direction in menus and keyboards, the HUD hiding and returning around actions, chat balloons and the timer display, K.K. Slider concerts, turning and skidding while running, river ripples and foam, walking through doors, fruit swaying on trees, the autosave icon, light flicker, and the fishing bite window.
- Each patch group has a one-line comment saying what it changes.

## The rules

Every rescaled value follows one of these rules, chosen so the result per second matches the 30 FPS game:

| What the value is | Rule | Why |
|---|---|---|
| Speed (distance or angle per update) | x 1/2 | applied twice as often |
| Acceleration, gravity | x 1/4 | a change to a per-update speed, applied twice as often: 1/2 x 1/2 |
| Count of updates (timers, durations) | x 2 | twice as many updates per second |
| Smoothing rate r (move r of the remaining gap each update) | 1 - sqrt(1 - r) | two new steps close the same share of the gap as one old step |
| Per-update decay k | sqrt(k) | two new steps equal one old step |
| Literal 30 frames per second, 1/30 s | 60, 1/60 | direct conversion |
| A per-update distance that another system reads as a speed (for example to pick an animation) | x 2 | the reader's thresholds expect the 30 FPS amount |

## How it was checked

The unmodified game and the modded game ran side by side on PC, from the same save, with the same scripted button presses. Each action was timed from the game's own state, read from memory about every 8 ms; the few rows marked "on screen" in measured.md were timed from recorded frames of the screen. Results: [measured.md](measured.md).

## Limits

- Game speed still follows the frame rate: below 60 FPS the game slows down in step.
- A few actions remain a fraction of a second off (listed in measured.md).
- The patches only fit versions 3.0.0 to 3.0.3. Each SpeedFix file starts with the main build it fits (3.0.3 `FF1D1C05670DB6021C85B624A710B963`, 3.0.2 `FCD2BB238ABE99E925B4E452DF1F41F1`, 3.0.1 `8F2CB7A9774959C89189C994FE4CC988`, 3.0.0 `5D913CF71EB24CB22C5105B1FA3EFD97`), and emulators and Atmosphere load only the matching one.

## Building the files yourself

- **Switch patches:** `python tools/pchtxt_to_ips.py <file.pchtxt> <out folder>` turns each patch text into the `.ips` Atmosphere loads.
- **Parameter file:** `python tools/apply_ips.py pack/StaticParam.pack.ips <your StaticParam.pack> <output>` builds the modified file from your own dump of 3.0.0, 3.0.1, 3.0.2 or 3.0.3 (the file is the same in all four). It refuses any other file.
