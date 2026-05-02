**Slice Edge: Boss Protocol** is a high-energy, arcade-style action game developed in Python using the **Pygame** library. Experience fluid slicing mechanics as you defend against waves of targets and face off against elite bosses in a test of reflexes and precision.

---

## Getting Started

### Prerequisites
*   **Python 3.x**
*   **Pygame Library**

### Installation
1.  Ensure Python is installed on your system.
2.  Install the required library via terminal:
    ```bash
    pip install pygame
    ```
3.  Ensure the following assets are in your project directory:
    *   `root.py` (The main game logic)
    *   `python_logo.png` (Used for particle effects)
    *   `quiz.jpg` (Heal target texture)
    *   `smug_javier.png` (Elite target texture)
    *   `sad_javier.jpg` (Boss texture)

---

## How to Play

*   **Objective**: Slice falling targets to earn points and stay alive.
*   **Controls**: Use your **Mouse Left-Click** and drag to create a "slice" path across the screen.
*   **Start Game**: Press **ENTER** at the menu to begin the protocol.

### Target Types
*   **Standard Targets**: Green (1 HP), Orange (3 HP), and Yellow (2 HP).
*   **Yellow Splinters**: Larger yellow targets burst into smaller, fast-moving fragments when destroyed.
*   **Quiz Targets (`quiz.jpg`)**: Slicing these restores **5 HP** and grants a score bonus.
*   **Elite Smug Javier (`smug_javier.png`)**: High-value targets protected by an energy barrier. You must break the barrier before dealing damage.

### The Boss Protocol
Destroying **3 Smug Javier** elites has a high chance of triggering the **Boss: Sad Javier (`sad_javier.jpg`)**.
*   The Boss moves horizontally across the top of the screen.
*   He spawns a constant rain of mini-projectiles.
*   Defeating the boss clears the screen and awards a massive **500-point bonus**.

---

## 🛠️ Technical Overview

*   **Collision System**: Uses `rect.clipline` to detect intersections between the player's slice path and target hitboxes.
*   **Particle Engine**: Custom `Particle` class using `python_logo.png` with gravity and life-cycle physics.
*   **State Management**: Handles transitions between `menu` and `playing` states with wave-based difficulty scaling.
*   **UI/UX**: Includes a shaking boss effect, floating "A+" text for heals, and a dynamic HUD tracking your score and streak.

---
