Project: HIT137 Group Assignment 3
This repository contains two distinct applications developed as part of HIT137 Group Assignment 3:

Image Editor App (Question 1): A desktop application for basic image manipulation.
Space Battle Game (Question 2): A simple arcade-style game featuring a player, enemies, and level progression.
Installation
To run these applications, you'll need Python installed on your system along with several libraries.

1. Clone the Repository
First, clone this repository to your local machine:

Bash

git clone https://github.com/pramishakc3/HIT137_Group_Assignment_3.git
cd HIT137_Group_Assignment_3
2. Install Dependencies
It's highly recommended to use a virtual environment to manage dependencies.

a. Create and Activate a Virtual Environment (Recommended):

Bash

python -m venv venv
# On Windows:
.\venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
b. Install Required Libraries:

You'll need pygame, opencv-python, Pillow (PIL), and numpy. While your code implies some of these, let's create a requirements.txt file for a smooth installation.

First, create a file named requirements.txt in the root of your project directory with the following content:

pygame
opencv-python
Pillow
numpy
Then, install them using pip:

Bash

pip install -r requirements.txt

Question 1: Image Editor App
This application provides a graphical user interface (GUI) for basic image editing functionalities.

How to Run
Navigate to the project root and run the Python script for Question 1:

Bash

python q1_image_editor.py
(Note: You might want to rename your this is question no 1 file to something like q1_image_editor.py to be more descriptive and easier to run.)

Functional Requirements Implemented
Load Image: Users can load an image from their local file system using a file dialog.
Save Image: Users can save the currently displayed (and edited) image to a chosen location.
Grayscale Conversion: Transform the loaded image to a grayscale version.
Apply Blur: Apply a Gaussian blur filter to the image.
Rotate 90°: Rotate the image clockwise by 90 degrees.
Crop Image:
Users can select a region on the left canvas by clicking and dragging.
Clicking the "Crop" button will apply this selection to the image, displaying the cropped result on the right canvas.
Resize Slider: A slider allows users to resize the image displayed on the right canvas by a percentage.
Undo/Redo Functionality:
Undo (Ctrl+Z): Reverts the last image modification, allowing users to go back through their edit history.
Redo (Ctrl+Y): Reapplies a previously undone modification.
Keyboard Shortcuts:
Ctrl+S: Save Image
Ctrl+Z: Undo
Ctrl+Y: Redo
Ctrl+R: Rotate 90°
Dual Canvas Display: The application uses two canvases: one for the original image (or the working copy being edited) and another for showing the cropped/resized output.


Question 2: Space Battle Game
This is an arcade-style shooter game where the player controls a plane to defeat incoming enemies and a boss.

How to Run
Ensure you have the Input folder in the same directory as your game script. This folder should contain:

space.mp3 (background music)
player_plane.png
enemy_plane.png
boss_plane.png
bulletshot.mp3
victory.mp3
collect.mp3
levelup.mp3
backvd.mp4 (background video)
Navigate to the project root and run the Python script for Question 2:

Bash

python q2_space_battle.py
(Note: You might want to rename your this is question no 2 file to something like q2_space_battle.py for clarity.)

Functional Requirements Implemented

Player Control:
Movement (WASD / Arrow Keys): The player can move left and right using the A/D keys or Left/Right arrow keys.
Jump (W / Up Arrow): The player can jump, with gravity affecting their vertical movement.
Shoot (Spacebar): The player can fire projectiles.
Enemies:
Regular Enemies: Enemies spawn from the top of the screen and move downwards.
Boss Enemy: A more powerful boss enemy appears in Level 3.
Enemy Projectiles: Enemies shoot their own bullets towards the player.
Health Bars: Both regular enemies and the boss have health bars displayed above them.
Collision Detection:
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