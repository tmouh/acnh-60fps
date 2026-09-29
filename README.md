# ACNH 60 FPS + SpeedFix

Animal Crossing: New Horizons 60 FPS patch with **normal game speed** for version 3.0.3 only.

## The problem

The internal game logic is timed by FPS, not seconds. Nintendo never intended for anything other than 30 FPS for the vanilla game, so everything happens/moves too quickly when increasing the frame rate. Run it at 60 FPS instead of 30 and everything happens twice as fast: walking, text, animations, villagers, weather, effects.

## The fix

- **60 FPS patch:** lets the game run at 60.
- **SpeedFix:** puts the game back at normal speed. It manually halves the per-frame speeds and doubles the frame-counted timers in the game's parameter file, and patches the code that counts frames (text, animations, camera, effects, villagers, fishing and more).

The result is a smoother picture at the pace of the normal game.

## How it was made

I used multiple expensive Claude Code subscriptions to fan out agents operating emulators and running tests. I personally tested the mod on a real V1 2017 modded Switch and held 60 FPS on safe overclocks (1785/844/1600), finding that most stress was on the CPU, with my top core fluctuating below 90% usage.

- **Side-by-side testing:** Two copies of the game ran together on PC, the normal game and the mod, from the same save with the same scripted button presses. For every single update, the agent read each game's state from memory and timed actions to the frame.
- **Finding what counts frames:** Reversing while running played a walking animation at 60 FPS, because the game picks animations by how far you moved in one frame, which halves at 60. The agent pulled the animation data out of the game, rebuilt that choice in a small model that matched the measurements frame for frame, and fixed it with one change.
- **Checking its own footage:** While cutting the comparison video, the agent went through the clips frame by frame and caught a small difference I hadn't noticed while testing. It saw the clock and minimap come back about 0.4 s early after an axe swing and traced this to fixed frame counts in the game's HUD code (15 frames after an action, 30 after walking), doubled them, and brought the gap down to about 0.1 s.

## Requirements

**Game:** version **3.0.3** only (title ID `01006F8002326000`, main build `FF1D1C05670DB6021C85B624A710B963`). On any other version the code patches are skipped but the parameter file still loads, which runs the game at the wrong speed or can freeze it.

**The game must hold 60 FPS.** Game speed follows the frame rate: at 45 FPS everything runs at three-quarter speed.

**Switch:**

- Atmosphere custom firmware.
- sys-clk with a profile for this game. Tested on a 2017 Switch (V1, Atmosphere 1.11.2, firmware 22.5.0), handheld on a 15 V USB-C PD charger with the battery full: **CPU 1785 MHz, GPU 844 MHz, memory 1600 MHz** held 60 FPS.
  - Not GPU 921: with CPU 1785 it drew more power than the charger supplies, so the battery slowly drained while plugged in. 844 holds 60 with power in balance. Below a full battery, expect slow or no charging while playing.
  - GPU above 768 MHz needs the dock or a full-power charger (Nintendo's adapter or a 15 V USB-C PD charger). On a low-power USB charger sys-clk caps the GPU at 768 and the battery may drain while playing (untested).
  - On battery the GPU is capped at 460 MHz, which does not hold 60. Remove the mod before playing on battery.
- Docked: at 1080p the game does not hold 60, even at sys-clk's maximum clocks (about 45 FPS on a 2017 Switch). Forcing handheld mode while docked, the TV gets 720p and the game holds 60 (ReverseNX-RT overlay, which needs SaltyNX).
- An FPS counter for the first session helps (Status Monitor overlay, which needs SaltyNX). **Do not use FPSLocker with this mod.**
- At these clocks the stock fan runs at or near full speed, which is loud. NX-FanControl (Ultrahand/Tesla overlay) lets you set a quieter fan curve. It is untested with this mod, and a quieter curve means higher temperatures (about 59 °C SoC at these clocks with a moderate curve).
- Newer Switch models (2019 V2, Lite, OLED) are untested.

**PC:** Ryujinx (tested on Ryubing Canary 1.3.351) with the 3.0.3 update installed, on a machine that holds a steady 60. VSync mode: Switch (the default); do not use an unlimited or turbo frame rate. Other emulators are untested.

## Other mods

Works alongside mods that replace models, textures or music (tested). Text mods are expected to work but are untested.

Conflicts:

- Any other 60 FPS or frame-rate mod, cheat or tool.
- Any mod that includes its own `romfs/Pack/StaticParam.pack`. Only one copy can load, so one of the two mods stops working.

This mod needs no ResourceSizeTable file. If your other mods need one, use one made for 3.0.3; older ones can crash the game or hide objects.

## Install

**Back up your save first** (JKSV or Checkpoint).

Download the zip for your platform from [Releases](https://github.com/tmouh/acnh-60fps/releases).

**Switch:** copy the `atmosphere` folder from the Switch zip to the root of your SD card. To remove the mod, delete these two together:

- `atmosphere/exefs_patches/ACNH_60FPS_SpeedFix`
- `atmosphere/contents/01006F8002326000/romfs/Pack/StaticParam.pack`

Removing only one of them runs the game at double speed or half speed. Deleting both is the only way to play without the mod.

**Ryujinx:** right-click the game, **Open Mods Directory**, copy the `ACNH 60 FPS + SpeedFix` folder from the Ryujinx zip (inside `mods/contents/01006F8002326000/`) into it, then right-click the game, **Manage Mods**, and make sure it is enabled. On Linux or Steam Deck, use the folder that Open Mods Directory opens.

## Known differences

- K.K. Slider concerts: the last moments after the song come a fraction of a second early (up to 0.7 s at the island's first concert).
- Wasps chase and sting about 0.1 s sooner. Keep medicine in your pockets.
- A few actions are a fraction of a second off: a warp pipe trip (0.1 s shorter), casting the fishing rod (0.06 s longer), releasing a caught creature, walking out of a building, the clock and minimap coming back after an action (about 0.1 s early). See [docs/measured.md](https://github.com/tmouh/acnh-60fps/blob/main/docs/measured.md).
- Tested on one 2017 Switch and one PC.
- Any game update breaks it. If ACNH ever happens to receive a new update down the line, an update for the mod will be released shortly.

The patch sources are in this repo. `pack/StaticParam.pack.ips` applies to the game's own `romfs/Pack/StaticParam.pack`; the ready-made file is in the zips.
