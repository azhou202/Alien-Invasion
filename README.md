# Alien-Invasion
Alien invasion is a version of the classic arcade game where you pilot a ship and shoot down fleets of alien ships.
# Frameworks
This game is built with Pygame.
# Features
* Lives system that limits the amount of ships you can lose to aliens before you lose the game.
* The speed of the alien ships increase as you level up.
* Scoreboard displays high score, current score, level, and ships left.
* Sound effects such as ship explosion.
* Power ups that are obtained through shooting certain alien ships. 
  1. Shield: Prevents hitting one alien from counting against your ships left. <sup> work in progress </sup>
  2. Super Bullet: Fires one bullet that is wider than the standard bullet and can pass through alien ships to hit multiple. 
  3. Extra Life: Gives an extra life to the player. If the player has not lost any lives, this does nothing. <sup> work in progress </sup>
# Structure
The main script is `alien_invasion.py`. Running this script will start the game.
Features of the objects in the game (aliens, ship, background, scoreboard, game stats, bullet, etc.) can be found in their respective files.
`settings.py` controls global game settings such as window size and the size of bullets
`game_functions.py` contains assorted functions that allow the game to work.
# Acknowledgement
This game was written with inspiration from Eric Matthes's work in his book "Python Crash Course, A Hands-On, Project-Based, Introduction to Programming".
