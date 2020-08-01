"""
customtablemode.py
2020/07/31 15:33
"""
import operator
from PySide2 import QtWidgets
from PySide2 import QtGui
from PySide2 import QtCore


# class MyWindow(QtWidgets.QWidget):
#     def __init__(self, data_list, header, *args):
#         QtWidgets.QWidget.__init__(self, *args)
#         # setGeometry(x_pos, y_pos, width, height)
#         self.setGeometry(300, 200, 570, 450)
#         self.setWindowTitle("Click on column title to sort")
#         table_model = MyTableModel(self, data_list, header)
#         table_view = QtWidgets.QTableView()
#         table_view.setModel(table_model)
#         # set font
#         font = QtGui.QFont("Courier New", 14)
#         table_view.setFont(font)
#         # set column width to fit contents (set font first!)
#         table_view.resizeColumnsToContents()
#         # enable sorting
#         table_view.setSortingEnabled(True)
#         layout = QtWidgets.QVBoxLayout(self)
#         layout.addWidget(table_view)
#         self.setLayout(layout)


class MyTableModel(QtCore.QAbstractTableModel):
    def __init__(self, parent, mylist, header, *args):
        QtCore.QAbstractTableModel.__init__(self, parent, *args)
        self.mylist = mylist
        self.header = header

    def rowCount(self, parent):
        return len(self.mylist)

    def columnCount(self, parent):
        return len(self.mylist[0])

    def data(self, index, role):
        if not index.isValid():
            return None
        elif role != QtCore.Qt.DisplayRole:
            return None
        return self.mylist[index.row()][index.column()]

    def headerData(self, col, orientation, role):
        if orientation == QtCore.Qt.Horizontal and role == QtCore.Qt.DisplayRole:
            return self.header[col]
        return None

    def sort(self, col, order):
        """sort table by given column number col"""
        self.emit(QtCore.SIGNAL("layoutAboutToBeChanged()"))
        self.mylist = sorted(self.mylist,
                             key=operator.itemgetter(col))
        if order == QtCore.Qt.DescendingOrder:
            self.mylist.reverse()
        self.emit(QtCore.SIGNAL("layoutChanged()"))
