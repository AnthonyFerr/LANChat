# LANChat
A local-area chat application in the terminal using the client-server model.

This is a refactor of a simple project I made while taking Network Programming (Spring 2025).
Here are some improvements being made:
 - Clients/Server use threads to get around IO BLOCKED states
 - Clients use dynamic sockets designated by the operating system (as they should have from the start!)
 - The server will need to handle client disconnects
