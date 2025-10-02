
## Python

### Windows & Mac:
Here are the steps to install Python and add it to your system's PATH:

- Download that latest official version of Python https://www.python.org/downloads/.
- Choose the appropriate installer for your operating system (Windows: Windows x86-64 executable installer, macOS: macOS 64-bit installer)
- Run the installer, ensuring that you select "Add Python to PATH" during the installation
- After the installation has finisihed, open a terminal window and enter "python" to test that it is callable from the terminal 


### Linux:

Open a terminal window and install Python by running the following commands:


```
sudo apt update
sudo apt install python3
```

Verify that Python has been installed correctly by entering the following command:


```
python3 --version
```

Add Python to your PATH by opening the ~/.bashrc file in your home directory:

```
nano ~/.bashrc
```

Add the following line to the end of the file:

```
export PATH=$PATH:/usr/bin/python3
```


Save the changes and exit the editor and reload your bashrc file so the changes take effect: 

```
source ~/.bashrc
```

Test that python was successfully installed by calling python in the terminal:
```
python3
```
