# PRG1

PRG1 (Programming 1) is a module in semester 1.1 of the CSF course in Ngee Ann Polytechnic, focusing on Python language.

This repository contains my Python code written for the module's assignment.


Overall description:

This program is a game played over 16 turns.
In each turn, the player will build one of two randomly-selected buildings in the 4x4 city.
In the first turn, the player can build anywhere.
In subsequent turns, the player can only build on squares connected to existing buildings.
The other building not built is discarded.
There are five types of buildings, with 8 copies each.
They are: Beach (BCH), Factory (FAC), House (HSE), Shop (SHP), and Highway (HWY)


Scoring System:

Beach:

    Scores 3 points if built on the left-most or right-most column, or 1 point otherwise


Factory:

    Scores 1 point per Factory, up to a maximum of 4 points for the first 4 factories.
    Subsequent factories only score 1 point each.


House:

    Scores 1 point only if placed next to a Factory.
    Otherwise, scores 1 point for each adjacent House or Shop, and 2 points for each adjacent Beach.


Shop:

    Scores 1 point per different type of adjacent building.


Highway:

    Scores 1 point per connected Highway in the same row



Note:

Change variables 'path', 'game_data_file', and 'high_score_file' before running
