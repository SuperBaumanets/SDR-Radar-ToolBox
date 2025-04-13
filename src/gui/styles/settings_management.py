headline_settings = """
QLabel {
    background-color: transparent;
    border: 0px;
    border-radius: 0px;
    padding: 0px 0px;
    font-family: "Roboto";
    font-size: 14px;
    font-weight: none;
    color: #000000;
    margin: 0px 0px;
}

QLineEdit {
    background-color: #D8D8D8;
    color: #000000;
    border: 1px solid #000000;
    border-radius: 2px;
    font-family: "Roboto";
    font-size: 14px;
    padding: 2px 5px;
    height: 20px;
}

QLineEdit:focus {
    background-color: #D8D8D8;
    color: #000000;
}

QLineEdit:placeholder-text {
    color: #B2B2B2;              
}

QComboBox {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
        stop:0 #BEBEBE, stop:0.3 #D8D8D8, stop:0.7 #D8D8D8, stop:1 #BEBEBE);
    border: 1px solid #000000;
    border-radius: 2px;
    font-family: "Roboto";
    font-size: 14px;
    color: #000000;
    padding: 0px 5px;
    width: 410px;
    height: 70px;
    selection-background-color: #2196F3;
    selection-color: #FFFFFF;
}

QComboBox::drop-down {
    subcontrol-origin: padding;
    subcontrol-position: right;
    width: 20px;
    border-left: 1px solid #7A7A7A;
    image: url(src/resources/icons/arrow_down.svg);
}

QComboBox QAbstractItemView {
    border: 1px solid #000000;       
    background-color: #D8D8D8;       
    margin: 0px;                      
    padding: 0px;                     
    outline: 0px;
    height: 50px;      
}

QComboBox QAbstractItemView::item {
    color: #FFFFFF;
}
"""

main_settings = """
QLabel {
    background-color: transparent;
    border: 0px;
    border-radius: 0px;
    padding: 0px 0px;
    font-family: "Roboto";
    font-size: 14px;
    font-weight: none;
    color: #000000;
    margin: 0px 0px;
    width: 230px;
}

QLineEdit {
    background-color: #D8D8D8;
    color: #000000;
    border: 1px solid #000000;
    border-radius: 2px;
    font-family: "Roboto";
    font-size: 14px;
    padding: 2px 5px;
    width: 300px;
    height: 16px;
}

QLineEdit:focus {
    background-color: #D8D8D8;
    color: #000000;
}

QLineEdit:placeholder-text {
    color: #B2B2B2;              
}

QComboBox {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
        stop:0 #BEBEBE, stop:0.3 #D8D8D8, stop:0.7 #D8D8D8, stop:1 #BEBEBE);
    border: 1px solid #000000;
    border-radius: 2px;
    font-family: "Roboto";
    font-size: 14px;
    color: #000000;
    padding: 0px 5px;
    width: 150px;
    height: 20px;
    selection-background-color: #2196F3;
    selection-color: #FFFFFF;
}

QComboBox#measurement {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
        stop:0 #BEBEBE, stop:0.3 #D8D8D8, stop:0.7 #D8D8D8, stop:1 #BEBEBE);
    border: 1px solid #000000;
    border-radius: 2px;
    font-family: "Roboto";
    font-size: 14px;
    color: #000000;
    padding: 0px 5px;
    width: 60px;
    height: 20px;
    selection-background-color: #2196F3;
    selection-color: #FFFFFF;
}

QComboBox::drop-down {
    subcontrol-origin: padding;
    subcontrol-position: right;
    width: 20px;
    border-left: 1px solid #7A7A7A;
    image: url(src/resources/icons/arrow_down.svg);
}

QComboBox QAbstractItemView {
    border: 1px solid #000000;       
    background-color: #D8D8D8;       
    margin: 0px;                      
    padding: 0px;                     
    outline: 0px;
    height: 50px;      
}

QComboBox QAbstractItemView::item {
    color: #FFFFFF;
}
"""


antenna_settings = """
QLabel {
    background-color: transparent;
    border: 0px;
    border-radius: 0px;
    padding: 0px 0px;
    font-family: "Roboto";
    font-size: 14px;
    font-weight: none;
    color: #000000;
    margin: 0px 0px;
    width: 50px;
}

QLineEdit {
    background-color: #D8D8D8;
    color: #000000;
    border: 1px solid #000000;
    border-radius: 2px;
    font-family: "Roboto";
    font-size: 14px;
    padding: 2px 5px;
    width: 200px;
    height: 16px;
}

QLineEdit:focus {
    background-color: #D8D8D8;
    color: #000000;
}

QLineEdit:placeholder-text {
    color: #B2B2B2;              
}

QComboBox {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
        stop:0 #BEBEBE, stop:0.3 #D8D8D8, stop:0.7 #D8D8D8, stop:1 #BEBEBE);
    border: 1px solid #000000;
    border-radius: 2px;
    font-family: "Roboto";
    font-size: 14px;
    color: #000000;
    padding: 0px 5px;
    width: 330px;
    height: 20px;
    selection-background-color: #2196F3;
    selection-color: #FFFFFF;
}

QComboBox#measurement {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
        stop:0 #BEBEBE, stop:0.3 #D8D8D8, stop:0.7 #D8D8D8, stop:1 #BEBEBE);
    border: 1px solid #000000;
    border-radius: 2px;
    font-family: "Roboto";
    font-size: 14px;
    color: #000000;
    padding: 0px 5px;
    width: 60px;
    height: 20px;
    selection-background-color: #2196F3;
    selection-color: #FFFFFF;
}

QComboBox::drop-down {
    subcontrol-origin: padding;
    subcontrol-position: right;
    width: 20px;
    border-left: 1px solid #7A7A7A;
    image: url(src/resources/icons/arrow_down.svg);
}

QComboBox QAbstractItemView {
    border: 1px solid #000000;       
    background-color: #D8D8D8;       
    margin: 0px;                      
    padding: 0px;                     
    outline: 0px;
    height: 50px;      
}

QComboBox QAbstractItemView::item {
    color: #FFFFFF;
}

QCheckBox {
    font: 14px;
    color: #000000;
    width: 16px;
    height: 16px;
}

QCheckBox::indicator {
    width: 16px;
    height: 16px;
}
"""

tab_style = """
QTabWidget::pane {
    border: 2px solid #7A7A7A;
    border-top-left-radius: 6px;
    border-top-right-radius: 6px;
}

QTabBar::tab {
    background: #7A7A7A;
    color: black;
    border: 1px solid #000000;
    border-top-left-radius: 6px;
    border-top-right-radius: 6px;
    padding: 8px 12px;
    margin-right: 0px;
}

QTabBar::tab:selected {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                               stop:0 #90ACAF, stop:1 transparent);
    color: black;
    border: 1px solid #000000;
    border-bottom: none;
}

QTabBar::tab:hover {
    background:qlineargradient(x1:0, y1:0, x2:0, y2:1,
                               stop:0 #AFAFAF, stop:1 transparent);
}

QTabBar {
    background: transparent;
}
"""