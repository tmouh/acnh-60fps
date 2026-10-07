# How it works

## Why plain 60 FPS runs the game at double speed

Animal Crossing: New Horizons updates its world once per frame. Movement speeds, timers, gravity, animation steps and text printing are all written as "per update" amounts tuned for 30 updates a second. Unlock 60 FPS and every one of them is applied twice as often, so the whole game runs twice as fast.

There is no single global speed setting to turn down. The fix is to rescale every per-update amount the game uses, one system at a time.

## The three parts

**1. 60 FPS enabler** (`enabler_sdk.pchtxt`)
- One line in the game's SDK module (`sdk`): present a frame on every display refresh instead of every second one. This module is the same in 3.0.0 to 3.0.3, so one file serves all four.

**2. Parameter file** (`romfs/Pack/StaticParam.pack`)
- The game keeps most tuning values in this file: player movement, cameras, insects, fish, villager activity, weather and water.
- 1,345 values in 104 files are rescaled, each in place: same file size, same structure.
- Parameter list: [parameters.md](parameters.md) and [parameters.csv](parameters.csv).
- Each rate also includes `romfs/Bcsv/ItemNpcFtrActionParam.bcsv`, `romfs/Bcsv/ItemNpcWherearenFtrActionParam.bcsv` and `romfs/Bcsv/NpcInterest.bcsv`, rescaled for villager activity and wait timers (107 values); 45 and 60 ship for Switch and emulators, 120 for emulators.

