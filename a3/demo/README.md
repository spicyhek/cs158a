# cs158 Assignment 3

This is a simulation of the leader election process on a network.

## How to Run

- Note: To simulate multiple computers in the network on one computer, the port number of each server and client must be different. To do this, editing the config file in between creating each server/client is needed and shown below.
- Use Python 3

1. Ensure that config.txt reads:

   ```
   localhost,5001
   localhost,5002
   ```

   Then, open a terminal and run:

   ```
   cd a3
   python .\myleprocess.py
   ```

2. Modify config.txt to:

   ```
   localhost,5002
   localhost,5003

   # This is to differentiate each process and correspond them to a log file (port number 5001 is log1, 5002 is log2, 5003 is log3)
   ```

   Then, open another terminal and run:

   ```
   cd a3
   python .\myleprocess.py
   ```

3. Modify config.txt to:
   ```
   localhost,5003
   localhost,5001
   ```
   Then, open another terminal and run:
   ```
   cd a3
   python .\myleprocess.py
   ```
   Each process will generate its own UUID and the leader will be elected and printed after this run.

## Example Runthrough

### After running third process:

![alt text](image.png)
