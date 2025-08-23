from PyQt5.QtCore import QObject, pyqtSignal


class SignalBus(QObject):
    session_updated = pyqtSignal()
    loan_added = pyqtSignal()

signal_bus = SignalBus()
