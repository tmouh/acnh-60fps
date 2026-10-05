# 45 FPS version: measured against the unmodified game

The normal game (30 FPS) and the 45 FPS version ran side by side in Ryujinx, from the same save and with the same button presses. Each time runs from the moment the game starts an action to the moment it ends it, read from the game's own state about every 8 ms (rows marked "on screen" were timed from recorded frames of the screen). Rows were measured on the 45 FPS version's release files or on the test builds leading up to them.

| Action | Normal game (30 FPS) | 45 FPS version | Difference |
|---|---|---|---|
| Frame rate (game updates per second) | 30.00 | 45.00 | frames shown 16.7, 16.7, 33.3 ms apart |
| Walking speed (stick fully tilted) | 1.000 | 1.005 | +0.5% |
| Shaking a tree | 0.90 s | 0.91 s | +0.01 s |
| Digging a hole / filling it | 1.13 / 1.40 s | 1.11 / 1.40 s | −0.02 / 0.00 s |
| Swinging the net | 0.93 s | 0.91 s | −0.02 s |
| Swinging the axe at nothing | 1.20 s | 1.20 s | 0.00 s |
| Chopping a tree (one hit) | 0.77 s | 0.78 s | +0.01 s |
| Watering (one pour) | 3.87 s | 3.87 s | 0.00 s |
| Taking out / putting away a tool | 0.87 / 0.90 s | 0.90 / 0.91 s | +0.03 / +0.01 s |
| Hopping over a hole / vaulting over a river | 0.83 / 1.50 s | 0.84 / 1.51 s | +0.01 / +0.01 s |
| Hitting a rock with the shovel / the axe: the bounce back | 0.87 / 1.07 s | 0.89 / 1.09 s | +0.02 / +0.02 s |
| Wading into the sea / climbing out (wet suit) | 2.20 / 2.40 s | 2.20 / 2.38 s | 0.00 / −0.02 s |
| Diving / coming back up | 2.13 / 1.87 s | 2.13 / 1.87 s | 0.00 / 0.00 s |
| Warp pipe: jumping in, until the next scene / whole trip | 2.97 / 6.23 s | 2.98 / 6.21 s | +0.01 / −0.02 s |
| Walking into / out of a building, the door part | 2.20 / 2.03 s | 2.20 / 2.02 s | 0.00 / −0.01 s |
| Reeling in the line without a bite | 1.03 s | 1.04 s | +0.01 s |
| Villagers' pauses between actions (set to 2, 3, 4 or 5 s) | set length ±0.02 s | set length ±0.02 s | 0.00 s |
| Dialogue: the old page cleared after pressing A (on screen) | 0.25 s | 0.27 s | +0.02 s |
| Dialogue: next page, first letter after pressing A | 0.13 s | 0.13 s | 0.00 s |
| Holding a direction in a menu list: first repeat / then every | 0.333 / 0.133 s | 0.333 / 0.133 s | 0.00 s |
| Nook Phone app grid, holding a direction | 5 moves per second | 5 moves per second | 0 |
| Keyboard cursor, holding a direction: moves at | 0, 0.333, 0.467, 0.600 s | 0, 0.333, 0.467, 0.600 s | 0.00 s |
| Custom design editor cursor: first repeat / then every | 0.200 / 0.100 s | 0.200 / 0.089 s | 0.00 / −0.011 s ¹ |
| Pockets: closing with B / dropping an item | 0.36 / 0.23 s | 0.35 / 0.21 s | −0.02 / −0.02 s ² |
| House camera, right stick held: turn speed / first move | 59.9 °/s / 0.016 s | 60.1 °/s / 0.016 s | +0.2% / 0.00 s |
| Timer item: "Time's up!" banner / clock staying on 00:00 (on screen) | 6.74 / 3.07 s | 6.77 / 3.05 s | +0.03 / −0.02 s |
| K.K. Slider concert: the two camera moves / the slow orbit between them | 12.53 and 7.17 s / 6.0° per second | 12.53 and 7.17 s / 6.0° per second | 0.00 |
| K.K. Slider's first concert: the villagers' applause | 4.0 s | 4.0 s | 0.00 s |
| River ripples under a standing player | one every 0.333 s | one every 0.333 s | 0 |

- One frame of the normal game lasts 0.033 s. Every difference above is about one frame or less.
- Values are averages of 1 to 10 tries per game; where only a range was recorded, the range is shown.
- ¹ Faster on purpose: the 45 FPS version can only repeat every 0.089 s or every 0.111 s here, and the faster one keeps the editor as quick as the rest of the controls.
- ² Waits that answer a button press round to the faster side when 45 FPS can't hit the normal time exactly.
- Citron (stable 2026.04.18) and Eden (v0.2.1) with the 45 FPS version's emulator files on game 3.0.3: the game ran at 45.0 FPS, and the moving arrow on the title screen kept the normal game's pace (0.998 of it). With the 45 FPS version's emulator download on game versions 3.0.0, 3.0.1 and 3.0.2, Ryujinx, Citron and Eden also ran at about 45.0 FPS with the title-screen arrow at 0.998 of the normal pace. These checks cover loading, frame rate and intro pace; they do not repeat every action in the table on each emulator and version.
- Astris 1.0.29 on one M2 Mac, game version 3.0.3: the 45 and 60 FPS emulator downloads passed a hand test. The reported pace was normal; no timed measurements were taken on Astris. This does not establish performance on other Macs.
- On a real Switch (2017 model, handheld on the charger, an earlier test build), the Timer item's "Timer started!" banner stayed on screen 7 s by a phone stopwatch, the same as the normal game.
- Measured in an emulator. The Switch runs the same files, but these timings hold only while the game keeps a steady 45 FPS.

