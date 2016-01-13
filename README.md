# Synacor Challenge
The current state of my attempt at the Synacor Challenge.

If you are interested in attempting the Challenge yourself, [visit the official page](https://challenge.synacor.com/) 
and give it a shot - preferably before looking at my solution ;)

This attempt is written in Python (2.7.9).

Files:
  - **VM.py** - short for Virtual Machine, this is the main file: the "actual" solution. Runs the program in the input file 
  - **arch-spec.txt** - The instructions for the first part of the challenge. Describes the virtual machine that needs to be created
  - **challenge.bin** - The puzzle input. Consists of a program (in 0s and 1s) to be ran according to the specifications
  - **program.txt** - The contents of *challenge.bin*, in a human-readable format. 
  - **log.txt** and **log1.txt** - Like *program.txt*, but dynamically generated (only shows instructions that actually run)

<details> 
  <summary>**Spoilers** below! Click to show </summary>
   - **algorithm.py** - An attempt at running a specific section of the code efficiently
   - **gameInput.txt** - The input to automate the "game" up to the teleporter - because *actually* playing the game is so 2015
</details>
  
##Todo

- Approach the algorithm in a different way. (Understanding what it actually does would be a good start)
- Add a description at the start of each code file (and maybe some restructuring?)
