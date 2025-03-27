import os
import time
import webbrowser
import pyautogui
import pyperclip
from flask import Flask, request, redirect

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def upload_form():
    return '''
    <!doctype html>
    <html>
    <body>
        <h2>Upload an Image</h2>
        <form action="/upload" method="post" enctype="multipart/form-data">
            <input type="file" name="file">
            <input type="submit" value="Upload">
        </form>
    </body>
    </html>
    '''

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return "No file part"
    file = request.files['file']
    if file.filename == '':
        return "No selected file"
    if file:
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filepath)
        
        # Open ChatGPT in a browser
        webbrowser.open("https://chat.openai.com/")
        time.sleep(3)  # Wait for the page to load

        # Copy image path to clipboard
        pyperclip.copy(os.path.abspath(filepath))

        # Open file dialog (Windows: Ctrl+L in File Explorer)
        pyautogui.hotkey("win", "r")
        time.sleep(1)
        pyautogui.typewrite(os.path.abspath(filepath), interval=0.1)
        pyautogui.press("enter")
        time.sleep(2)

        # Copy image to clipboard (Windows)
        pyautogui.hotkey("ctrl", "c")
        time.sleep(1)

        # Switch back to browser
        pyautogui.hotkey("alt", "tab")
        time.sleep(1)

        # Paste image in chat
        pyautogui.hotkey("ctrl", "v")
        time.sleep(3)
        pyautogui.typewrite("read and provide me json data")
        time.sleep(1)
        pyautogui.press("enter")

        return "File uploaded and sent to ChatGPT!"

if __name__ == '__main__':
    app.run(debug=True)

# import os
# import time
# import webbrowser
# import pyautogui
# import pyperclip
# from flask import Flask, request, jsonify
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC

# # Flask setup
# app = Flask(__name__)
# UPLOAD_FOLDER = 'uploads'
# os.makedirs(UPLOAD_FOLDER, exist_ok=True)
# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# # Selenium ChromeDriver setup
# CHROME_DRIVER_PATH = r"C:/Users/skprj/Downloads/134.0.6998.35 chromedriver-win64/chromedriver.exe"

# service = Service(CHROME_DRIVER_PATH)
# options = webdriver.ChromeOptions()
# options.add_argument("--start-maximized")

# @app.route('/')
# def upload_form():
#     return '''
#     <!doctype html>
#     <html>
#     <body>
#         <h2>Upload an Image</h2>
#         <form action="/upload" method="post" enctype="multipart/form-data">
#             <input type="file" name="file">
#             <input type="submit" value="Upload">
#         </form>
#     </body>
#     </html>
#     '''

# @app.route('/upload', methods=['POST'])
# def upload_file():
#     if 'file' not in request.files:
#         return "No file part"
#     file = request.files['file']
#     if file.filename == '':
#         return "No selected file"
    
#     if file:
#         filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
#         file.save(filepath)

#         # Open ChatGPT in Chrome
#         driver = webdriver.Chrome(service=service, options=options)
#         driver.get("https://chat.openai.com/")
#         wait = WebDriverWait(driver, 20)

#         try:
#             # If login is required, handle it
#             if "login" in driver.current_url:
#                 print("Logging in required. Please log in manually.")
#                 time.sleep(30)  # Allow user to log in
#                 driver.get("https://chat.openai.com/")  # Reload after login
            
#             # Locate input box and send request
#             input_box = wait.until(EC.presence_of_element_located((By.TAG_NAME, "textarea")))
#             input_box.send_keys("Extract data in JSON format")
#             input_box.send_keys(Keys.ENTER)

#             # Wait for ChatGPT to generate a response
#             time.sleep(10)

#             # Find and click the last "Copy" button
#             copy_button_script = """
#             let buttons = document.querySelectorAll('button[aria-label="Copy"]');
#             if (buttons.length > 0) {
#                 buttons[buttons.length - 1].click();
#             }
#             """
#             driver.execute_script(copy_button_script)
#             time.sleep(2)

#             # Get copied JSON from clipboard
#             extracted_json = pyperclip.paste()
#         finally:
#             driver.quit()  # Ensure browser closes

#         return jsonify({"Extracted JSON": extracted_json})

# if __name__ == '__main__':
#     app.run(debug=True)
