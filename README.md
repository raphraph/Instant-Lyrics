<div align="center">
<h1>Instant-Lyrics</h1>
<h2>Instantly fetches the lyrics of the currently playing song and displays it on a window.</h2>
<em>A linux application with a very convenient GUI. Built with Python 3 Gtk+3 (gi).</em></br></br>
</div>
</br>

# Screenshot
![Screenshot](https://cloud.githubusercontent.com/assets/6123105/23824316/3fe58044-069a-11e7-804e-180ea4041002.jpeg)

# Working example
![Working](https://cloud.githubusercontent.com/assets/6123105/23824730/e0e0829e-06a1-11e7-8d57-3235c4266f2c.gif)

# Compatibility
- Python 3
- Linux

# Installation

### system requirements (use `apt`, `pacman`, `dnf` ... your package manager):
- python-gi (PyGObject)
- python-dbus
- AppIndicator3

### python requirements (use `pip2` or `pip3`):
- requests
- beautifulsoup4
- lxml


First, install the requirements:

### For Ubuntu/Debian based systems:

``` bash
sudo apt install python-gi python-dbus gir1.2-appindicator3-0.1 python-requests python-bs4 python-lxml
```

### For Arch users

``` bash
sudo pacman -S python3-dbus python3-requests python3-lxml python3-beautifulsoup4 python3-gobject libappindicator-gtk3
```

### Fedora

``` bash
sudo dnf install dbus-python python-gobject libappindicator-gtk3 python3-requests python-beautifulsoup4 python3-lxml
```

Then, enter the commands:

``` bash
git clone https://github.com/bhrigu123/Instant-Lyrics.git
cd Instant-Lyrics/
pip3 install .# this installs requests, lxml and bs4
instantlyrics  # `instantlyrics.py &` to keep it running in background
```

The icon will appear in the system tray (indicator panel). You can start using the application from there.

<br>

# Creating a launcher shortcut

If you have installed from source, you can go to **Preferences** from the menu options, and click on the button `Create Desktop Entry`.
You should be able to see the `Instant Lyrics` application shortcut in your launcher menu.
You can also find several manual ways of doing so from the web.

![Launcher](https://cloud.githubusercontent.com/assets/6123105/23824317/4735e83e-069a-11e7-8b1e-2814632bb3aa.jpeg)


# Contribution
Create an issue to discuss the changes/modifications before sending a PR.

# Icon Credits
Icon made by [Freepik](http://www.freepik.com/) from www.flaticon.com

# License
## The MIT License
> Copyright (c) 2017 Bhrigu Srivastava http://bhrigu.me

> Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

> The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

> THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

