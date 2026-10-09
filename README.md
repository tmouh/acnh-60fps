# ACNH 60 FPS + SpeedFix

Animal Crossing: New Horizons 60 FPS patch with **normal game speed** for versions 3.0.0 to 3.0.3.

Downloads: [GameBanana](https://gamebanana.com/mods/722295). Sources: GitHub.

## The problem

The internal game logic is timed by FPS, not seconds. Nintendo never intended for anything other than 30 FPS for the vanilla game, so everything happens/moves too quickly when increasing the frame rate. Run it at 60 FPS instead of 30 and everything happens twice as fast: walking, text, animations, villagers, weather, effects.

## The fix

- **60 FPS patch:** lets the game run at 60.
- **SpeedFix:** puts the game back at normal speed. It manually halves the per-frame speeds and doubles the frame-counted timers in the game's parameter file, and patches the code that counts frames (text, animations, camera, effects, villagers, fishing and more).

The result is a smoother picture at the pace of the normal game.

Built from scratch for this project: the 60 FPS patch, the SpeedFix code patch and the parameter changes were all made from the game's own files. No other mod's files are included.

<!-- counts -->
**In numbers:** the SpeedFix rescales 1,428 values in the game's parameter file, 107 values in three villager data files and 5,836 code patches.

## How it was made

I used multiple expensive Claude Code subscriptions to fan out agents operating emulators and running tests. I personally tested the mod on a real V1 2017 modded Switch and held 60 FPS at clocks (1785/844/1600), finding that most stress was on the CPU, with my top core at about 91-92% usage.

- **Side-by-side testing:** Two copies of the game ran together in emulators, the normal game and the mod, from the same save with the same scripted button presses. For every single update, the agent read each game's state from memory and timed actions to the frame.
- **Finding what counts frames:** Turning around while running skipped the skidding animation and instead played a normal walking animation at 60 FPS, making it look very odd. This is because the game picks animations by how far you moved in one frame, which halves at 60 FPS without adjustment. The agent pulled the animation data out of the game, rebuilt that choice in a small model that matched the measurements frame for frame, and fixed it with one change.
- **Checking its own footage:** While cutting the comparison video, the agent went through the clips frame by frame and caught a small difference I hadn't noticed while testing. It saw the clock and minimap come back about 0.4 s early after an axe swing and traced this to fixed frame counts in the game's HUD code (15 frames after an action, 30 after walking), doubled them, and brought the gap down to about 0.1 s.

## Do these or it won't play right

**Emulators**

- **Windows: set the emulator to High priority every time you start it** (Task Manager > Details > right-click the emulator > Set priority > High). Windows doesn't remember the change; at Normal priority the game can drop frames even on a fast PC. Or use a [High priority shortcut](#high-priority-shortcut).
- **Set the emulator speed for your version** (each emulator step by step: [Emulator setup](#emulator-setup)):

**IMPORTANT**
**Ryujinx**: **Options > Settings > System**; scroll down to Hacks and tick **Enable Custom Refresh Rate (Experimental)**, then scroll back up, set **VSync** to **Custom Refresh Rate** and drag **Custom Refresh Rate %** to **200 %** (not 120: the slider is a percentage, and 200 % is 120 FPS). 
**Citron and Eden**: **Emulation > Configure > System**, **Limit Speed Percent 200 %**. For 45 and 60 FPS, use Ryujinx VSync mode Switch or Citron/Eden speed limit 100 %.

**120 FPS needs a PC that holds a steady 120.** Below that, the game slows down; use 60 if your PC cannot hold 120. 

**Switch**

- **sys-clk must be running with a profile for this game, and handheld needs a full-power charger.** Clocks and chargers: see [Switch setup](#switch-setup).
- **Docked at 1080p, 60 FPS holds about 45.** Use the 45 FPS version there, or force handheld mode (see [Switch setup](#switch-setup)).

**Switch and emulators**

- **Game:** versions 3.0.0 to 3.0.3. Older versions don't work, the game can run too slow or freeze.
- **Back up your save first** (JKSV or Checkpoint).
- **Download ONE version, and the right file for your device**, from the [GameBanana page](https://gamebanana.com/mods/722295) (Files section): on an emulator the emulator file, on a Switch the Switch file. Keep only one version installed: they change the same parts of the game.
- **Turn off every other 60 FPS or frame-rate mod, cheat or tool**, including FPSLocker.

## Emulator setup

The emulator files are `60fps-emulator-speedfix-v1-4-0-acnh.zip`, `45fps-emulator-speedfix-v1-4-0-acnh.zip` and `120fps-emulator-speedfix-v1-4-0-acnh.zip`. Copy your version's folder whole: it must directly contain both `exefs` and `romfs`. With only one of them the game runs at the wrong speed. The pack and Bcsv files must all come from the version you play.

### Windows

- **AMD dual-die X3D CPUs:** in Task Manager > Details, right-click the emulator > Set affinity, and keep only the first half of the CPUs (the V-cache die).

#### High priority shortcut

To start the emulator at High priority every time: right-click its desktop shortcut, choose **Properties**, and in **Target** put `cmd.exe /c start "" /high` in front of the existing path, keeping its quotes. Example: `cmd.exe /c start "" /high "C:\Emulators\Ryujinx.exe"`. Optional: set **Run** to Minimized to keep the command window out of the way, and use **Change Icon** to get the emulator's icon back.

### Ryujinx

1. Download the emulator file of your version.
2. Right-click the game > **Open Mods Directory**.
3. Copy the `ACNH 60 FPS + SpeedFix` folder from the zip (inside `mods/contents/01006F8002326000/`) into it (or 45/120 if you download those versions).
4. Right-click the game > **Manage Mods** and make sure it is enabled. Keep only one version enabled.
5. **Speed:**
   - **45 or 60 FPS:** **Options > Settings > System**, VSync Switch (the default).
   - **120 FPS:** Custom Refresh Rate % at **200 %**, step by step under **IMPORTANT** in [Do these or it won't play right](#do-these-or-it-wont-play-right).
   - F1, or clicking VSync in the bar at the bottom of the window, changes the VSync mode. If the speed is wrong, check it is back on Switch (Custom Refresh Rate for 120).

### Citron

1. Download the emulator file of your version.
2. Right-click the game > **Open Mod Data Location**.
3. Copy the `ACNH 60 FPS + SpeedFix` folder from the zip into it (or 45/120 if you download those versions). Copy that folder itself, not the `mods` folder: Citron looks for `exefs` and `romfs` at most one folder down.
4. Right-click the game > **Properties** > **Add-Ons** and make sure it is ticked. Keep only one version ticked.
5. **Speed:** **Emulation > Configure > System**, Limit Speed Percent **100 %** (the default) for 45 or 60 FPS, **200 %** for 120 FPS. Ctrl+U, or Home+Y on a controller, turns the frame-rate limit off and the game runs too fast.

### Eden

1. Download the emulator file of your version.
2. Right-click the game > **Open Mod Data Location**.
3. Copy the `ACNH 60 FPS + SpeedFix` folder from the zip into it (or 45/120 if you download those versions), so it directly contains `exefs` and `romfs`. Keep only one version there.
4. **Speed:** **Emulation > Configure > System**, Limit Speed Percent **100 %** (the default) for 45 or 60 FPS, **200 %** for 120 FPS. Ctrl+U, or Home+Y on a controller, turns the frame-rate limit off and the game runs too fast. Eden also has a Turbo speed mode (Ctrl+Z, 200 % by default) that makes any game run 2x, so keep it off.

### Astris (Apple silicon Mac, 45 and 60 FPS)

1. Unzip the emulator file.
2. Right-click the game > **Manage Mods**.
3. Click **Add** and choose the `ACNH 60 FPS + SpeedFix` folder (or 45) from inside `mods/contents/01006F8002326000/`.
4. Make sure it is enabled, and keep only one version enabled.
5. **Speed:** keep VSync on (the default).

**Updating from an earlier version (emulators):** copy the new version's folder over the old one and let it replace everything.

## Switch setup

You need Atmosphere custom firmware and sys-clk. An FPS counter (Status Monitor overlay, needs SaltyNX) helps for the first session.

1. Download the Switch file of your version (60 or 45 FPS; 120 FPS has no Switch file): `60fps-switch-speedfix-v1-4-0-acnh.zip` or `45fps-switch-speedfix-v1-4-0-acnh.zip`.
2. Copy its `atmosphere` folder to the root of your SD card.
3. Set a sys-clk profile for this game with the clocks below. sys-clk must be running with this profile while you play.

Reference clock readings from one 2017 Switch, not recommendations for every Switch:

| Version | How you play | CPU | GPU | Memory | Result |
|---|---|---|---|---|---|
| 60 FPS | Handheld on the charger | 1785 MHz | 844 MHz | 1600 MHz | held 60 FPS |
| 45 FPS | Handheld on the charger | 1428 MHz | 768 MHz | 1331 MHz | held 45 FPS |
| 45 FPS | Docked at 1080p | 1428 MHz | 844 or 921 MHz | 1600 MHz | both held 43 FPS or more in the busiest spots, with the battery charging |

In the docked test, 844 ran the GPU near its limit and charged faster; 921 gave the GPU headroom and charged more slowly.

**Handheld:** play on a full-power charger (Nintendo's adapter or a 15 V USB-C PD charger). A low-power USB charger caps the GPU at 768 MHz and the battery may drain. On battery it does not hold 60, from the moment you unplug: remove the mod for battery play.

**Docked at 1080p:** 60 FPS holds about 45, even at maximum clocks. Either use the 45 FPS version, or use the 60 FPS version and force handheld mode while docked with ReverseNX-RT (needs SaltyNX) to achieve 720p holding 60.

**45 FPS on a 60 Hz screen:** Nintendo Switch has a 60 Hz screen. On a 60 Hz screen, 45 FPS cannot display perfectly evenly, so it has a small stutter effect on Switch: it's recommended docked on a TV/monitor.

**FPS counter at 45 FPS:** read the **PFPS** line of Status Monitor: it shows 45. The **FPS** line jumps between about 43 and 47 even when the game holds 45.

**Do not use FPSLocker with this mod.**

**Fan:** at these clocks the stock fan runs near full speed, which is loud. NX-FanControl can set a quieter curve, but it means higher temperatures.

**To remove (Switch):** delete all of these together (removing only some runs the game at the wrong speed):

- `atmosphere/exefs_patches/ACNH_60FPS_SpeedFix` (45 FPS: `ACNH_45FPS_SpeedFix`)
- `atmosphere/contents/01006F8002326000/romfs/Pack/StaticParam.pack`
- `atmosphere/contents/01006F8002326000/romfs/Bcsv/ItemNpcFtrActionParam.bcsv`
- `atmosphere/contents/01006F8002326000/romfs/Bcsv/ItemNpcWherearenFtrActionParam.bcsv`
- `atmosphere/contents/01006F8002326000/romfs/Bcsv/NpcInterest.bcsv`

**Switching between 60 and 45 (Switch):** install one version at a time. Delete the other version's folder in `atmosphere/exefs_patches` first, then copy the new `atmosphere` folder and let it replace `StaticParam.pack` and the three `romfs/Bcsv/` files listed above. The pack and Bcsv files must all come from the version you play.

**Updating from an earlier version (Switch):** remove the previous frame-rate patch folder from `atmosphere/exefs_patches/`, then copy the new `atmosphere` folder over the old one and let it replace everything.

## Too fast or too slow

The game should play at the pace of the normal game. If it does not:

- **Wrong file:** emulators need the emulator file. The Switch file does nothing useful in an emulator.
- **Partial copy:** see [Emulator setup](#emulator-setup) (the folder must directly contain both `exefs` and `romfs`). On Switch, all paths under To remove in [Switch setup](#switch-setup) must be there.
- **Emulator speed:** check the Speed step for your emulator in [Emulator setup](#emulator-setup). The FPS counter cannot tell you: Citron shows 60 FPS both when the game runs at normal speed and when it runs twice as fast.
- **Capable computer being too slow:** set the emulator to High priority, every time you start it (see [Do these or it won't play right](#do-these-or-it-wont-play-right)).
- **Computer not fast enough:** if the FPS counter stays below your version's frame rate, the game runs slower to match. Which version to try: [Emulator setup](#emulator-setup).
- **Another 60 FPS mod or cheat:** turn it off (see [Other mods](#other-mods)).
- **More than one version installed:** keep only one version: 45, 60 or 120 FPS.
- **Wrong game version:** only 3.0.0 to 3.0.3 work.
- **Switch:** check [Switch setup](#switch-setup) (sys-clk running, charger, docked at 1080p).

## Other mods

Works alongside mods that replace models, textures or music.

Conflicts:

- Any other 60 FPS or frame-rate mod, cheat or tool.
- Any mod that includes its own `romfs/Pack/StaticParam.pack`. Only one copy can load, so one of the two mods stops working. The same applies to `romfs/Bcsv/ItemNpcFtrActionParam.bcsv`, `romfs/Bcsv/ItemNpcWherearenFtrActionParam.bcsv` and `romfs/Bcsv/NpcInterest.bcsv`.

This mod needs no ResourceSizeTable file. If your other mods need one, use one made for 3.0.3; older ones can crash the game or hide objects.

## Known issues

- Any game update breaks it. If ACNH ever happens to receive a new update down the line, an update for the mod will be released shortly.
- On the 2017 Switch, a very full island can dip below 60 FPS in the evening even at maximum clocks (the CPU is the limit), and the game slows slightly for those moments. Islands differ.

This repo holds the sources: the code patches for 45, 60 and 120 FPS, the parameter-file patches (`pack/StaticParam.pack.ips`, `pack45/StaticParam45.pack.ips` and `pack120/StaticParam120.pack.ips`, applied to the game's own `romfs/Pack/StaticParam.pack`), the three `romfs/Bcsv/` villager data files for each rate, and the tools that build the zips. The ready-made pack and the matching three `romfs/Bcsv/` files are in each zip. How the patches work and how to build the files yourself: [docs/how-it-works.md](https://github.com/tmouh/acnh-60fps/blob/main/docs/how-it-works.md). Measurements: [docs/measured.md](https://github.com/tmouh/acnh-60fps/blob/main/docs/measured.md) (60 FPS) and [docs/measured-45.md](https://github.com/tmouh/acnh-60fps/blob/main/docs/measured-45.md) (45 FPS).

## What's new

**v1.4.0:** more of the game is back at its normal pace at 45, 60 and 120 FPS:

- **Insects:** butterflies, moths, bees, dragonflies, cicadas, fireflies, mosquitoes and other fliers bob, wander, hover, turn and land at their normal pace, and moths no longer fly twice as fast. Grasshoppers and crickets hop at their normal rhythm. Beetles and other ground bugs, tarantulas, scorpions, wasps and mantises move, pause, rear up, chase and escape at their normal pace. Pond skaters and diving beetles glide their normal distance, and fleeing insects no longer get away faster than normal.
- **Fishing:** fish turn and steer toward the float at their normal pace, a hooked fish pulls, leans and wobbles at the normal pace while you reel it in, and near a waterfall the float drifts at the normal speed. Caught bugs and fish rise into the catch pose at their normal pace.
- **Museum:** aquarium fish that swim against the current stay inside their area again, and insects flutter and hover at their normal pace.
- **Your character:** steps into position at the normal pace when starting actions such as fishing, digging or pushing furniture. Timed actions such as swinging the net, opening chests, emotes and the megaphone no longer end early. Waking up from dozing off, getting out of a pitfall by mashing buttons and gliding after jumping into the sea are back to normal.
- **World:** rain, snow and falling leaves blow sideways at the normal speed in the wind. Doors, buildings and warps fade out and in for their normal length, and the music fades out at its normal pace. Snowballs roll and grow at their normal pace.

**v1.3.1:** fish behave like in the normal game again at 45, 60 and 120 FPS: they swim away when you run up to them and dart off at the normal speed when they get away.

**v1.3.0:** Adds 120 FPS for emulators, plus villager behaviour and timing fixes at 45, 60 and 120 FPS. The goal is the same: smoother animation, normal game pace, and maintaining the snappy menu navigation and camera response inherent to FPS increases.

## License

ACNH 60 FPS + SpeedFix © 2026 tmouh, licensed under [CC BY-NC 4.0](https://creativecommons.org/licenses/by-nc/4.0/) (full text in [LICENSE](LICENSE)).

- **Credit:** if you share this mod, or anything made from it, name "ACNH 60 FPS + SpeedFix by tmouh" and link https://gamebanana.com/mods/722295. If you changed it, say so.
- **No commercial use.**

`StaticParam.pack` in the GameBanana zips is modified game data and remains Nintendo's; the license covers the patches, tools and documentation.
