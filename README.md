## Time Management/Calculation App
Voluntarily developed for [Newport Corporation](https://www.newport.com/)

![A quick look at the GUI](https://github.com/Frenchman98/PlanetTimeMgmtApp/blob/master/demo.gif)

### Instructions
- If you are looking for an executable, head to the [releases](https://github.com/Frenchman98/PlanetTimeMgmtApp/releases) and download the latest one, or click [here](https://github.com/Frenchman98/PlanetTimeMgmtApp/releases/download/v0.5/app.exe).
- If you are looking to test this and run the python code
    - Clone the repository
    - Before first run, launch the build-gui-files.bat file (Only has to be done once after cloning/pulling new version)
    - Run the app.py script
##
### Notes
- Waiting on response from Newport Corporation on functionality that they would like to see implemented, or removed, to continue with development.

- Currently on first working version. Missing functionality is:
   - Tabs 2 & 3
   - Time calculation (other than machine time) in table
   
- Developed with expansion in mind, so expanding from 1 to 3 tabs (or more) should require minimal modifications to code, most of which are already labeled as todo items. Also, optimization was not the focus, simply functionality, since it is a relatively small application. 

- There is one mistake I made in terms of development that causes it to be quite a bit slower than it could be (which is not storing planets within the machines), but I only thought of this after having written most of the code. May restructure to fix this later.
