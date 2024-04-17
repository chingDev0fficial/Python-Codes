# Gunner vs Target Simulation

This Python script simulates a scenario where a gunner with various guns and bullets tries to eliminate a target by firing at it. The script implements classes for `Person`, `Target`, `Gunner`, `Bullet`, `Magazine`, `Gun`, and specific gun types like `Pistol`, `Shotgun`, and `Sniper`. It also includes utility functions for console clearing and displaying big font messages.

## How It Works

- **Classes**: The script defines several classes to represent different entities and functionalities:
  - `Person`: Base class representing a person with attributes like name, health, armor, and gun mastery.
  - `Target`: Subclass of `Person` representing a target.
  - `Gunner`: Subclass of `Person` representing a gunner with a specific gun mastery and distance from the target.
  - `Bullet`: Class representing a bullet with a damage value and ID.
  - `Magazine`: Class representing a magazine that holds bullets.
  - `Gun`: Base class representing a gun with attributes like base damage, accuracy, range, and ammo capacity. It includes methods for triggering the gun and reloading it.
  - `Pistol`, `Shotgun`, `Sniper`: Subclasses of `Gun` with specific attribute values for different types of guns.
  
- **Simulation**: The script simulates the interaction between the gunner and the target:
  - The gunner selects a gun and a bullet type.
  - The gunner attempts to fire at the target, reducing its health and armor based on the selected gun and bullet properties.
  - The gunner can reload the gun if needed.
  - The simulation continues until the target's health reaches zero, indicating that the target has been eliminated.

## How to Run

1. Ensure you have Python installed on your system.
2. Clone or download the repository to your local machine.
3. Open a terminal or command prompt and navigate to the directory containing the Python script.
4. Run the script using the command `python gunner_vs_target.py`.
5. Follow the on-screen prompts to select a gun and bullet type, and observe the simulation results.

## Note

- This script is for educational purposes and simulation only. It does not accurately represent real-world scenarios and should not be used for any practical applications.

Feel free to explore the code, modify it, or use it as a reference for your own projects or learning purposes!
