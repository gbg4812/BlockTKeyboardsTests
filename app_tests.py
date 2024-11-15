from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import (
    QApplication,
    QDialog,
    QDialogButtonBox,
    QFileDialog,
    QInputDialog,
    QLineEdit,
    QLabel,
    QFrame,
    QPushButton,
    QVBoxLayout,
)
from PyQt6.QtCore import QThread, pyqtSignal, pyqtSlot, QObject, QTimer, Qt


class TextPrompter(QObject):
    def __init__(self) -> None:
        super().__init__(None)

        self.txt = []
        self.current = 0
        self.test_time = 60

        # time
        self.update_timer = QTimer()
        self.update_timer.timeout.connect(self.update_timer_label)
        self.update_timer.start(250)

        self.test_timer = QTimer()
        self.test_timer.setSingleShot(True)
        self.test_timer.timeout.connect(self.end_test)

        # QWidgets
        self.layout = QVBoxLayout()
        self.wndw = QFrame()

        self.infile = QLabel()
        self.browsefile = QPushButton("Browse File")
        self.label = QLabel()
        self.infield = QLineEdit()
        self.timerlab = QLabel()
        self.edittimer = QPushButton("Edit Test Time")

        # Config Widgets
        self.wndw.setLayout(self.layout)

        self.browsefile.clicked.connect(self.search_file)

        font = QFont("Arial", 16)
        self.label.setWordWrap(True)
        self.label.setFont(font)

        self.infield.setFont(font)
        self.infield.textEdited.connect(self.update_current_word)
        self.infield.setReadOnly(True)

        self.timerlab.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.timerlab.setFont(font)

        self.edittimer.clicked.connect(self.set_test_time)

        self.layout.addWidget(self.infile)
        self.layout.addWidget(self.browsefile)
        self.layout.addWidget(self.label, stretch=10)
        self.layout.addWidget(self.infield)
        self.layout.addWidget(self.timerlab)
        self.layout.addWidget(self.edittimer)

        self.wndw.show()

    @pyqtSlot(str)
    def update_current_word(self, text: str):
        if not self.test_timer.isActive():
            self.test_timer.start(self.test_time * 1000)

        if text == self.txt[self.current] + " ":
            self.current += 1
            self.infield.clear()
            if self.current < len(self.txt):
                self.update_label()
            else:
                self.label.setText(
                    "The input text was to short for this magnificent competitor!"
                )

    @pyqtSlot()
    def update_timer_label(self):
        if self.test_timer.isActive():
            self.timerlab.setText(
                "{}s".format(int(self.test_timer.remainingTime() / 1000))
            )
        else:
            self.timerlab.setText(f"{self.test_time}s")

    @pyqtSlot()
    def end_test(self):
        characters = 0
        for wrd in self.txt[: self.current]:
            characters += len(wrd)
        wpm = float(self.current / float(self.test_time)) * 60.0
        ccpm = int(float(characters / float(self.test_time)) * 60.0)
        self.label.setText(
            f"Finished! WPM: {wpm}\nYou have writen {self.current} correct words!\nCCPM: {ccpm}"
        )
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.infield.clear()
        self.infield.setReadOnly(True)

    def update_label(self):
        txt = ""
        for i, word in enumerate(self.txt):
            if i == self.current:
                txt += f'<font color="red">{word}</font> '
            else:
                txt += f"{word} "
        # print(f"updating label current: {self.current}")
        self.label.setText(txt)

    @pyqtSlot(str)
    def create_test(self, path: str):
        self.test_timer.stop()
        self.infield.clear()
        self.label.setAlignment(Qt.AlignmentFlag.AlignJustify)

        with open(path, "r") as f:
            self.txt = f.readlines()

        for i, word in enumerate(self.txt):
            self.txt[i] = word.replace("\n", "")

        self.current = 0
        self.infield.setReadOnly(False)
        self.update_label()

    @pyqtSlot()
    def search_file(self):
        fdig = QFileDialog()
        fdig.fileSelected.connect(self.create_test)
        fdig.exec()

    @pyqtSlot()
    def set_test_time(self):
        new_time = QInputDialog.getInt(
            self.wndw,
            "Set Test Time",
            "Time",
        )
        if new_time[1] and new_time[0] > 0:
            self.test_time = new_time[0]


app = QApplication([])
prompter = TextPrompter()

app.exec()
