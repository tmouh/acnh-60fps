# ACNH 60 FPS + SpeedFix

Animal Crossing: New Horizons 60 FPS patch with **normal game speed** for versions 3.0.0 to 3.0.3.

Downloads: [GameBanana](https://gamebanana.com/mods/722295). Sources: GitHub.

## What's new in v1.3.0

Adds 120 FPS for emulators, plus villager behaviour and timing fixes at 45, 60 and 120 FPS. The goal is the same: smoother animation, normal game pace, and maintaining the snappy menu navigation and camera response inherent to FPS increases.

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

## Which version

- **60 FPS** (Switch and emulators): try this first.
- **45 FPS** (Switch and emulators): if your setup can't hold a steady 60, for example docked at 1080p on Switch. On a 60 Hz screen, 45 FPS can't display perfectly evenly.
- **120 FPS** (emulators only): only if your PC holds a steady 120.

Install one version at a time. Game speed follows the frame rate: if the game drops below the version's frame rate, it slows down in step (the 60 FPS version at 45 FPS runs about 25% slower).

**Game:** versions 3.0.0 to 3.0.3. Older versions don't work, the game can run too slow or freeze.

## Switch

- Atmosphere, and sys-clk running with a profile for this game.
- Reference clocks from one 2017 Switch (V1), not recommendations for every Switch:
  - 60 FPS, handheld: **CPU 1785 MHz, GPU 844 MHz, memory 1600 MHz**.
  - 45 FPS, handheld: **CPU 1428 MHz, GPU 768 MHz, memory 1331 MHz**. Docked at 1080p: **CPU 1428 MHz, GPU 844 or 921 MHz, memory 1600 MHz** held 43 FPS or more in the busiest spots.
- Handheld needs a full-power charger (Nintendo's adapter or a 15 V USB-C PD charger). A weaker charger caps the GPU at 768 MHz; on battery it is capped at 460 MHz, which can't hold 60. Remove the mod for battery play.
- Docked at 1080p, the 60 FPS version runs at about 45 FPS. Use the 45 FPS version, or force handheld mode with ReverseNX-RT (needs SaltyNX) for 720p at 60.
- The fan gets loud at these clocks; NX-FanControl can set a quieter curve.
- **Do not use FPSLocker with this mod.**
- 45 FPS: read the **PFPS** line of the Status Monitor overlay; it shows 45. The **FPS** line jumps between about 43 and 47 even when the game holds 45.

## Install

**Back up your save first** (JKSV or Checkpoint). Download the zip for your platform and frame rate from the [GameBanana page](https://gamebanana.com/mods/722295) (Files section). The Switch zip does nothing useful in an emulator.

**Switch:** copy the zip's `atmosphere` folder to the root of your SD card. To remove the mod or to change between 45 and 60, first delete these together:

- `atmosphere/exefs_patches/ACNH_60FPS_SpeedFix` (45 FPS: `ACNH_45FPS_SpeedFix`)
- `atmosphere/contents/01006F8002326000/romfs/Pack/StaticParam.pack`
- `atmosphere/contents/01006F8002326000/romfs/Bcsv/ItemNpcFtrActionParam.bcsv`
- `atmosphere/contents/01006F8002326000/romfs/Bcsv/ItemNpcWherearenFtrActionParam.bcsv`
- `atmosphere/contents/01006F8002326000/romfs/Bcsv/NpcInterest.bcsv`

Removing only some of them leaves the game at the wrong speed.

**Emulators:** the version's folder is in the emulator zip, inside `mods/contents/01006F8002326000/`: `ACNH 60 FPS + SpeedFix`, `ACNH 45 FPS + SpeedFix` or `ACNH 120 FPS + SpeedFix`. Keep only one version enabled.

- **Ryujinx:** right-click the game, **Open Mods Directory**, copy the folder into it, then right-click the game, **Manage Mods**, and make sure it is enabled. On Linux or Steam Deck, use the folder that Open Mods Directory opens.
- **Citron:** right-click the game, **Open Mod Data Location**, and copy the folder itself into it (not the `mods` folder: Citron looks for `exefs` and `romfs` at most one folder down). Make sure it is ticked under the game's **Properties** > **Add-Ons**.
- **Eden:** right-click the game, **Open Mod Data Location**, and copy the folder there, so it directly contains `exefs` and `romfs`.
- **Astris (Apple silicon Mac):** unzip the emulator zip, right-click the game, **Manage Mods**, click **Add** and choose the folder.

**Emulator settings:**

- **Windows: set the emulator to High priority every time you start it** (Task Manager > Details > right-click the emulator > Set priority > High). Windows starts programs at Normal priority and doesn't remember the change; at Normal the game can drop frames even on a fast PC.
- **AMD dual-die X3D CPUs:** in the same menu, **Set affinity** and keep only the first half of the CPUs (the V-cache die). This also resets each time.
- **45 and 60 FPS:** keep the emulator at normal speed: Ryujinx VSync mode Switch, Citron and Eden speed limit 100 % (the defaults), Astris VSync on. In Citron, Ctrl+U or Home+Y turns the limit off and the game runs too fast; in Eden, keep Turbo mode off.
- **120 FPS:** Ryujinx: **Options > Settings > System**, **VSync = Custom Refresh Rate**, tick **Enable Custom Refresh Rate**, value **120**. Citron and Eden: speed limit **200 %**.

## Too fast or too slow

The game should play at the pace of the normal game. If it does not:

- **Wrong zip:** emulators need the emulator zip.
- **Partial copy:** the version's folder must directly contain both `exefs` and `romfs`; on Switch, every item listed under Install must be there.
- **Emulator speed:** check the emulator settings above. The FPS counter cannot tell you: Citron shows 60 FPS both when the game runs at normal speed and when it runs twice as fast.
- **Frame rate not held:** the game slows down in step. Set High priority (Windows), or use a lower version (120 → 60 → 45). If your setup can't hold 45, play without the mod.
- **Another frame-rate mod, cheat or tool:** turn it off.
- **More than one version installed:** keep only one.
- **Wrong game version:** only 3.0.0 to 3.0.3 work.
- **Switch:** check the sys-clk profile, the charger and, docked at 1080p, the version (see Switch above).

## Other mods

Works alongside mods that replace models, textures or music. Conflicts: any other 60 FPS or frame-rate mod, cheat or tool, and any mod with its own `romfs/Pack/StaticParam.pack`, `romfs/Bcsv/ItemNpcFtrActionParam.bcsv`, `romfs/Bcsv/ItemNpcWherearenFtrActionParam.bcsv` or `romfs/Bcsv/NpcInterest.bcsv` (only one copy of each can load).

This mod needs no ResourceSizeTable file. If your other mods need one, use one made for 3.0.3; older ones can crash the game or hide objects.

## Known issues

- Any game update breaks it. If ACNH ever happens to receive a new update down the line, an update for the mod will be released shortly.
- On the 2017 Switch, a very full island can dip below 60 FPS in the evening even at maximum clocks (the CPU is the limit), and the game slows slightly for those moments. Islands differ.

## Sources

This repo holds the code patches for 45, 60 and 120 FPS, the parameter-file patches (`pack/StaticParam.pack.ips`, `pack45/StaticParam45.pack.ips`, `pack120/StaticParam120.pack.ips`, applied to the game's own `romfs/Pack/StaticParam.pack`), the three `romfs/Bcsv/` villager data files for each rate, and the tools that build the zips. How the patches work and how to build the files yourself: [docs/how-it-works.md](https://github.com/tmouh/acnh-60fps/blob/main/docs/how-it-works.md). Measurements: [docs/measured.md](https://github.com/tmouh/acnh-60fps/blob/main/docs/measured.md) and [docs/measured-45.md](https://github.com/tmouh/acnh-60fps/blob/main/docs/measured-45.md).

## License

ACNH 60 FPS + SpeedFix © 2026 tmouh, licensed under [CC BY-NC 4.0](https://creativecommons.org/licenses/by-nc/4.0/) (full text in [LICENSE](LICENSE)).

- **Credit:** if you share this mod, or anything made from it, name "ACNH 60 FPS + SpeedFix by tmouh" and link https://gamebanana.com/mods/722295. If you changed it, say so.
- **No commercial use.**

`StaticParam.pack` in the GameBanana zips is modified game data and remains Nintendo's; the license covers the patches, tools and documentation.
