HIT137 Group Assignment 3
This repository contains two separate Python applications developed for HIT137 Group Assignment 3:
- Image Editor App (Question 1): A desktop tool for basic image manipulation.
- Space Battle Game (Question 2): A simple arcade shooter featuring player controls, enemy waves, and level progression.
  
Installation
1. Clone the Repository
git clone https://github.com/pramishakc3/HIT137_Group_Assignment_3.git
cd HIT137_Group_Assignment_3

2. Set Up a Virtual Environment (Recommended)
python -m venv venv
# On Windows:
.\venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

3. Install Dependencies
Create a requirements.txt file with the following content:
pygame
opencv-python
Pillow
numpy

Then run:
pip install -r requirements.txt


Question 1: Image Editor App
A GUI-based image editor for basic editing tasks.
How to Run
python q1_image_editor.py
Features
•	Load & Save Images via file dialogs
•	Grayscale Conversion
•	Gaussian Blur
•	Rotate 90° (Clockwise)
•	Crop Tool (select area, click Crop)
•	Resize via a slider (percentage-based)
•	Undo/Redo (Ctrl+Z / Ctrl+Y)
•	Keyboard Shortcuts (Ctrl+S, Ctrl+R, etc.)
•	Dual Canvas for original vs. modified image



Question 2: Space Battle Game

An arcade-style shooter with enemies, collectibles, levels, and a boss fight.
How to Run
Make sure the Input folder contains required media files, then run:
python q2_space_battle.py
Game Features

Player Controls
•	Move: A/D or Left/Right arrows
•	Jump: W or Up arrow
•	Shoot: Spacebar

Enemies
Regular enemies fall from the top
Boss enemy appears at Level 3
Enemies can shoot bullets

Game Logic
•	Collision Detection (bullets, enemies, player, collectibles)
•	Health & Lives (bars and counters)
•	Scoring System
•	Escape Count

Game States
•	Start screen with instructions
•	Level complete transitions
•	Game over screen
•	Victory screen (with looping video)

Level Progression
Level 1: 5 enemies
Level 2: 7 enemies
Level 3: Boss battle
HUD shows current level

Collectibles
•	Health Boost
•	Extra Life
•	Score Boost
Audio & Visuals
•	Looping video as background (OpenCV)
•	Background music
•	Sound effects (shots, pickups, etc.)


Notes
Rename the Python files if necessary.
Place all assets in the Input folder.
