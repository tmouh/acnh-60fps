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

## How it was made

I used multiple expensive Claude Code subscriptions to fan out agents operating emulators and running tests. I personally tested the mod on a real V1 2017 modded Switch and held 60 FPS on safe overclocks (1785/844/1600), finding that most stress was on the CPU, with my top core at about 91-92% usage.

- **Side-by-side testing:** Two copies of the game ran together on PC, the normal game and the mod, from the same save with the same scripted button presses. For every single update, the agent read each game's state from memory and timed actions to the frame.
- **Finding what counts frames:** Turning around while running instead played a walking animation at 60 FPS, because the game picks animations by how far you moved in one frame, which halves at 60. The agent pulled the animation data out of the game, rebuilt that choice in a small model that matched the measurements frame for frame, and fixed it with one change.
- **Checking its own footage:** While cutting the comparison video, the agent went through the clips frame by frame and caught a small difference I hadn't noticed while testing. It saw the clock and minimap come back about 0.4 s early after an axe swing and traced this to fixed frame counts in the game's HUD code (15 frames after an action, 30 after walking), doubled them, and brought the gap down to about 0.1 s.

## Requirements

**Game:** versions 3.0.0 to 3.0.3. Older versions don't work, the game can run too slow or freeze.

**The game must hold 60 FPS.** Game speed follows the frame rate: at 45 FPS everything runs at three-quarter speed.

**Switch:**

