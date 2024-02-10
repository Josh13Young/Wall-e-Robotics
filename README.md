# Project WALL-E

Programs 1.0, 1.6.3, 2.2.1 and 2.2.2 work with the following setup:
- 2 motors with wheels on the side,
- 2 touch sensors for the left and right
- 1 forward facing ultrasonic sensor parallel to the ground on top
And the configuration of these (i.e setting ports) is in `bot_control/Bot.py`

Program 2.2.3 is similar, but the ultrasonic sensor isn't forward facing anymore

## Dev Setup
Upon first cloning the repo, install `pre-commit` on your system (i.e on Ubuntu `sudo apt install pre-commit`) and run `pre-commit` in the root Git directory to initialise the git hooks we'll be using on this project.

I recommend using `commitizen` too (`pip install commitizen`) for better commits (then make git commits via `cz commit`).