# cs158 Assignment 3

This is a simulation of the leader election process on a network across multiple computers.

## How to Run

- Note: To simulate communication between multiple machines, each machine must have its own `config.txt` and configured with the correct IP address and port of its own server and its neighbor's server, as well as a `log.txt` file.
- Use Python 3

1. On one machine, edit config.txt so that the first line is your IP and port number and the second line is the IP address of the next machine, then run:

   ```
   cd a3
   python myleprocess.py
   ```

2. On the next machine, edit edit config.txt so that the first line is your IP and port number and the second line is the IP address of the next machine, then run the same commands as step 1.

3. Repeat for as many computers as you like.