**3. SpeedFix code patches** (`speedfix_main.pchtxt` for 3.0.3; `speedfix_main_302.pchtxt`, `speedfix_main_301.pchtxt` and `speedfix_main_300.pchtxt` for 3.0.2, 3.0.1 and 3.0.0: the same changes at each version's addresses)
- 3,761 code and data patches (4-byte words) for places where the speed is fixed in code rather than in the parameter file, such as:
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

The unmodified game and the modded game ran side by side in emulators, from the same save, with the same scripted button presses. Each action was timed from the game's own state, read from memory about every 8 ms; the few rows marked "on screen" in measured.md were timed from recorded frames of the screen. Results: [measured.md](measured.md).

## Limits

- Game speed still follows the frame rate: below 60 FPS the game slows down in step.
- A few actions remain a fraction of a second off (listed in measured.md).
- The patches only fit versions 3.0.0 to 3.0.3. Each SpeedFix file starts with the main build it fits (3.0.3 `FF1D1C05670DB6021C85B624A710B963`, 3.0.2 `FCD2BB238ABE99E925B4E452DF1F41F1`, 3.0.1 `8F2CB7A9774959C89189C994FE4CC988`, 3.0.0 `5D913CF71EB24CB22C5105B1FA3EFD97`), and emulators and Atmosphere load only the matching one.

## The 45 FPS version

The 45 FPS version uses the same approach with a factor of 1.5 instead of 2: every per-update amount is rescaled so that 45 updates a second do what 30 did.

### The rules at 45

| What the value is | Rule at 60 | Rule at 45 |
|---|---|---|
| Speed (distance or angle per update) | x 1/2 | x 2/3 |
| Acceleration, gravity | x 1/4 | x 4/9 |
| Count of updates (timers, durations) | x 2 | x 1.5 |
| Smoothing rate r | 1 - sqrt(1 - r) | 1 - (1 - r)^(2/3) |
| Per-update decay k | sqrt(k) | k^(2/3) |
| Literal 30 frames per second, 1/30 s | 60, 1/60 | 45, 1/45 |

A count of updates times 1.5 is not always a whole number (7 updates become 10.5). The game counts whole updates, so these are rounded:

- A wait that answers a button press (cursor repeats, menu and button waits) rounds down, to the faster side.
- Everything else (animations, walking, the world and physics) rounds to the nearest whole update, and a half rounds up.

Each rounded value is off by at most half an update at 45 FPS (0.011 s).

### The three parts at 45

**1. 45 FPS cadence** (the first section of each 45 FPS patch file, `speedfix45_main.pchtxt` and its 3.0.0 to 3.0.2 versions)
- 45 frames a second can't be shown evenly on a 60 Hz screen, so the patch shows them in a steady 1, 1, 2 rhythm: each frame stays on screen for one, one, then two refreshes. Three frames take four refreshes: 45 frames per second.
- It sits in the game's main module, not in the SDK module. In the game's present routine, a call before each frame is queued sets the frame's present interval (1, 1, then 2) through the game's own graphics call `nvnWindowSetPresentInterval`.
- 26 code words: two hooks (the present routine exists in two identical copies) and a short routine in unused space.
- It carries none of the 60 FPS version's SDK change, so it only touches this game's own code. That is also why the two versions must not be installed together: the 60 FPS SDK change would force every frame to one refresh.
- On emulators it works at normal speed settings (Ryujinx VSync mode Switch, Citron and Eden at speed limit 100 %; Astris VSync on).

**2. Parameter file** (`romfs/Pack/StaticParam.pack`)
- 1,344 parameter values and the same 107 villager-data values are rescaled with the 45 rules. Same file size, same structure.
- The tool that builds it takes the factor as an input: with a factor of 2 it rebuilds the 60 FPS version's file byte for byte.

**3. SpeedFix code patches** (the rest of `speedfix45_main.pchtxt` for 3.0.3 and `speedfix45_main_302.pchtxt`, `_301`, `_300` for the older versions; on Switch, one `.ips` per game version)
- 4,251 code and data words (including the 26-word 45 FPS cadence) rescale the game for 45 FPS; menu navigation and camera response keep their snappy feel.
- Most words are the 60 FPS version's patches with the 45 rules applied. One tool generates them from the factor: with a factor of 2 it reproduces the 60 FPS version's generated words bit for bit.
- Where an instruction can't hold the 45 value (some float constants and fixed-point frame-count conversions), the value moves to a new constant or a short routine in unused space.

### What was converted by hand

Some of the 60 FPS version's code changes are built around exactly 2, so a factor of 1.5 doesn't fit them: "only on every second update" checks, a frame count added to itself, one-update hand-offs. These were rewritten by hand, one system at a time, and each was checked by a separate review before it went in:

- dialogue windows and menus;
- player actions (pockets, tools, warp pipes);
- villagers, events, K.K. Slider concerts and the house cameras;
- river ripples and foam, aquarium fish, wind;
- projectiles, jumps and creatures (insects, fish).

Later test rounds against the normal game found a few more places, which were fixed the same way (villager timers, sitting down on a seat, the save-and-end messages).

### How the 45 FPS version was checked

The same way as the 60 FPS version: the normal game and the 45 FPS version ran side by side in emulators, from the same save, with the same scripted button presses, and each action was timed from the game's own state. Most actions were measured on the 45 FPS version's release files; the others on test builds whose patches for that action are the same. Results: [measured-45.md](measured-45.md). On a real Switch the frame rate and the game speed were checked by hand (an FPS overlay and the Timer item's banner).

### Limits at 45

- Game speed follows the frame rate: below 45 FPS the game slows down in step.
- The patches only fit versions 3.0.0 to 3.0.3, like the 60 FPS version.

## The 120 FPS version

The emulator-only 120 FPS version uses a factor of 4: speeds are divided by 4, acceleration by 16, and update-counted timers multiplied by 4. Its frame-rate and SpeedFix code (3,924 code and data words, 1,345 parameter values, the same 107 villager-data values) is in `speedfix120_main*.pchtxt`, its parameter patch is `pack120/StaticParam120.pack.ips`, and its three `romfs/Bcsv/` files match the 120 rate. It needs a PC that holds a steady 120; below that, the game slows down, so use 60.

## Building the files yourself

- **Switch patches:** `python tools/pchtxt_to_ips.py <file.pchtxt> <out folder>` turns each patch text into the `.ips` Atmosphere loads.
- **Parameter file:** `python tools/apply_ips.py pack/StaticParam.pack.ips <your StaticParam.pack> <output>` builds the modified file from your own dump of 3.0.0, 3.0.1, 3.0.2 or 3.0.3 (the file is the same in all four). It refuses any other file.
- **45 FPS version:** the same two commands: `pchtxt_to_ips.py` on each 45 FPS patch file (one per game version; the 45 FPS cadence is inside them), and `apply_ips.py` with the 45 FPS version's parameter-file patch (`pack45/StaticParam45.pack.ips`).
- **120 FPS version (emulators):** use the `speedfix120_main*.pchtxt` files directly in the mod's `exefs` folder, and `python tools/apply_ips.py pack120/StaticParam120.pack.ips <your StaticParam.pack> <output>` to build `romfs/Pack/StaticParam.pack`. Copy the 120 version's three `romfs/Bcsv/` files alongside it.
- **Villager data files:** for 45 or 60 FPS, copy the matching three `romfs/Bcsv/` files from that rate's emulator (`ryujinx/`) or Switch (`switch45/`, `switch60/`) sources. Use the same rate as the code and parameter patches.
