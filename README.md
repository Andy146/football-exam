# Football-exam for IT

## How to start:

- Make sure you have the flask module installed on your system
- If you don't have it you can get it with pip in a terminal/command prompt:
```bash
pip install Flask
or
pip3 install Flask
```
- Run the server.py file at the root of the project
- Open the website that will be on http://localhost:5000
- (Hope that there are no more steps to start on windows, I haven't tested it in windows)

## Additional instructions:

- The stored dataset is stored as a csv in the "data" folder, it contains every match (which teams played and how many goals they each scored)
- If you want to clear the stored dataset, DO NOT delete results.csv 
- To clear the stored dataset just delete every line except the header, and make sure there is a newline after if (there should be two lines in the file, line 1 with the headings, and line 2 should exist, but not contain anything)
