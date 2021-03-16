from PySide2.QtWidgets import QPushButton, QLineEdit, QApplication, QFormLayout, QWidget, QTextEdit, QMessageBox, QSpinBox
from PySide2.QtCore import QObject, QRunnable, QThreadPool, Signal, Slot

#Frame work gathered from below 
#https://www.learnpyqt.com/examples/python-pdf-report-generator/


from reportlab.pdfgen.canvas import Canvas

import os

import textwrap
from datetime import datetime

from pdfrw import PdfReader
from pdfrw.buildxobj import pagexobj
from pdfrw.toreportlab import makerl

class WorkerSignals(QObject):
    error = Signal(str)
    file_saved_as = Signal(str)


class Generator(QRunnable):
    def __init__(self, data):
        super().__init__()
        self.data = data
        self.signals = WorkerSignals()

    @Slot()
    def run(self):
        try:
            outfile = "result.pdf"

            template = PdfReader("template.pdf", decompress=False).pages[0]
            template_obj = pagexobj(template)

            canvas = Canvas(outfile)

            xobj_name = makerl(canvas, template_obj)
            canvas.doForm(xobj_name)

            canvas.drawString(230, 610, self.data['totalTickets'])

            canvas.drawString(240, 576, self.data['serviceTickets'])

            canvas.drawString(250, 545, self.data['incidentTickets'])

            canvas.drawString(275, 512, self.data['unassignedTickets'])

            canvas.drawString(89, 457, self.data['reasonOne'])

            canvas.drawString(89, 430, self.data['reasonTwo'])

            canvas.drawString(89, 406, self.data['reasonThree'])

            additionalNotes = self.data['additionalNotes'].replace('\n', ' ')
            if additionalNotes:
                lines = textwrap.wrap(additionalNotes, width=55)
                first_line = lines[0]
                remainder = ' '.join(lines[1:])

                lines = textwrap.wrap(remainder, 50) # 55
                lines = lines[:3]  # max lines, not including the first.

                canvas.drawString(170, 375, first_line)
                for n, l in enumerate(lines, 1):
                    canvas.drawString(71, 350, l)

            canvas.save()

        except Exception as e:
            self.signals.error.emit(str(e))
            return

        self.signals.file_saved_as.emit(outfile)

class Window(QWidget):

    def __init__(self):
        super().__init__()

        self.threadpool = QThreadPool()

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
        self.generate_btn.pressed.connect(self.generate)

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

    def generate(self):
        self.generate_btn.setDisabled(True)
        data = {
            'totalTickets': str(self.totalTickets.value()),
            'serviceTickets': str(self.serviceTickets.value()),
            'incidentTickets': str(self.incidentTickets.value()),
            'unassignedTickets': str(self.unassignedTickets.value()),
            'reasonOne': self.reasonOne.text(),
            'reasonTwo': self.reasonTwo.text(),
            'reasonThree':self.reasonThree.text(),
            'additionalNotes': self.additionalNotes.toPlainText()
        }
        g = Generator(data)
        g.signals.file_saved_as.connect(self.generated)
        g.signals.error.connect(print)  # Print errors to console.
        self.threadpool.start(g)

    def generated(self, outfile):
        self.generate_btn.setDisabled(False)
        try:
            os.startfile(outfile)
        except Exception:
            # If startfile not available, show dialog.
            QMessageBox.information(self, "Finished", "PDF has been generated")



app = QApplication([])
w = Window()
w.show()
app.exec_()
