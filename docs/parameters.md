# StaticParam.pack: changed values

The mod replaces `romfs/Pack/StaticParam.pack`. Compared with the game's own 3.0.3 file (SHA-256 `4a3d6530d6430b6b…`), **1,429 values in 104 files** are changed, each in place: same file size, same structure, 1,905 bytes differ (mod file SHA-256 `370486e5beb84c25…`). The full list is in `parameters.csv`.

Why: the game advances its logic once per frame. At 60 FPS it runs twice as many updates per second, so the values it applies once per update are rescaled to give the same real-time result as the 30 FPS game. Each value's rule below is read from its numbers alone (new against original).

## Rules

| rule | values | what it keeps the same in real time |
|---|---:|---|
| speed x1/2 | 607 | speeds: distance or angle moved per second (applied twice as often, so halved). Includes turn, scroll and spawn rates |
| acceleration/gravity x1/4 | 111 | acceleration and gravity: speed-up and falling arcs (a change to a per-update speed, applied twice as often: 1/2 x 1/2) |
| update count x2 | 683 | timers and durations counted in updates. Includes some values whose names end in `Sec` or `Time` |
| smoothing r -> 1-sqrt(1-r) | 22 | easing toward a target: two new steps close the same share of the gap as one original step, since (1 - new)^2 = 1 - r |
| other: per-update decay k -> sqrt(k) | 3 | per-update decay: two new steps equal one original step, since new^2 = k |
| other: start frame 0 -> 1 (timing alignment) | 2 | warp pipe entry: fall and shrink start frames, one update later so they line up with the 30 FPS timing |
| other: x2 + 2 (timing alignment) | 1 | warp pipe entry: fade-out start, doubled plus two updates so the fade lines up with the 30 FPS timing |
| **total** | **1,429** | |

3 values (mRotateSpeed, mSwimWaitTurnChaseDegreeY, each 4 → 2) fit both x1/2 and k → sqrt(k); they are turn speeds and are listed as speed x1/2.

## By folder

| folder | files | values | x1/2 | x1/4 | x2 | smoothing | sqrt(k) | pipe timing |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `Param/Actor` | 10 | 150 | 60 | 23 | 39 | 22 | 3 | 3 |
| `Param/Camera` | 37 | 190 |  |  | 190 |  |  |  |
| `Param/Fg` | 1 | 6 | 4 | 1 | 1 |  |  |  |
| `Param/Fish` | 9 | 161 | 117 |  | 44 |  |  |  |
| `Param/Gfx` | 4 | 20 | 15 |  | 5 |  |  |  |
| `Param/Insect` | 39 | 847 | 411 | 87 | 349 |  |  |  |
| `Param/Npc` | 2 | 44 |  |  | 44 |  |  |  |
| `Param/Others` | 1 | 6 |  |  | 6 |  |  |  |
| `Param/RadioGymnastics` | 1 | 5 |  |  | 5 |  |  |  |
| **total** | **104** | **1,429** | **607** | **111** | **683** | **22** | **3** | **3** |

## By file

