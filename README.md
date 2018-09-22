# Cards
The aim of this repository is to allow any card game the user(s) wish to play. Basic functionality includes:

- Drawing from the main deck to the table
- Drawing from the main deck to a specified hand
- Drawing from a specified hand to the table
- Drawing from the table to a specified hand

## Compiling
There are currently two versions of this program.

### C only, console based
To compile, navigate to backend/ and execute ```make main```.
To run, simply execute in backend ```./main```.
There is a set of predetermined commands that can be run. While running the program, execute ```help``` to see more.


### C backend with Python frontend
To compile, navigate to backend/ and execute ```make library```.
To run, from the main directory, execute ```python wrapper.py```.
There is limited functionality with this feature right now. If you wish to play around with the program, I recommend compiling and running the C-only version (see above).
