# Word Scramble Game

Word Scramble Game is a simple desktop game developed using Python and the Pygame library.  
The objective of the game is to guess the correct word from a scrambled version within a limited time.

## Project Description

This project demonstrates the use of Python for game development using the Pygame library.  
The game provides multiple difficulty levels and challenges the player to identify the correct word before the timer runs out.

The application includes a graphical interface, background images, sound effects, and a scoring system.

## Technologies Used

- Python
- Pygame
- Random module
- OS module

## Features

- Graphical interface built using Pygame
- Three difficulty levels: Easy, Medium, and Hard
- Word scrambling algorithm
- Countdown timer
- Score tracking
- Sound alert when time is low
- Game over screen with restart option

## Project Structure

```
word-scramble-game
│
├── main.py
├── assets
│   ├── images
│   │   ├── imge.jpg
│   │   ├── pngtree.png
│   │   └── background.jpg
│   │
│   └── sounds
│       └── TunePocket-Countdown-Timer-10-Sec-1-Preview.mp3
```

## Installation

1. Clone the repository

```
git clone https://github.com/VinoSRHarrison/word-scramble-game.git
```

2. Navigate to the project directory

```
cd word-scramble-game
```

3. Install the required dependency

```
pip install pygame
```

## Running the Game

Run the following command:

```
python main.py
```

## How to Play

1. Launch the game.
2. Select a difficulty level:
   - Press **1** for Easy
   - Press **2** for Medium
   - Press **3** for Hard
3. A scrambled word will appear on the screen.
4. Type your guess and press **Enter**.
5. If the answer is correct, your score increases.
6. The game ends when the timer reaches zero.

## Future Improvements

- Add more word categories
- Add difficulty-based scoring
- Add sound effects for correct and incorrect answers
- Improve user interface and animations

## Author

Vino S R Harrison  
Computer Science Undergraduate

GitHub: https://github.com/VinoSRHarrison
