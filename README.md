# Cards
The aim of this repository is to support any card game (std. french deck) the user(s) wish to play. Basic functionality includes:

- Drawing from the main deck to the table
- Drawing from the main deck to a specified hand
- Drawing from a specified hand to the table
- Drawing from the table to a specified hand

There are currently two versions of this program.

## C only, console based
To compile, navigate to server/backend/ and execute
```sh
make main
```
To run, simply execute in the same directory:
```sh
./main
```

There is a set of predetermined commands that can be run. While running the program, execute:
```sh
help
```
to see more.


## ASP.NET/MVC Server, Python frontend
To compile, navigate to backend/ and execute:
```sh
make library
```

Place the resulting .so file in server/CardsServer/bin.

### Local
Start the server by running the C# program from within visual studio. Note the port.
Start the game by visiting:

localhost:xxxx/api/start

To run, from client/, execute:
```sh
python main.py
```

Enter in the server box localhost:xxxx and click submit.

### AWS/EC2 Hosted
Start a EC2 instance (Windows Server 2012 Base ami) with RDP (3389), HTTP (80), and web deployment (8172) ports open.
The HTTP port needs to be universal to allow anyone to connect to the main server and achieve the desired functionality.
Log in and set up remote publishing and web. If inexperienced with this, you may find links like:

http://www.tothenew.com/blog/deploy-asp-net-application-on-amazon-ec2/

particularly helpful.

Publish the server code from within visual studio to the ec2 instance.
Start the game by visiting your EC2 instance's public dns + /api/start. i.e.:

ec2-xx-xxx-xxx-xxx.compute-1.amazonaws.com/api/start

To run, from client, execute:
```sh
python main.py
```

Enter the EC2 instance's public dns in the server box and click submit.