- Atmosphere custom firmware.
- sys-clk with a profile for this game, running while you play (a profile does nothing while sys-clk is turned off). Tested on a 2017 Switch (V1, Atmosphere 1.11.2, firmware 22.5.0), handheld on a 15 V USB-C PD charger with the battery full: **CPU 1785 MHz, GPU 844 MHz, memory 1600 MHz** held 60 FPS.
  - Not GPU 921: with CPU 1785 it drew more power than the charger supplies, so the battery slowly drained while plugged in. 844 holds 60 with power in balance. Below a full battery, expect slow or no charging while playing.
  - GPU above 768 MHz needs the dock or a full-power charger (Nintendo's adapter or a 15 V USB-C PD charger). On a low-power USB charger sys-clk caps the GPU at 768 and the battery may drain while playing (untested).
  - On battery the GPU is capped at 460 MHz, which does not hold 60. This applies as soon as you unplug the charger. Remove the mod before playing on battery.
- Docked: at 1080p the game does not hold 60, even at sys-clk's maximum clocks (about 45 FPS on a 2017 Switch, so the game plays about 25% slower). Forcing handheld mode while docked, the TV gets 720p and the game holds 60 (ReverseNX-RT overlay, which needs SaltyNX).
- An FPS counter for the first session helps (Status Monitor overlay, which needs SaltyNX). **Do not use FPSLocker with this mod.**
- At these clocks the stock fan runs at or near full speed, which is loud. NX-FanControl (Ultrahand/Tesla overlay) lets you set a quieter fan curve. It is untested with this mod, and a quieter curve means higher temperatures (about 59 °C SoC at these clocks with the fan at 90-100 %).

**PC:** Ryujinx (tested on Ryubing Canary 1.3.351), Citron (tested on stable 2026.04.18 and nightly 40212aa3e) or Eden (tested on v0.2.1) with update 3.0.0, 3.0.1, 3.0.2 or 3.0.3 installed, on a PC that holds a steady 60 FPS. Make sure yours does before you play with the mod: the game runs slower whenever it drops below 60 (at 45 FPS, about 25% slower). If it can't hold 60, play without the mod. Keep the emulator at normal speed:

- Ryujinx: VSync mode Switch (the default); do not use an unlimited or turbo frame rate.
- Citron: Limit Speed Percent at 100 % (the default; **Emulation** > **Configure** > **System**). Ctrl+U, or Home+Y on a controller, turns the frame-rate limit off and the game runs too fast; the status bar then shows "(Unlocked)". It is back on the next time you start the game.
- Eden: the speed limit is 100 % by default. Eden also has a Turbo speed mode (200 % by default) that makes any game run 2x, so keep it off.

Planned: a 120 FPS version for PC emulators. It will take some time.

Other emulators are untested.

## Other mods

Works alongside mods that replace models, textures or music (tested). Text mods are expected to work but are untested.

Conflicts:

- Any other 60 FPS or frame-rate mod, cheat or tool.
- Any mod that includes its own `romfs/Pack/StaticParam.pack`. Only one copy can load, so one of the two mods stops working.

This mod needs no ResourceSizeTable file. If your other mods need one, use one made for 3.0.3; older ones can crash the game or hide objects.

## Install

**Back up your save first** (JKSV or Checkpoint).

Download the zip for your platform from the [GameBanana page](https://gamebanana.com/mods/722295) (Files section): the Switch zip for Atmosphere, the PC emulators zip for Ryujinx, Citron and Eden. The Switch zip does nothing useful in an emulator. This repo holds the sources: the code patches (the 60 FPS patch and one SpeedFix patch per game version), the parameter-file patch (`pack/StaticParam.pack.ips`, applied to the game's own file) and the tools that build the zips.

**Switch:** copy the `atmosphere` folder from the Switch zip to the root of your SD card. To remove the mod, delete these two together:

- `atmosphere/exefs_patches/ACNH_60FPS_SpeedFix`
- `atmosphere/contents/01006F8002326000/romfs/Pack/StaticParam.pack`

Removing only one of them runs the game at double speed or half speed. Deleting both is the only way to play without the mod.

**Ryujinx:** right-click the game, **Open Mods Directory**, copy the `ACNH 60 FPS + SpeedFix` folder from the PC emulators zip (inside `mods/contents/01006F8002326000/`) into it, then right-click the game, **Manage Mods**, and make sure it is enabled. On Linux or Steam Deck, use the folder that Open Mods Directory opens.

**Citron:** right-click the game, **Open Mod Data Location**, and copy the same `ACNH 60 FPS + SpeedFix` folder from the PC emulators zip (inside `mods/contents/01006F8002326000/`) into it. Copy that folder itself, not the `mods` folder: Citron looks for `exefs` and `romfs` at most one folder down. Make sure it is ticked under the game's **Properties** > **Add-Ons**.

**Eden:** right-click the game, Open Mod Data Location, and copy the `ACNH 60 FPS + SpeedFix` folder there, so it directly contains `exefs` and `romfs`.

## Too fast or too slow

The game should play at the pace of the normal game. If it does not:

- **Wrong zip:** emulators need the PC emulators zip. The Switch zip does nothing useful in an emulator.
- **Partial copy:** the `ACNH 60 FPS + SpeedFix` folder must directly contain both `exefs` and `romfs`. With only one of them the game runs at the wrong speed. On Switch, both items listed under Install must be there.
- **Emulator speed:** the speed limit must be 100 % and the frame-rate limit on (see PC above). The FPS counter cannot tell you: Citron shows 60 FPS both when the game runs at normal speed and when it runs twice as fast.
- **PC not fast enough:** if the FPS counter stays below 60, the game runs slower to match (at 45 FPS, about 25% slower). Play without the mod on that PC.
- **Another 60 FPS mod or cheat:** turn off every other 60 FPS or frame-rate mod, cheat or tool.
- **Wrong game version:** only 3.0.0 to 3.0.3 work (see Game above).
- **Switch:** check the Switch requirements above (sys-clk profile running, charger, handheld mode when docked).

## Known differences

- K.K. Slider concerts: the last moments after the song come a fraction of a second early (up to 0.7 s at the island's first concert).
- Wasps chase and sting about 0.1 s sooner. Keep medicine in your pockets.
- A few actions are a fraction of a second off: a warp pipe trip (0.1 s shorter), casting the fishing rod (0.06 s longer), releasing a caught creature, walking out of a building, the clock and minimap coming back after an action (about 0.1 s early), opening a letter (0.06 s faster), the popup after picking up bells (stays about 0.15 s shorter). See [docs/measured.md](https://github.com/tmouh/acnh-60fps/blob/main/docs/measured.md).
- The title screen goes dark about 1 s sooner after you press A.
- A fish that gets away after you miss the bite darts off twice as fast, for half as long, so it ends up just as far away.
- Pitfall seeds: mashing buttons can climb out up to about 0.12 s sooner. Very fast mashing (over about 15 presses a second) is untested and is expected to get out noticeably sooner.
- Fireworks evenings: villagers' pauses between their event actions are about half as long as in the normal game (for example 2.5 s instead of 5 s).
- Rain falls at the normal speed and ripples on water look the same, but in wind the drops are blown sideways about twice as fast.
- With other players (untested), the call-out balloon over another player's head is expected to close after about 1 s instead of 2 s.
- Tested on one 2017 Switch and one PC.
- Any game update breaks it. If ACNH ever happens to receive a new update down the line, an update for the mod will be released shortly.
- On the 2017 Switch this was tested on, a very full island can dip below 60 FPS in the evening even at maximum clocks (the CPU is the limit), and the game slows slightly for those moments. Newer models are untested. Islands differ.

## Not tested

- Happy Home Paradise.
- Local wireless play (island visits between consoles).
- Online play, including online island visits.
- Dream Suite.
- Android builds of Eden and Citron, and Steam Deck.
- Newer Switch models (2019 V2, Lite, OLED).
- Game versions 3.0.0, 3.0.1 and 3.0.2 on a Switch, Ryujinx or Citron (tested on Eden only).
- Game languages other than English and Japanese.

The patch sources are in this repo. `pack/StaticParam.pack.ips` applies to the game's own `romfs/Pack/StaticParam.pack`; the ready-made file is in the GameBanana zips. How the patches work and how to build the files yourself: [docs/how-it-works.md](https://github.com/tmouh/acnh-60fps/blob/main/docs/how-it-works.md).

## License

ACNH 60 FPS + SpeedFix © 2026 tmouh, licensed under [CC BY-NC 4.0](https://creativecommons.org/licenses/by-nc/4.0/) (full text in [LICENSE](LICENSE)).

- **Credit:** if you share this mod, or anything made from it, name "ACNH 60 FPS + SpeedFix by tmouh" and link https://gamebanana.com/mods/722295. If you changed it, say so.
- **No commercial use.**

`StaticParam.pack` in the GameBanana zips is modified game data and remains Nintendo's; the license covers the patches, tools and documentation.
