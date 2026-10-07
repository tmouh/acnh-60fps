# ACNH 60 FPS + SpeedFix

Animal Crossing: New Horizons 60 FPS patch with **normal game speed** for versions 3.0.0 to 3.0.3.

Downloads: [GameBanana](https://gamebanana.com/mods/722295). Sources: GitHub.

## What's new in v1.3.0

Adds 120 FPS for emulators, plus villager behaviour and timing fixes at 45, 60 and 120 FPS. The goal is the same: smoother animation, normal game pace, and maintaining the snappy menu navigation and camera response inherent to FPS increases.

Install one frame-rate version at a time. Choose your download:

- Emulators: `60fps-emulator-speedfix-v1-3-0-acnh.zip`, `45fps-emulator-speedfix-v1-3-0-acnh.zip` or `120fps-emulator-speedfix-v1-3-0-acnh.zip`.
- Switch: `60fps-switch-speedfix-v1-3-0-acnh.zip` or `45fps-switch-speedfix-v1-3-0-acnh.zip`.

Back up your save first. In an emulator, copy the selected `ACNH 45 FPS + SpeedFix`, `ACNH 60 FPS + SpeedFix` or `ACNH 120 FPS + SpeedFix` folder from `mods/contents/01006F8002326000/` into the game's mods folder, and enable only that version. On Switch, remove the previous frame-rate patch folder from `atmosphere/exefs_patches/`, then copy the new zip's `atmosphere` folder to the SD card root, replacing the old mod files.

**120 FPS needs a PC that holds a steady 120.** Below that, the game slows down; use 60 if your PC cannot hold 120. 

**IMPORTANT**
**Ryujinx**: **Options > Settings > System**; scroll down to Hacks and tick **Enable Custom Refresh Rate (Experimental)**, then scroll back up, set **VSync** to **Custom Refresh Rate** and drag **Custom Refresh Rate %** to **200 %** (not 120: the slider is a percentage, and 200 % is 120 FPS). 
**Citron and Eden**: **Emulation > Configure > System**, **Limit Speed Percent 200 %**. For 45 and 60 FPS, use Ryujinx VSync mode Switch or Citron/Eden speed limit 100 %.

**AMD dual-die X3D CPUs:** in Task Manager > Details, right-click the emulator > Set affinity, and keep only the first half of the CPUs (the V-cache die).

## The problem

The internal game logic is timed by FPS, not seconds. Nintendo never intended for anything other than 30 FPS for the vanilla game, so everything happens/moves too quickly when increasing the frame rate. Run it at 60 FPS instead of 30 and everything happens twice as fast: walking, text, animations, villagers, weather, effects.

## The fix

- **60 FPS patch:** lets the game run at 60.
- **SpeedFix:** puts the game back at normal speed. It manually halves the per-frame speeds and doubles the frame-counted timers in the game's parameter file, and patches the code that counts frames (text, animations, camera, effects, villagers, fishing and more).

The result is a smoother picture at the pace of the normal game.

Built from scratch for this project: the 60 FPS patch, the SpeedFix code patch and the parameter changes were all made from the game's own files. No other mod's files are included.

## How it was made

I used multiple expensive Claude Code subscriptions to fan out agents operating emulators and running tests. I personally tested the mod on a real V1 2017 modded Switch and held 60 FPS at clocks (1785/844/1600), finding that most stress was on the CPU, with my top core at about 91-92% usage.

- **Side-by-side testing:** Two copies of the game ran together in emulators, the normal game and the mod, from the same save with the same scripted button presses. For every single update, the agent read each game's state from memory and timed actions to the frame.
- **Finding what counts frames:** Turning around while running skipped the skidding animation and instead played a normal walking animation at 60 FPS, making it look very odd. This is because the game picks animations by how far you moved in one frame, which halves at 60 FPS without adjustment. The agent pulled the animation data out of the game, rebuilt that choice in a small model that matched the measurements frame for frame, and fixed it with one change.
- **Checking its own footage:** While cutting the comparison video, the agent went through the clips frame by frame and caught a small difference I hadn't noticed while testing. It saw the clock and minimap come back about 0.4 s early after an axe swing and traced this to fixed frame counts in the game's HUD code (15 frames after an action, 30 after walking), doubled them, and brought the gap down to about 0.1 s.

## Requirements

**Game:** versions 3.0.0 to 3.0.3. Older versions don't work, the game can run too slow or freeze.

**The game must hold 60 FPS** (the 45 FPS version needs a steady 45; see 45 FPS version). Game speed follows the frame rate: with the 60 FPS version, at 45 FPS it runs about 25% slower.

**Switch:**

- Atmosphere custom firmware.
- sys-clk running with a profile for this game. These clock readings are references from one setup, not recommendations for every Switch. **CPU 1785 MHz, GPU 844 MHz, memory 1600 MHz** held 60 FPS on a 2017 Switch (V1, Atmosphere 1.11.2, firmware 22.5.0), handheld on a 15 V USB-C PD charger.
  - GPU above 768 MHz needs the dock or a full-power charger (Nintendo's adapter or a 15 V USB-C PD charger). A low-power USB charger caps the GPU at 768 and the battery may drain.
  - On battery the GPU is capped at 460 MHz, which can't hold 60. Remove the mod before playing on battery.
- Docked at 1080p the game runs at about 45 FPS, even at maximum clocks. Forcing handheld mode (ReverseNX-RT overlay, needs SaltyNX) gives the TV 720p at 60.
- An FPS counter (Status Monitor overlay, needs SaltyNX) helps for the first session. **Do not use FPSLocker with this mod.**
- At these clocks the stock fan runs near full speed, which is loud. NX-FanControl can set a quieter curve, but it means higher temperatures (about 59 °C SoC at full fan).

**Emulators:** Ryujinx (Ryubing Canary 1.3.351), Citron (stable 2026.04.18 and nightly 40212aa3e) or Eden (v0.2.1) with update 3.0.0 to 3.0.3, on a computer that holds a steady 60 FPS. Try the 60 FPS version first; if your setup can't hold 60, try the 45 FPS version. If it can't hold 45 either, play without the mod. Astris (Apple silicon Mac) is also supported. For 45 and 60 FPS, keep the emulator at normal speed:

- **Windows: set the emulator to High priority every time you start it** (Task Manager > Details > right-click the emulator > Set priority > High). Windows doesn't remember the change; at Normal priority the game can drop frames even on a fast PC. Or use a [High priority shortcut](#high-priority-shortcut).
- Ryujinx: VSync mode Switch (the default), not unlimited or turbo.
- Citron: Limit Speed Percent at 100 % (the default; **Emulation** > **Configure** > **System**). Ctrl+U or Home+Y turns the limit off (status bar shows "(Unlocked)"), which makes the game run too fast; it resets when you restart the game.
- Eden: speed limit 100 % (the default), and keep Turbo mode off (it runs any game 2x).
- Astris: VSync on.

#### High priority shortcut

To start the emulator at High priority every time: right-click its desktop shortcut, choose **Properties**, and in **Target** put `cmd.exe /c start "" /high` in front of the existing path, keeping its quotes. Example: `cmd.exe /c start "" /high "C:\Emulators\Ryujinx.exe"`. Optional: set **Run** to Minimized to keep the command window out of the way, and use **Change Icon** to get the emulator's icon back.

## 45 FPS version

**On a 60 Hz screen, 45 FPS cannot display perfectly evenly.**

Try the 60 FPS version first, whether you play on Switch or an emulator. If your setup can't hold a steady 60, try this 45 FPS version. It runs the game at the normal game's speed while it holds 45, and can help in demanding scenes, for example docked at 1080p on Switch.

**Game speed:** at 45 FPS the game plays at the pace of the normal game. Game speed still follows the frame rate: below 45 the game slows down in step (at 43 FPS, about 4% slower).

**One version at a time:** install only one frame-rate version. They change the same parts of the game.

**Game:** versions 3.0.0 to 3.0.3, as for the 60 FPS version.

**Switch:**

- Atmosphere custom firmware and sys-clk with a profile for this game. These are reference readings from one 2017 Switch (V1), not clock recommendations for every Switch:
  - Handheld on the charger: **CPU 1428 MHz, GPU 768 MHz, memory 1331 MHz** held 45 FPS, also in Happy Home Paradise.
  - Docked at 1080p: **CPU 1428 MHz, memory 1600 MHz** and GPU **844 MHz** or **921 MHz**. Both held 43 FPS or more in the busiest spots, with the battery charging. In that test, 844 ran the GPU near its limit and charged the battery faster; 921 gave the GPU headroom and charged more slowly.
  - At the Switch's own clocks (sys-clk off, handheld on the charger) the game ran at 40 to 45 FPS and dipped.
- Read the **PFPS** line of the Status Monitor overlay: it shows 45, sometimes 44 or 46 for a moment. The **FPS** line next to it jumps between about 43 and 47 even when the game holds 45, because it averages the frame times.

**Emulators:** Ryujinx (VSync mode Switch, the default), Citron (Limit Speed Percent 100 %, the default), Eden (speed limit 100 %, the default) or Astris (Apple silicon Mac, VSync on). Your computer needs to hold a steady 45 FPS. Keep the emulator at normal speed, as for the 60 FPS version.

**Install:** the same steps as the 60 FPS version, with the two 45 FPS zips: `45fps-switch-speedfix-v1-3-0-acnh.zip` (Switch) and `45fps-emulator-speedfix-v1-3-0-acnh.zip` (emulators).

- **Switch:** copy the `atmosphere` folder from the 45 FPS Switch zip to the root of your SD card. To remove it, delete these together:
  - `atmosphere/exefs_patches/ACNH_45FPS_SpeedFix`
  - `atmosphere/contents/01006F8002326000/romfs/Pack/StaticParam.pack`
  - `atmosphere/contents/01006F8002326000/romfs/Bcsv/ItemNpcFtrActionParam.bcsv`
  - `atmosphere/contents/01006F8002326000/romfs/Bcsv/ItemNpcWherearenFtrActionParam.bcsv`
  - `atmosphere/contents/01006F8002326000/romfs/Bcsv/NpcInterest.bcsv`
- **Ryujinx, Citron, Eden, Astris:** copy the `ACNH 45 FPS + SpeedFix` folder from the 45 FPS emulator zip (inside `mods/contents/01006F8002326000/`), the same way as the 60 FPS folder. On Astris, add it with Manage Mods > Add.
- **Switching between 60 and 45 on a Switch:** delete these together, then copy the new `atmosphere` folder:
  - The other version's folder: `atmosphere/exefs_patches/ACNH_60FPS_SpeedFix` or `atmosphere/exefs_patches/ACNH_45FPS_SpeedFix`
  - `atmosphere/contents/01006F8002326000/romfs/Pack/StaticParam.pack`
  - `atmosphere/contents/01006F8002326000/romfs/Bcsv/ItemNpcFtrActionParam.bcsv`
  - `atmosphere/contents/01006F8002326000/romfs/Bcsv/ItemNpcWherearenFtrActionParam.bcsv`
  - `atmosphere/contents/01006F8002326000/romfs/Bcsv/NpcInterest.bcsv`
  The pack and Bcsv files must all come from the version you play.
- **Switching in an emulator:** keep only one frame-rate folder in the game's mods folder (Ryujinx: enable only one under Manage Mods).

Details and measurements: [docs/measured-45.md](https://github.com/tmouh/acnh-60fps/blob/main/docs/measured-45.md) and [docs/how-it-works.md](https://github.com/tmouh/acnh-60fps/blob/main/docs/how-it-works.md).

## Other mods

Works alongside mods that replace models, textures or music.

Conflicts:

- Any other 60 FPS or frame-rate mod, cheat or tool.
- Any mod that includes its own `romfs/Pack/StaticParam.pack`. Only one copy can load, so one of the two mods stops working. The same applies to `romfs/Bcsv/ItemNpcFtrActionParam.bcsv`, `romfs/Bcsv/ItemNpcWherearenFtrActionParam.bcsv` and `romfs/Bcsv/NpcInterest.bcsv`.

This mod needs no ResourceSizeTable file. If your other mods need one, use one made for 3.0.3; older ones can crash the game or hide objects.

## Install

**Back up your save first** (JKSV or Checkpoint).

Download the zip for your platform from the [GameBanana page](https://gamebanana.com/mods/722295) (Files section): the Switch zip for Atmosphere, the emulator zip for Ryujinx, Citron, Eden and Astris. The 45 FPS version has its own two zips (see 45 FPS version). The Switch zip does nothing useful in an emulator. This repo holds the sources: the code patches for 45, 60 and 120 FPS, the parameter-file patches (`pack/StaticParam.pack.ips`, `pack45/StaticParam45.pack.ips` and `pack120/StaticParam120.pack.ips`, applied to the game's own file), the three `romfs/Bcsv/` villager data files for each rate, and the tools that build the zips.

**Switch:** copy the `atmosphere` folder from the Switch zip to the root of your SD card. To remove the mod, delete these together:

- `atmosphere/exefs_patches/ACNH_60FPS_SpeedFix`
- `atmosphere/contents/01006F8002326000/romfs/Pack/StaticParam.pack`
- `atmosphere/contents/01006F8002326000/romfs/Bcsv/ItemNpcFtrActionParam.bcsv`
- `atmosphere/contents/01006F8002326000/romfs/Bcsv/ItemNpcWherearenFtrActionParam.bcsv`
- `atmosphere/contents/01006F8002326000/romfs/Bcsv/NpcInterest.bcsv`

Removing only part of the mod can leave the game at the wrong speed. Delete all the listed parts together to play without the mod.

**Ryujinx:** right-click the game, **Open Mods Directory**, copy the `ACNH 60 FPS + SpeedFix` folder from the emulator zip (inside `mods/contents/01006F8002326000/`) into it, then right-click the game, **Manage Mods**, and make sure it is enabled. On Linux or Steam Deck, use the folder that Open Mods Directory opens.

**Citron:** right-click the game, **Open Mod Data Location**, and copy the same `ACNH 60 FPS + SpeedFix` folder from the emulator zip (inside `mods/contents/01006F8002326000/`) into it. Copy that folder itself, not the `mods` folder: Citron looks for `exefs` and `romfs` at most one folder down. Make sure it is ticked under the game's **Properties** > **Add-Ons**.

**Eden:** right-click the game, Open Mod Data Location, and copy the `ACNH 60 FPS + SpeedFix` folder there, so it directly contains `exefs` and `romfs`.

**Astris (Apple silicon Mac):** unzip the emulator zip, right-click the game, **Manage Mods**, click **Add** and choose the `ACNH 60 FPS + SpeedFix` folder (for 45 FPS, the `ACNH 45 FPS + SpeedFix` folder). Keep only one version enabled and VSync on.

## Too fast or too slow

The game should play at the pace of the normal game. If it does not:

- **Wrong zip:** emulators need the emulator zip. The Switch zip does nothing useful in an emulator.
- **Partial copy:** the `ACNH 60 FPS + SpeedFix` folder must directly contain both `exefs` and `romfs`. With only one of them the game runs at the wrong speed. On Switch, all items listed under Install must be there.
- **Emulator speed:** for 45 and 60 FPS, the speed limit must be 100 % and the frame-rate limit on (see Emulators above). For 120 FPS: Ryujinx: **Options > Settings > System**; scroll down to Hacks and tick **Enable Custom Refresh Rate (Experimental)**, then scroll back up, set **VSync** to **Custom Refresh Rate** and drag **Custom Refresh Rate %** to **200 %** (not 120: the slider is a percentage, and 200 % is 120 FPS). Citron and Eden: **Emulation > Configure > System**, **Limit Speed Percent 200 %**. The FPS counter cannot tell you: Citron shows 60 FPS both when the game runs at normal speed and when it runs twice as fast.
- **Computer not fast enough:** if the FPS counter stays below 60 (with the 45 FPS version: below 45), the game runs slower to match (with the 60 FPS version at 45 FPS about 25% slower; with the 45 FPS version at 43 FPS about 4% slower). Try the 45 FPS version if your setup can't hold 60; if it can't hold 45 either, play without the mod.
- **Another 60 FPS mod or cheat:** turn off every other 60 FPS or frame-rate mod, cheat or tool.
- **More than one version installed:** keep only one frame-rate version: 45, 60 or 120 FPS.
- **Wrong game version:** only 3.0.0 to 3.0.3 work (see Game above).
- **Switch:** check the Switch requirements above (sys-clk profile running, charger, handheld mode when docked).

## Known issues

- Any game update breaks it. If ACNH ever happens to receive a new update down the line, an update for the mod will be released shortly.
- On the 2017 Switch, a very full island can dip below 60 FPS in the evening even at maximum clocks (the CPU is the limit), and the game slows slightly for those moments. Islands differ.

The patch sources are in this repo. `pack/StaticParam.pack.ips` (60 FPS), `pack45/StaticParam45.pack.ips` (45 FPS) and `pack120/StaticParam120.pack.ips` (120 FPS) apply to the game's own `romfs/Pack/StaticParam.pack`; the ready-made pack and the matching three `romfs/Bcsv/` files are in each zip. How the patches work and how to build the files yourself: [docs/how-it-works.md](https://github.com/tmouh/acnh-60fps/blob/main/docs/how-it-works.md).

## License

ACNH 60 FPS + SpeedFix © 2026 tmouh, licensed under [CC BY-NC 4.0](https://creativecommons.org/licenses/by-nc/4.0/) (full text in [LICENSE](LICENSE)).

- **Credit:** if you share this mod, or anything made from it, name "ACNH 60 FPS + SpeedFix by tmouh" and link https://gamebanana.com/mods/722295. If you changed it, say so.
- **No commercial use.**

`StaticParam.pack` in the GameBanana zips is modified game data and remains Nintendo's; the license covers the patches, tools and documentation.
