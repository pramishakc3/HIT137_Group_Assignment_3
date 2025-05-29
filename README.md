HIT137 Group Assignment 3
This repository contains two separate Python applications developed for HIT137 Group Assignment 3:

Image Editor App (Question 1): A desktop tool for basic image manipulation.

Space Battle Game (Question 2): A simple arcade shooter featuring player controls, enemy waves, and level progression.

Installation
1. Clone the Repository
bash
Copy code
git clone https://github.com/pramishakc3/HIT137_Group_Assignment_3.git
cd HIT137_Group_Assignment_3
2. Set Up a Virtual Environment (Recommended)
bash
Copy code
python -m venv venv
# On Windows:
.\venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
3. Install Dependencies
Create a requirements.txt file in the root of your project with the following:

nginx
Copy code
pygame
opencv-python
Pillow
numpy
Then run:

bash
Copy code
pip install -r requirements.txt


Question 1: Image Editor App
A GUI-based image editor for basic editing tasks.

How to Run
bash
Copy code
python q1_image_editor.py
<<<<<<< HEAD
Features
Load & Save Images via file dialogs

Grayscale Conversion

Gaussian Blur

Rotate 90° (Clockwise)

Crop Tool

Select an area on the left canvas

Click "Crop" to show result on right canvas

Resize via a slider (percentage-based)

Undo/Redo
=======
>>>>>>> f96435dfdb14a42a3df62d3935a4e9ccc07058bf

Ctrl+Z: Undo

Ctrl+Y: Redo

Keyboard Shortcuts

Ctrl+S: Save

Ctrl+R: Rotate

Dual Canvas for original vs. modified image


Question 2: Space Battle Game
An arcade-style shooter with enemies, collectibles, levels, and a boss fight.

How to Run
Ensure the Input folder is in the same directory as your game script, containing:

space.mp3, player_plane.png, enemy_plane.png, boss_plane.png

bulletshot.mp3, victory.mp3, collect.mp3, levelup.mp3

backvd.mp4 (background video)

Then run:

bash
Copy code
python q2_space_battle.py
<<<<<<< HEAD
Game Features
🎮 Player Controls
Move: A/D or Left/Right arrows
=======
>>>>>>> f96435dfdb14a42a3df62d3935a4e9ccc07058bf

Jump: W or Up arrow

Shoot: Spacebar

Enemies
Regular enemies fall from the top

Boss enemy appears at Level 3

Enemies can shoot bullets

Game Logic
Collision Detection:
<<<<<<< HEAD

Bullets vs. enemies

Enemy bullets vs. player

Bullet-on-bullet collision

Collectibles

Health & Lives:

Player health bar and lives counter

Enemies and boss have visible health bars

Scoring System

Escape Count for enemies going off-screen

Game States
Start screen with instructions

Level complete transitions

Game over screen

Victory screen (with looping video)

Level Progression
Level 1: 5 enemies

Level 2: 7 enemies

Level 3: Boss battle

Current level shown on HUD

Collectibles
Health Boost: Heals damage

Extra Life

Score Boost

Audio & Visuals
Looping video as background (via OpenCV)

Background music

Sound effects for bullets, pickups, level transitions, etc.

Notes
Replace script names (q1_image_editor.py, q2_space_battle.py) if you rename them.

All asset files must be placed inside the Input folder.
=======
Player vs. Enemy Bullets: Player takes damage when hit by enemy bullets.
Player Bullets vs. Enemies: Player bullets deal damage to enemies.
Bullet-on-Bullet Collision: Player and enemy bullets can cancel each other out upon collision.
Player vs. Collectibles: Player can collect items that provide bonuses.
Scoring System: The player earns points for defeating regular enemies.
Player Health & Lives (HUD):
The game displays the player's remaining lives.
A health bar indicates the player's current health (hits taken) in their current life.
The score is displayed on the HUD.
Counts how many enemies have escaped (gone off-screen).
Game States:
Start Screen: A screen before the game begins with instructions.
Game Over Screen: Displayed when the player runs out of lives or too many enemies escape.
Win Screen: Displayed upon defeating the final boss, with a looping background video and visual effects.
Level Complete Screen: A temporary screen indicating when a level has been successfully cleared before progressing.
Level Progression:
The game features 3 distinct levels.
Each level has a target number of enemies to defeat (e.g., 5 for Level 1, 7 for Level 2).
Upon reaching the target, the game progresses to the next level.
The current level is displayed on the HUD.
Collectibles (New Feature):
Collectibles spawn randomly during gameplay.
Health Boost: Reduces hits taken, effectively restoring player health.
Extra Life: Grants the player an additional life.
Score Boost: Adds points directly to the player's score.
Visuals & Audio:
Dynamic Background: Utilizes a looping video as the game's background using OpenCV.
Sound Effects: Includes sounds for bullet shots, collecting items, victory, and level ups.
Background Music: Looping music plays throughout the game.
Remember to replace the placeholder names for your Python files (q1_image_editor.py, q2_space_battle.py) if you decide to rename them. Also, make sure all the image, video, and audio files are correctly placed in the Input folder within your repository.
>>>>>>> f96435dfdb14a42a3df62d3935a4e9ccc07058bf
