# Glean ChitChat Client

![Static Badge](https://img.shields.io/badge/Glean-Chat_API-green?style=flat)
![Static Badge](https://img.shields.io/badge/Visual_Studio_Code-blue?style=flat)
![Static Badge](https://img.shields.io/badge/Python-yellow?style=flat)

![Glean ChitChat](assets/Create_Your_Own_ChatApp.png)

## Getting Started

Example of a simple Glean Chat API client created with Python. 

Blog post @ [Gleaning Ideas](https://gleaningideas.ai).

### Dependencies

```python
# Libraries
import sys
import requests
import json
import markdown

# UI elements
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QTextBrowser, QPushButton, QComboBox
```

### Installing

The chitchat client can be run without Visual Studio Code using ```python3 GleanChitChat.py```. Before executing install libraries for GUI elements and Markdown:

```python
pip3 install PyQt5
pip3 install markdown
```

## Help

Requests or problems? Please use [Issue Tracking](https://github.com/rob-barker-glean/chitchat/issues).

## Version History

* 0.1
  * Authentication
  * Send and recieve requests.

## Roadmap

* Annotations
* Persisted questions
* Customizable GUI logo
* Result output to document

## Authors

Rob Barker, rob.barker@glean.com, hit me up on [Bluesky](https://bsky.app/profile/robbarker.bsky.social).