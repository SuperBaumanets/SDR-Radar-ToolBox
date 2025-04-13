table_characterictics = """
QTableWidget {
    background-color: #c0c0c0;
    gridline-color: #000000;
    border: 1px solid #000000;
    border-radius: 0px;
    font-family: "Roboto";
    font-size: 14px;
}

QHeaderView::section {
    background-color: #7A7A7A;
    color: #000000;
    padding: 4px;
    border: 1px solid #000000;
    font-weight: bold;
    font-family: "Roboto";
    font-size: 14px;
}

QTableView::item {
    background-color: transparent;
    color: black;
    border-bottom: 1px solid #000000;
    padding: 0px;
}

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
    background-color: transparent;
    color: #000000;
    border: 0px solid #000000;
    border-radius: 0px;
    font-family: "Roboto";
    font-size: 14px;
    padding: 2px 5px;
    width: 300px;
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
    border-radius: 0px;
    font-family: "Roboto";
    font-size: 14px;
    color: #000000;
    padding: 0px 5px;
    width: 50px;
    height: 40px;
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
    width: 50px;    
}

QComboBox QAbstractItemView::item {
    color: #FFFFFF;
}
"""