| file | changed values | rules applied | examples (original → new) |
|---|---:|---|---|
| `Param/Actor/ActorWaterFall.byml` | 1 | x2 (1) | `mCycle` 8 → 16 |
| `Param/Actor/BbsBirdActor.byml` | 8 | x1/2 (4), x2 (1), sqrt(k) (3) | `mDayFlySpeed` 1.65 → 0.825; `mNightHoldFrame` 4 → 8; `mDayDownScale` 0.6 → 0.7745967 |
| `Param/Actor/CreatureShowActorMgr.byml` | 10 | x1/2 (7), x1/4 (2), x2 (1) | `mShellfishAlphaOutFrame` 10 → 20; `0x49562be6[0]` 1.2 → 0.6; `mGravity` 1.5 → 0.375 |
| `Param/Actor/FishFieldActor.byml` | 4 | x1/2 (2), x2 (2) | `mMoveSpeedMin` 0.125 → 0.0625; `mScaleOutFrame` 15 → 30; `mMoveSpeedMax` 0.25 → 0.125 |
| `Param/Actor/FtrActor.byml` | 5 | x1/2 (2), x1/4 (1), x2 (2) | `mLeafGravity` 0.1 → 0.025; `mDemiseScaleDownFrame` 7 → 14; `mLocalWindAddCalcMaxDecrement` 0.05 → 0.025 |
| `Param/Actor/ItemPreviewSwapActor.byml` | 2 | x1/2 (2) | `mCatalogRotateSpeed` 1 → 0.5; `mMyDesignRotateSpeed` 1.4 → 0.7 |
| `Param/Actor/ObjectBalloonActor.byml` | 1 | x1/2 (1) | `mDefaultSpeed` 0.085 → 0.0425 |
| `Param/Actor/ObjectKKFesShip.byml` | 5 | x1/2 (3), x2 (2) | `mWave2CycleSpd` 2.5 → 1.25; `mNpcFoundDelay` 240 → 480; `mFrame` 950 → 1900 |
| `Param/Actor/PlayerActor.byml` | 113 | x1/2 (39), x1/4 (20), x2 (29), smoothing (22), pipe timing (3) | `mRunSpeedMax` 1.25 → 0.625; `mDefaultGravity` -0.25 → -0.0625; `mBreathTimer` 220 → 440 |
| `Param/Actor/StructureHouseDoorDecoActor.byml` | 1 | x2 (1) | `mDemiseScaleDownFrame` 7 → 14 |
| `Param/Camera/AirPlane_DemoInterporateParams.byml` | 1 | x2 (1) | `mFrame` 60 → 120 |
| `Param/Camera/CameraInterpolateParams.byml` | 43 | x2 (43) | `mFrame` 30 → 60 |
| `Param/Camera/CloudIsland_DemoInterporateParams.byml` | 2 | x2 (2) | `mFrame` 150 → 300 |
| `Param/Camera/IdrAirPortDemoDeparture_DemoInterporateParams.byml` | 1 | x2 (1) | `mFrame` 120 → 240 |
| `Param/Camera/IdrDream_DemoInterporateParams.byml` | 1 | x2 (1) | `mFrame` 150 → 300 |
| `Param/Camera/IdrHotelRoom_DemoInterporateParams.byml` | 4 | x2 (4) | `mFrame` 100 → 200 |
| `Param/Camera/IdrMuseumArt_0_DemoInterporateParams.byml` | 10 | x2 (10) | `mFrame` 42 → 84 |
| `Param/Camera/IdrMuseumCafe_DemoInterporateParams.byml` | 2 | x2 (2) | `mFrame` 60 → 120 |
| `Param/Camera/IdrMuseumEnt00_DemoInterporateParams.byml` | 1 | x2 (1) | `mFrame` 24 → 48 |
| `Param/Camera/IdrMuseumEnt01_DemoInterporateParams.byml` | 1 | x2 (1) | `mFrame` 24 → 48 |
| `Param/Camera/IdrMuseumFish_0_DemoInterporateParams.byml` | 4 | x2 (4) | `mFrame` 24 → 48 |
| `Param/Camera/IdrMuseumFish_1_DemoInterporateParams.byml` | 5 | x2 (5) | `mFrame` 24 → 48 |
| `Param/Camera/IdrMuseumFish_2_DemoInterporateParams.byml` | 5 | x2 (5) | `mFrame` 24 → 48 |
| `Param/Camera/IdrMuseumFossil_0_DemoInterporateParams.byml` | 3 | x2 (3) | `mFrame` 24 → 48 |
| `Param/Camera/IdrMuseumFossil_1_DemoInterporateParams.byml` | 4 | x2 (4) | `mFrame` 24 → 48 |
| `Param/Camera/IdrMuseumFossil_2_DemoInterporateParams.byml` | 2 | x2 (2) | `mFrame` 24 → 48 |
| `Param/Camera/IdrMuseumInsect_0_DemoInterporateParams.byml` | 2 | x2 (2) | `mFrame` 30 → 60 |
| `Param/Camera/IdrMuseumInsect_1_DemoInterporateParams.byml` | 4 | x2 (4) | `mFrame` 24 → 48 |
| `Param/Camera/IdrMuseumInsect_2_DemoInterporateParams.byml` | 1 | x2 (1) | `mFrame` 30 → 60 |
| `Param/Camera/MainFieldDemoCeremony_DemoInterporateParams.byml` | 1 | x2 (1) | `mFrame` 240 → 480 |
| `Param/Camera/MainFieldDemoFirstLive_DemoInterporateParams.byml` | 2 | x2 (2) | `mFrame` 30 → 60 |
| `Param/Camera/MainFieldDemoLandingNet_DemoInterporateParams.byml` | 1 | x2 (1) | `mFrame` 1200 → 2400 |
| `Param/Camera/MainFieldDemoLanding_DemoInterporateParams.byml` | 1 | x2 (1) | `mFrame` 1200 → 2400 |
| `Param/Camera/MainField_DemoInterporateParams.byml` | 7 | x2 (7) | `mFrame` 150 → 300 |
| `Param/Camera/MainField_DemoInterporateParams_RVer_10400.byml` | 8 | x2 (8) | `mFrame` 150 → 300 |
| `Param/Camera/MainField_DemoInterporateParams_RVer_10600.byml` | 9 | x2 (9) | `mFrame` 150 → 300 |
| `Param/Camera/MainField_DemoInterporateParams_RVer_10700.byml` | 14 | x2 (14) | `mFrame` 150 → 300 |
| `Param/Camera/PhotoStudio_DemoInterporateParams.byml` | 1 | x2 (1) | `mFrame` 40 → 80 |
| `Param/Camera/PlayerHouse_DemoInterporateParams.byml` | 1 | x2 (1) | `mFrame` 300 → 600 |
| `Param/Camera/PlayerHouse_DemoInterporateParams_RVer_10400.byml` | 2 | x2 (2) | `mFrame` 300 → 600 |
| `Param/Camera/SeaDemoToKappeiIsland_DemoInterporateParams.byml` | 2 | x2 (2) | `mFrame` 300 → 600 |
| `Param/Camera/SeaDemoToMainField_DemoInterporateParams.byml` | 2 | x2 (2) | `mFrame` 300 → 600 |
| `Param/Camera/Title_DemoInterporateParams.byml` | 2 | x2 (2) | `mFrame` 150 → 300 |
| `Param/Camera/WherearenEditIndoor_DemoInterporateParams.byml` | 5 | x2 (5) | `mFrame` 180 → 360 |
| `Param/Camera/WherearenMainIsland_DemoInterporateParams.byml` | 19 | x2 (19) | `mFrame` 60 → 120 |
| `Param/Camera/WherearenNpcGarden_DemoInterporateParams.byml` | 10 | x2 (10) | `mFrame` 100 → 200 |
| `Param/Camera/WherearenNpcHouse_DemoInterporateParams.byml` | 7 | x2 (7) | `mFrame` 180 → 360 |
| `Param/Fg/BeatAwayStumpParam.byml` | 6 | x1/2 (4), x1/4 (1), x2 (1) | `mRollingY` 1 → 0.5; `mEndTime` 17 → 34; `mGravity` 0.2 → 0.05 |
| `Param/Fish/Museum/AntiStream/FishMuseum02.byml` | 28 | x2 (28) | `mDriftFrameMin` 10 → 20; `mDriftFrameMax` 30 → 60 |
| `Param/Fish/Museum/Layout/FishInsect00.byml` | 18 | x1/2 (18) | `mBaseSpeed` 0.1 → 0.05 |
| `Param/Fish/Museum/Layout/FishInsect01.byml` | 1 | x1/2 (1) | `mBaseSpeed` 0.1 → 0.05 |
| `Param/Fish/Museum/Layout/FishMuseum00.byml` | 31 | x1/2 (31) | `mBaseSpeed` 0.04 → 0.02 |
| `Param/Fish/Museum/Layout/FishMuseum01.byml` | 21 | x1/2 (21) | `mBaseSpeed` 0.3 → 0.15 |
| `Param/Fish/Museum/Layout/FishMuseum02.byml` | 46 | x1/2 (46) | `mBaseSpeed` 0.5 → 0.25 |
| `Param/Fish/Museum/RoundsSwimming/FishInsect00.byml` | 2 | x2 (2) | `mWaitFrameRangeMin` 20 → 40; `mWaitFrameRangeMax` 90 → 180 |
| `Param/Fish/Museum/RoundsSwimming/FishMuseum00.byml` | 10 | x2 (10) | `mWaitFrameRangeMin` 30 → 60; `mWaitFrameRangeMax` 120 → 240 |
| `Param/Fish/Museum/RoundsSwimming/FishMuseum02.byml` | 4 | x2 (4) | `mWaitFrameRangeMin` 20 → 40; `mWaitFrameRangeMax` 60 → 120 |
| `Param/Gfx/CloudDrawer.byml` | 4 | x1/2 (4) | `mWindScrollSpeedZ` 0.005 → 0.0025; `mProjectionShadowScrollSpeedX` 3 → 1.5; `mProjectionShadowScrollSpeedZ` 2 → 1 |
| `Param/Gfx/FieldUnitModelMgr.byml` | 3 | x2 (3) | `mUvScrollLoopTimingSRT1` 29 → 58; `mUvScrollLoopTimingSRT0` 40 → 80; `mUvScrollLoopTimingSRT2` 32 → 64 |
| `Param/Gfx/ShootingStarParam.byml` | 3 | x1/2 (2), x2 (1) | `mLife` 90 → 180; `mSpeed[0]` -2 → -1 |
| `Param/Gfx/WaveSimulation.byml` | 10 | x1/2 (9), x2 (1) | `mPropagationFrame` 30 → 60; `mRainUnitRate` 0.004 → 0.002; `mSeaChoppyScrollRate2Min` -0.1 → -0.05 |
| `Param/Insect/FieldAttackerParams.byml` | 21 | x1/2 (10), x2 (11) | `mMoveMinSec` 2 → 4; `mPursueSpeed` 1.5 → 0.75; `mMoveMaxSec` 4 → 8 |
| `Param/Insect/FieldAutumnLeafParams.byml` | 16 | x1/2 (10), x1/4 (6) | `mDumpAccel` 0.00625 → 0.0015625; `mDumpSpeed` 0.3125 → 0.15625; `mGravity` -0.00625 → -0.0015625 |
| `Param/Insect/FieldBeeParams.byml` | 12 | x1/2 (6), x1/4 (2), x2 (4) | `mAddDirAng` 9.997559 → 4.9987793; `mAroundFrame` 60 → 120; `mAccel` 0.3125 → 0.078125 |
| `Param/Insect/FieldBeetleParams.byml` | 8 | x2 (8) | `mStopFramesMin` 90 → 180; `mStopFramesMax` 180 → 360; `mMoveFramesMax` 150 → 300 |
| `Param/Insect/FieldButterflyParams.byml` | 64 | x1/2 (58), x1/4 (2), x2 (4) | `mApproachCycle` 300 → 600; `mSpeedForwardStep` 0.007813 → 0.00195325; `mSpeedUpDown` 0.03125 → 0.015625 |
| `Param/Insect/FieldCastOffSkinParams.byml` | 8 | x1/2 (4), x1/4 (4) | `mDumpAccel` 0.03125 → 0.0078125; `mDumpSpeed` 0.625 → 0.3125; `mGravity` -0.0625 → -0.015625 |
| `Param/Insect/FieldDragonflyParams.byml` | 34 | x1/2 (20), x2 (14) | `mApproachCycle` 600 → 1200; `mAppSpeedMax` 1.09375 → 0.546875; `mRestTime` 90 → 180 |
| `Param/Insect/FieldDytiscidaeParams.byml` | 25 | x1/2 (12), x1/4 (3), x2 (10) | `mNidusTimeMin` 150 → 300; `mSlowDown` 0.007813 → 0.00195325; `mDiveSpeed` 0.15 → 0.075 |
| `Param/Insect/FieldFeatherParams.byml` | 10 | x1/2 (8), x1/4 (2) | `mAddDirAng` 2.999268 → 1.499634; `mSpeedChaseMove` 0.007813 → 0.00195325; `mBreathMax` 0.078125 → 0.0390625 |
| `Param/Insect/FieldFireflyParams.byml` | 8 | x1/2 (8) | `mAddDirDeg` 0.999756 → 0.499878; `mBreathMax` 0.0625 → 0.03125; `mMoveSpeed` 0.117188 → 0.058594 |
| `Param/Insect/FieldFlowerParams.byml` | 29 | x1/2 (21), x2 (8) | `mMoveSecMax` 3 → 6; `mStopWaitRotateAngleYStep` 5 → 2.5; `mMoveSecMin` 1 → 2 |
| `Param/Insect/FieldGerriadeParams.byml` | 4 | x1/2 (2), x1/4 (2) | `mSlowDown` 0.007813 → 0.00195325; `mBorderSpeed` 0.5 → 0.25 |
| `Param/Insect/FieldHermitCrabParams.byml` | 10 | x1/2 (2), x1/4 (2), x2 (6) | `mMoveSpeed` 0.3125 → 0.15625; `mVanishTime` 10 → 20; `mRegistSpeed` -0.015625 → -0.00390625 |
| `Param/Insect/FieldHoneyBeeParams.byml` | 16 | x1/2 (10), x1/4 (2), x2 (4) | `mApproachCycle` 10 → 20; `mAddDirAng` 2.999268 → 1.499634; `mSpeedChaseMove` 0.0125 → 0.003125 |
| `Param/Insect/FieldInsectParams.byml` | 135 | x1/2 (30), x1/4 (4), x2 (101) | `mEscapeSpeedFly` 0.625 → 0.3125; `mGravity` -0.15625 → -0.0390625; `m1stSec` 60 → 120 |
| `Param/Insect/FieldLigiaParams.byml` | 2 | x1/2 (2) | `mEscapeSpeed` 1.875 → 0.9375 |
| `Param/Insect/FieldLocustParams.byml` | 32 | x1/2 (2), x1/4 (7), x2 (23) | `mStartChilpTime` 1 → 2; `mRegistSpeed` -0.015625 → -0.00390625; `mMoveFrames` 20 → 40 |
| `Param/Insect/FieldMosquitoParams.byml` | 10 | x1/2 (8), x1/4 (2) | `mAddDirAng` 1.999512 → 0.999756; `mSpeedChaseMove` 0.019531 → 0.00488275; `mBreathMax` 0.078125 → 0.0390625 |
| `Param/Insect/FieldMuscidaeParams.byml` | 16 | x1/2 (10), x1/4 (2), x2 (4) | `mApproachCycle` 1 → 2; `mAddDirAng` 14.996338 → 7.498169; `mSpeedChaseMove` 0.15625 → 0.0390625 |
| `Param/Insect/FieldPetalParams.byml` | 16 | x1/2 (10), x1/4 (6) | `mDumpAccel` 0.00625 → 0.0015625; `mDumpSpeed` 0.3125 → 0.15625; `mGravity` -0.00625 → -0.0015625 |
| `Param/Insect/FieldPhylliumParams.byml` | 16 | x1/2 (2), x1/4 (2), x2 (12) | `mEscapeMaxSec` 2 → 4; `mMoveSpeed` 0.15625 → 0.078125; `mRegistSpeed` -0.015625 → -0.00390625 |
| `Param/Insect/FieldPopStoneParams.byml` | 14 | x1/2 (3), x1/4 (3), x2 (8) | `mEscapeRefreshCycle` 2 → 4; `mRegistSpeed` -0.015625 → -0.00390625; `mSpeed` 0.09375 → 0.046875 |
| `Param/Insect/FieldSnowCrystalParams.byml` | 24 | x1/2 (15), x1/4 (9) | `mDumpAccel` 0.00625 → 0.0015625; `mDumpSpeed` 0.3125 → 0.15625; `mGravity` -0.00625 → -0.0015625 |
| `Param/Insect/FieldStumpParams.byml` | 18 | x1/2 (10), x2 (8) | `mMoveSecMax` 10 → 20; `mRotSpeedDeg` 1.40625 → 0.703125; `mMoveSecMin` 5 → 10 |
| `Param/Insect/FieldThreadParams.byml` | 18 | x1/2 (6), x1/4 (6), x2 (6) | `mDumpAccel` 0.05 → 0.0125; `mDumpSpeed` 1 → 0.5; `mStopSecMax` 4 → 8 |
| `Param/Insect/FieldTigerBeetleParams.byml` | 21 | x1/2 (6), x1/4 (3), x2 (12) | `mEscapeSpeed` 0.9375 → 0.46875; `mMoveSecMax` 8 → 16; `mAccel` 0.03125 → 0.0078125 |
| `Param/Insect/FieldWispParams.byml` | 6 | x1/2 (6) | `mBreathMax` 0.0625 → 0.03125; `mMoveSpeed` 0.117188 → 0.058594; `mSpeedY` 0.0625 → 0.03125 |
| `Param/Insect/MuseumBeetleBattleParams.byml` | 17 | x1/2 (6), x2 (11) | `mEscapeLastAngleXStepDeg` 10 → 5; `mInitialChargeMaxSec` 3 → 6; `mKnockOverSpeed` 0.4 → 0.2 |
| `Param/Insect/MuseumBeetleParams.byml` | 8 | x2 (8) | `mStopFramesMin` 90 → 180; `mStopFramesMax` 180 → 360; `mMoveFramesMax` 150 → 300 |
| `Param/Insect/MuseumFlyInCageParams.byml` | 12 | x1/2 (9), x2 (3) | `mCycleSec` 0.5 → 1; `mGyrateAngleYStepDeg` 15 → 7.5; `mBreadthMax` 0.1 → 0.05 |
| `Param/Insect/MuseumFlyStraightParams.byml` | 9 | x1/2 (5), x2 (4) | `mHoveringTimeMax` 2 → 4; `mUpSpeedMax` 0.078125 → 0.0390625; `mDownSpeed` -0.390625 → -0.1953125 |
| `Param/Insect/MuseumFlyStraightWithRestParams.byml` | 21 | x1/2 (10), x2 (11) | `mApproachCycleSec` 20 → 40; `mUpSpeedMax` 0.078125 → 0.0390625; `mRestTimeSec` 3 → 6 |
| `Param/Insect/MuseumFlyTottering.byml` | 55 | x1/2 (53), x1/4 (2) | `mSpeedUpDown` 0.03125 → 0.015625; `mSpeedChaseMove` 0.007813 → 0.00195325; `mGyrateAngleYStepDeg` 1.499634 → 0.749817 |
| `Param/Insect/MuseumFlyTotteringWithRestParams.byml` | 34 | x1/2 (28), x1/4 (2), x2 (4) | `mApproachCycleSec` 20 → 40; `mSpeedUpDown` 0.1 → 0.05; `mSpeedChaseMove` 0.007813 → 0.00195325 |
| `Param/Insect/MuseumLocustParams.byml` | 20 | x1/4 (8), x2 (12) | `mActStopSecMax` 1 → 2; `mRegistSpeed` 0.015625 → 0.00390625; `mActStopSecMin` 0.5 → 1 |
| `Param/Insect/MuseumMovePointToPointParams.byml` | 9 | x1/2 (2), x1/4 (2), x2 (5) | `mGyrateAngleYStepDeg` 15 → 7.5; `mJumpFrame` 20 → 40; `mRegistSpeed` 0.015625 → 0.00390625 |
| `Param/Insect/MuseumSkateOnTheWaterParams.byml` | 12 | x1/2 (5), x1/4 (4), x2 (3) | `mSpeedChaseStep` 0.007813 → 0.00195325; `mGyrateChaseAngleYMaxDeg` 4.394531 → 2.1972654; `mStopSecMax` 3 → 6 |
| `Param/Insect/MuseumWaitWithThreatenParams.byml` | 4 | x2 (4) | `mThreatenSec` 1.5 → 3 |
| `Param/Insect/MuseumWormParams.byml` | 53 | x1/2 (12), x2 (41) | `mMaxWaitTime` 1 → 2; `mSpeed` 0.09375 → 0.046875; `mMaxMoveTime` 15 → 30 |
| `Param/Npc/NpcActivityParam.byml` | 38 | x2 (38) | `mFacePanelReactionIntervalTime` 60 → 120; `mMinimumFtrFrameInHousing` 300 → 600; `mMinimumSitFrameInHousing` 900 → 1800 |
| `Param/Npc/NpcWherearenParam_RVer_20000.byml` | 6 | x2 (6) | `mWaitActionSeconds` 30 → 60; `mHouseOrderEndDemoFascinated` 150 → 300; `mWaitActionMaxSeconds` 45 → 90 |
| `Param/Others/CommonCurves.byml` | 6 | x2 (6) | `mFrame` 70 → 140 |
| `Param/RadioGymnastics/RadioGymnasticsParam/RadioGymnasticsData.byml` | 5 | x2 (5) | `mFirstLookFrameMin` 10 → 20; `mFirstLookFrameMax` 30 → 60; `mStartEmotionSmileOffsetFrameMax` 15 → 30 |

## Columns of `parameters.csv`

- `file`: the file inside `StaticParam.pack`.
- `parameter`: the parameter's name. Values nested in groups show the path below the file's top level; group keys whose names are not recovered appear as `0x` hex, list entries as `[i]`.
- `type`: `f32` (float), `s32` or `u32` (integer), as declared by the parameter's name; the stored type for list entries.
- `original`, `new`: the value in the game's file and in the mod's file (shortest exact float form).
- `factor`: new / original (blank when the original is 0).
- `rule`: one of the rules above.

## Names

Each key in these files is the CRC32 of `<name>.<type>` (for example `mRunSpeedMax.f32`); the names are matched against the strings in the game's own executable.

- Changed values whose own name is not recovered: **6**, in 2 lists of three entries, both in `Param/Actor/CreatureShowActorMgr.byml`: `0x0a9bf76f`, `0x49562be6`. They are listed by hex key.
- Every other changed value has its own name.

## Check

- 1,905 bytes differ between the two files; all 1,905 lie inside the 1,429 listed values (bytes outside a listed value: 0).
- Writing the 1,429 new values into the game's own file reproduces the mod's file exactly: yes.
- The file structure (keys, types, positions) is identical in both files; only values change.
