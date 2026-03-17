# TrueSens

A cross-game mouse sensitivity standardizer for FPS and TPS games.

---

## The Problem

Every game has its own sensitivity scale. A sensitivity of 3.0 in one game 
feels nothing like 3.0 in another. When you switch between games, your 
muscle memory breaks, and there's no universal way to fix it without 
doing the math yourself.

## What TrueSens Does

TrueSens lets you choose a target sensitivity in **cm/360** — the physical
distance your mouse travels to complete a full 360-degree turn — and 
converts it accurately across multiple games.

If it takes you 36 cm to do a 360 in CS2, TrueSens will tell you exactly 
What sensitivity to set in Valorant, Apex Legends, or any other supported 
game to feel identical.

Your desktop cursor speed stays untouched. This tool only affects in-game 
settings.

## Planned Features

- [x] Core cm/360 conversion calculator
- [x] Multi-game support with a community-maintained game database
- [x] Simple desktop UI
- [x] Automatic game detection
- [x] Auto-apply sensitivity to supported game config files
- [x] Profile saving

## How It Works (The Core Math)

Every game has a **yaw value** — the number of degrees the camera rotates 
per count of mouse input. By combining your DPI, in-game sensitivity, and 
a game's yaw, TrueSens calculates your physical cm/360 and converts it 
to any other game's sensitivity scale.
```
cm_per_360 = (360 / (yaw × sensitivity) / DPI) × 2.54
```

## Status

Early development. Currently building the core calculator (Phase 1).

## Anti-Cheat and Safety

TrueSens is designed to only interact with game config files on disk, 
never with game memory. It will not run while games are active. 
Compatibility and safety notes will be documented per game as support 
is added.

## Tech Stack

- Python 3.x
- Game database: JSON

## Contributing

Game database contributions (yaw values with verified sources) are welcome. 
See CONTRIBUTING.md (coming soon).

---

*Built as a learning project and real tool by NateCurtis402.*
```

