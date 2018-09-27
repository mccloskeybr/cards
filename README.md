# Cards
The aim of this repository is to support any card game (std. french deck) the user(s) wish to play. Basic functionality includes:

- Drawing from the main deck to the table
- Drawing from the main deck to a specified hand
- Drawing from a specified hand to the table
- Drawing from the table to a specified hand

## Compiling
There are currently two versions of this program.

### C only, console based
To compile, navigate to server/backend/ and execute ```make main```.
To run, simply execute ```./main``` in the same directory.
There is a set of predetermined commands that can be run. While running the program, execute ```help``` to see more.


### C# Server with Python Frontend (local only)
To compile, navigate to backend/ and execute ```make library```. Place the resulting .so file in server/CardsServer/bin.
Start the server by running the C# program from within visual studio. Note the port. You'll either have to change this to the current default 56785 or change
the hardcoded port num in request.py.
To run, from client/, execute ```python main.py```.
There is limited functionality with this feature right now. If you wish to play around with the program, I recommend compiling and running the C-only version (see above).
