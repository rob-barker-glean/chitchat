# Core libraries to handle HTTP requests and responses
import sys
import requests
import json

# Markdown library to convert markdown to HTML
import markdown

# UI elements from PyQt5
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QSize
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QTextBrowser, QPushButton, QComboBox, QSpacerItem, QSizePolicy

API_KEY = '<YOUR_API_KEY>'
CHATBOT_ENDPOINT = 'https://<YOUR_GLEAN_URL>/rest/api/v1/chat'

def authenticate():
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {API_KEY}'
    }
    
    response = requests.post(CHATBOT_ENDPOINT, headers=headers)
    
    if response.status_code == 200:
        return response.json().get('token')
    else:
        response.raise_for_status()

def send_chatbot_request(message):
    # token = authenticate()
    
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {API_KEY}'
    }
    
    payload = {
        'stream': False, # Set to False to toggle off streaming mode
        'messages': [{
            'author': 'USER',
            'fragments': [{'text': message}]
        }],
    }
    
    # Debugging print statements
    print("Headers:", headers)
    print("Payload:", json.dumps(payload, indent=2))
    
    response = requests.post(CHATBOT_ENDPOINT, headers=headers, data=json.dumps(payload))
    
    if response.status_code == 200:
        return response.json()
    else:
        print("Response Status Code:", response.status_code)
        print("Response Content:", response.content)
        response.raise_for_status()

def process_message_fragment(message):
    message_type = message['messageType']
    fragments = message.get('fragments', [])
    citations = message.get('citations', [])

    result = ""
    if message_type == 'CONTENT':
        if fragments:
            for fragment in fragments:
                text = fragment.get('text', '')
                result += text
        if citations:
            result += '\nSources:\n'
            for idx, citation in enumerate(citations):
                sourceDocument = citation.get('sourceDocument', {})
                if sourceDocument:
                    source = citation['sourceDocument']
                    result += f'Source {idx + 1}: {source["title"]}, url: <a href="{source["url"]}">{source["url"]}</a>\n'
                sourcePerson = citation.get('sourcePerson', {})
                if sourcePerson:
                    source = citation['sourcePerson']
                    result += f'Source {idx + 1}: Person name - {source["name"]}\n'
                else:
                    result += f'No source information available.\n'
    return result

class GleanChitChatUI(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
    
    def initUI(self):
        self.setWindowTitle('Glean ChitChat')
 
        main_layout = QVBoxLayout()
        
        self.message_label = QLabel('What can I help you find?')
        main_layout.addWidget(self.message_label)
        
        self.message_input = QLineEdit()
        main_layout.addWidget(self.message_input)
        
        self.send_button = QPushButton('Ask Glean')
        self.send_button.clicked.connect(self.on_send)
        main_layout.addWidget(self.send_button)
        
        self.response_text = QTextBrowser()
        self.response_text.setOpenExternalLinks(True)  # Enable clickable links
        main_layout.addWidget(self.response_text)
        
        self.history_label = QLabel('Query History:')
        main_layout.addWidget(self.history_label)
        
        self.message_history = QComboBox()
        self.message_history.currentIndexChanged.connect(self.on_history_selected)
        main_layout.addWidget(self.message_history)
        
        # Create a horizontal layout for the image and main layout
        top_layout = QHBoxLayout()
        top_layout.addItem(QSpacerItem(10, 10, QSizePolicy.Expanding, QSizePolicy.Minimum))
        
        # Add the top layout to the main layout
        main_layout.insertLayout(0, top_layout)
        
        self.setLayout(main_layout)
    
    def on_send(self):
        user_message = self.message_input.text().strip()
        if user_message:
            try:
                response = send_chatbot_request(user_message)
                messages = response.get('messages', [])
                result = ""
                for message in messages:
                    result += process_message_fragment(message)
                self.response_text.append(f"What did you ask for?<br> <b>{user_message}</b><br>")
                self.response_text.append(f"{markdown.markdown(result)}<br><hr>")  # Convert Markdown to HTML
                self.message_input.clear()
                self.message_history.addItem(user_message)  # Add message to history
            except Exception as e:
                self.response_text.append(f"<b>Error:</b> {str(e)}<br><hr>")
    
    def on_history_selected(self, index):
        if index >= 0:
            selected_message = self.message_history.itemText(index)
            self.message_input.setText(selected_message)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    gui = GleanChitChatUI()
    gui.show()
    sys.exit(app.exec_())