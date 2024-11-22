from PyQt5.QtWidgets import QApplication
from ui.login_page import LoginPage #Import the first UI page 
import sys 

# For my own reference on colour scheme:
# Colour Palette:
# Primary: Dark Grey (#2C3E50)
# Accent: Electric Blue (#3498DB)
# Neutral: Very Light Grey (#ECF0F1)
# Error: Scarlet (#C0392B)
# Success: Neon Green (#2ECC71)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # Apply the stylesheet
    try:
        with open("styles/app_styles.qss", "r") as style_file:
            app.setStyleSheet(style_file.read())
    except FileNotFoundError:
        print("Stylesheet file not found. Default style will be used.")
    
    login_window = LoginPage()
    login_window.login_successful.connect(lambda: print("Login Successful!"))  # Placeholder
    login_window.show()
    
    sys.exit(app.exec_())