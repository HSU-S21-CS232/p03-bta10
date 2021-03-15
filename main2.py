from PySide2.QtWidgets import QPushButton, QLineEdit, QApplication, QFormLayout, QWidget, QTextEdit, QSpinBox


class Window(QWidget):

    def __init__(self):
        super().__init__()

        self.totalTickets = QSpinBox()
        self.totalTickets.setRange(0, 500)
        self.serviceTickets = QSpinBox()
        self.serviceTickets.setRange(0, 250)
        self.incidentTickets = QSpinBox()
        self.incidentTickets.setRange(0, 250)
        self.unassignedTickets = QSpinBox()
        self.unassignedTickets.setRange(0, 200)
        self.reasonOne = QLineEdit()
        self.reasonTwo = QLineEdit()
        self.reasonThree = QLineEdit()
        self.additionalNotes  = QTextEdit()

        self.generate_btn = QPushButton("Generate PDF")

        layout = QFormLayout()
        layout.addRow("Number of tickets today", self.totalTickets)
        layout.addRow("Service tickets", self.serviceTickets)
        layout.addRow("Incident tickets", self.incidentTickets)
        layout.addRow("Unassigned tickets", self.unassignedTickets)
        layout.addRow("Reason for most tickets", self.reasonOne)
        layout.addRow("Second reason for most tickets", self.reasonTwo)
        layout.addRow("Third reason for most tickets", self.reasonThree)

        layout.addRow("additionalNotes", self.additionalNotes)
        layout.addRow(self.generate_btn)

        self.setLayout(layout)


app = QApplication([])
w = Window()
w.show()
app.exec_()
