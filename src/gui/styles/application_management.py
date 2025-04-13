application = """
QFrame {
    background-color: #A8A8A8;
    border: 2px solid #7A7A7A;
    border-radius: 0px;
    padding: 5px;
}

QLabel {
    background-color: transparent;
    border: 0px;
    border-radius: 0px;
    padding: 0px 0px;
    font-family: "Roboto";
    font-size: 12px;
    font-weight: none;
    color: #000000;
    margin: 0px 0px;
}

QPushButton {
    background-color: #A8A8A8;
    color: #000000;
    border: 0px solid #7A7A7A;
    border-radius: 0px;
    margin: 0px 0px;
    font-family: "Roboto";
    font-size: 12px;
    width: 75px;
    height: 40px;
}

QPushButton:hover, 
QPushButton:checked {
    border: 2px solid #7A7A7A;
    border-radius: 4px;
    background: #7A7A7A;
}

QLineEdit {
    background-color: #D8D8D8;
    color: #000000;
    border: 1px solid #7A7A7A;
    border-radius: 2px;
    font-family: "Roboto";
    font-size: 12px;
    padding: 2px 5px;
}

QLineEdit:placeholder-text {
    color: #B2B2B2;              
}

QComboBox {
    background-color: #B9B9B9;
    border: 1px solid #7A7A7A;
    border-radius: 2px;
    font-family: "Roboto";
    font-size: 12px;
    color: #000000;
    padding: 0px 5px;
    width: 150px;
    height: 70px;
}

QComboBox QAbstractItemView {
    border: 0px solid #7A7A7A;       
    background-color: #D8D8D8;        
    margin: 0px;                      
    padding: 0px;                     
    outline: 0px;
    height: 50px;      
}
"""

menu_btn = """
QPushButton {
    background-color: #A8A8A8;
    color: #000000;
    border: 0px solid #7A7A7A;
    border-radius: 0px;
    margin: 0px 0px;
    font-family: "Roboto";
    font-size: 12px;
    font-weight: normal;      
}

QPushButton#delete_duplicate {
    background-color: #A8A8A8;
    color: #000000;
    border: 0px solid #7A7A7A;
    border-radius: 0px;
    margin: 0px 0px;
    font-family: "Roboto";
    font-size: 12px;
    font-weight: normal;
    height: 30px;
    width: 150px;     
}

QPushButton:hover, 
QPushButton:checked {
    background-color: #B4B4B4;
    border: 1px solid #7A7A7A;
    border-radius: 3px;
    width: 150px;
}

QPushButton:hover#delete_duplicate {
    background-color: #B4B4B4;
    border: 1px solid #7A7A7A;
    border-radius: 3px;
}

QPushButton#metric_button {
    background-color: #A8A8A8;
    border: 0px solid #7A7A7A;
    border-radius: 0px;
    padding: 0px;
}

QPushButton#metric_button:hover {
    background-color: #B4B4B4;
    border: 1px solid #7A7A7A;
    border-radius: 3px;
}
"""

menu_item = """
QMenu {
    background: #B9B9B9;
    color: #000000;
    border: 1px solid #7A7A7A;
    border-radius: 4px;
    padding: 2px;
    width: 140px;
    height: 70px;
}

QMenu#openNewSessionMenu {
    background: #B9B9B9;
    color: #000000;
    border: 1px solid #7A7A7A;
    border-radius: 4px;
    padding: 2px;
    width: 200px;
    height: 40px;
}

QMenu#openSessionMenu {
    background: #B9B9B9;
    color: #000000;
    border: 1px solid #7A7A7A;
    border-radius: 4px;
    padding: 2px;
    width: 140px;
    height: 120px;
}

QMenu#metricTitle  {
    background: #B9B9B9;
    color: #000000;
    border: 1px solid #7A7A7A;
    border-radius: 4px;
    padding: 2px;
    width: 350px;
    height: 120px;
}

QMenu#ExportTitle  {
    background: #B9B9B9;
    color: #000000;
    border: 1px solid #7A7A7A;
    border-radius: 4px;
    padding: 2px;
    width: 400px;
    height: 180px;
}

QMenu::item {
    padding: 5px 10px;
    border: 1px solid #7A7A7A;
    border-radius: 4px;
    width: 140px;
    height: 10px;
}


QLabel {
    background-color: #B9B9B9;
    border: 0px;
    border-radius: 0px;
    padding: 0px 0px;
    font-family: "Roboto";
    font-size: 12px;
    font-weight: none;
    color: #000000;
    margin: 0px 0px;
}

QLabel#openSessionMenu {
    background-color: #AFAFAF;
    border: 0px;
    border-radius: 0px;
    padding: 0px 0px;
    font-family: "Roboto";
    font-size: 12px;
    font-weight: none;
    color: #000000;
    margin: 0px 0px;
}

QLabel#metricTitle {
    background-color: #B9B9B9;
    border: 0px;
    border-radius: 0px;
    padding: 0px 0px;
    font-family: "Roboto";
    font-size: 12px;
    font-weight: bold;
    color: #1C3C50;
    margin: 0px 0px;
}

QWidget {
    background-color: #B9B9B9;
}
"""

icon_button_style = """
QPushButton[class="icon_button"] {
    background: #A8A8A8;
    border: 0px solid transparent;
    border-radius: 4px;
    padding: 5px;
}

QPushButton[class="icon_button"]:hover {
    background: #B4B4B4;
    border: 1px solid #7A7A7A;
}

QPushButton[class="icon_button"]:checked {
    background: #888888;
    border: 1px solid #7A7A7A;
}

QPushButton[class="icon_button"]:pressed {
    background: #777777;
}
"""