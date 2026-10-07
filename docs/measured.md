# Measured against the unmodified game

The normal game (30 FPS) and this mod (60 FPS) ran side by side in Ryujinx, from the same save and with the same button presses. Each time runs from the moment the game starts an action to the moment it ends it, read from the game's own state about every 8 ms (rows marked "on screen" were timed from recorded frames of the screen). Rows were measured on the 60 FPS version's release files or on the test builds leading up to them.

| Action | Normal game (30 FPS) | This mod (60 FPS) | Difference |
|---|---|---|---|
| Walking (stick fully tilted) / running (B held), speed | 3.74 / 5.38 tiles/s | 3.75 / 5.37 tiles/s | +0.2% / −0.05% |
| One page of dialogue at normal text speed (text prints 36 letters a second in both) | 2.93 s and 3.14 s | 2.91 s and 3.12 s | −0.02 s |
| Shaking a tree | 0.90 s | 0.90 s | 0.00 s |
| Digging a hole | 1.07–1.13 s | 1.07–1.11 s | within 0.02 s |
| Swinging the net | 0.93 s | 0.93 s | 0.00 s |
| Chopping a tree (one hit) | 0.77 s | 0.77 s | 0.00 s |
| Watering (one pour) | 3.86 s | 3.86 s | 0.00 s |
| Taking out a tool from the tool ring | 0.87 s | 0.88 s | +0.02 s |
| Hopping over a hole / vaulting over a river | 0.83 / 1.50 s | 0.83 / 1.50 s | 0.00 / 0.00 s |
| Wading into the sea / climbing out (wet suit) | 2.20 / 2.40 s | 2.20 / 2.38 s | 0.00 / −0.02 s |
| Opening / closing the pockets (on screen) | 0.26 / 0.42 s | 0.23 / 0.41 s | −0.03 / −0.01 s ¹ |
| Villagers' one-second pauses between actions | 1.02–1.04 s | 1.00–1.02 s | −0.02 s |
| Timer item: each countdown step / the result balloon after "Time's up!" (on screen) | 1.000 / 10.08–10.13 s | 1.000 / 10.13–10.15 s | 0.00 / +0.03 s |
| Dialogue: the old page cleared after pressing A (on screen) | 0.23–0.25 s | 0.27 s | +0.02 s |
| Holding a direction in a menu list: first repeat / then every | 0.333 / 0.133 s | 0.333 / 0.133 s | 0.00 s |
| Keyboard: cursor repeat / characters deleted per second with B held | 0.333 / 0.133 s, 6 | 0.333 / 0.133 s, 6 | 0.00 s |
| Custom design editor cursor: first repeat / then every | 0.200 / 0.100 s | 0.200 / 0.100 s | 0.00 s |
| Turning around from a walk into a run: sideways swing | 0.19 tiles | 0.19 tiles | 0.00 |
| Skid when reversing while running: length / slide | 0.567 s / 1.14 tiles | 0.567 s / 1.15 tiles | 0.00 s |
| Reeling in the line without a bite | 1.03 s | 1.03–1.07 s | 0.00 to +0.03 s |
| K.K. Slider concert: the two camera moves / the slow orbit between them | 12.53 and 7.17 s / 6.0° per second | 12.53 and 7.17 s / 6.0° per second | 0.00 |
| K.K. Slider's first concert: the villagers' applause | 4.0 s | 4.0 s | 0.00 s |
| Warp pipe, whole trip | 6.27 s | 6.17 s | −0.10 s ² |
| Casting the fishing rod | 1.97 s | 2.03 s | +0.06 s |
| Releasing a caught creature (sea bass / sea star) | 2.07 / 1.73 s | 1.86 / 1.67 s | −0.21 / −0.06 s |
| Walking out of a building, after the door | 2.22 s | 2.16 s | −0.06 s |
| Clock / minimap back on screen after stopping a run (on screen) | 1.38 / 1.26 s | 1.27 / 1.20 s | −0.11 / −0.06 s ³ |
| K.K. Slider's first concert, after the song: closing words (on screen) / end of the scene | 9.0 / 20.3 s | 8.8 / 19.7 s | −0.22 / −0.65 s |

- One frame of the normal game lasts 0.033 s. Every difference in the first twenty-two rows is about one frame or less.
- The last six rows are known small differences that remain at 60 FPS.
- Values are averages of 1 to 7 tries per game; where only a range was recorded, the range is shown.
- A tile is one square of the island grid.
- Villagers' random 2–5 s idle pauses also matched their set lengths within 0.02 s in both games.
- ¹ Timed from the screen, accurate to about ±0.05 s. An earlier test build closed the pockets about 0.08 s slower; the latest measurement shows no clear difference.
- ² Across tests the whole trip ran 0.07 to 0.11 s shorter. About 0.06 s of that comes after the press is registered; the rest depends on when the press lands between frames.
- ³ The game asks for the clock and minimap at the same moment in both (0.5 s after an action, 1.0 s after walking); the difference is in how they fade back in. After other actions (axe, vault, shaking a tree) it is 0.05–0.13 s.
- Measured in an emulator. The Switch runs the same files, but these timings hold only while the game keeps a steady 60 FPS.

## Setup readings and notes

The README and the GameBanana page give only what you need to set up. These details used to be on the README and are kept here.

**Switch (one 2017 Switch, V1)**

- The 60 FPS clock reading (CPU 1785 MHz, GPU 844 MHz, memory 1600 MHz, held 60 FPS) was taken on Atmosphere 1.11.2, firmware 22.5.0, handheld on a 15 V USB-C PD charger.
- GPU above 768 MHz needs the dock or a full-power charger.
- On battery the GPU is capped at 460 MHz, which can't hold 60.
- At full fan the SoC is at about 59 °C; a quieter NX-FanControl curve means higher temperatures.
- The 45 FPS version at the Switch's own clocks (sys-clk off, handheld on the charger): the game ran at 40 to 45 FPS and dipped.
- The 45 FPS version in the Status Monitor overlay: the PFPS line shows 45, sometimes 44 or 46 for a moment. The FPS line next to it jumps between about 43 and 47 even when the game holds 45, because it averages the frame times.

**Game speed below the version's frame rate**

Game speed follows the frame rate. With the 60 FPS version at 45 FPS, the game runs about 25% slower; with the 45 FPS version at 43 FPS, about 4% slower.

**Emulators**

- Emulator versions: Ryujinx (Ryubing Canary 1.3.351), Citron (stable 2026.04.18 and nightly 40212aa3e), Eden (v0.2.1).
- Ryujinx: VSync mode Switch, not unlimited or turbo. For the 120 FPS version, Custom Refresh Rate % at 120 % instead of 200 % runs the game slow.
- Ryujinx on Linux or Steam Deck: use the folder that Open Mods Directory opens.
- Citron: when Ctrl+U or Home+Y turns the frame-rate limit off, the status bar shows "(Unlocked)"; the limit resets when you restart the game.
