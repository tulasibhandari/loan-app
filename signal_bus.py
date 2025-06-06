from PyQt5.QtCore import QObject, pyqtSignal


class SignalBus(QObject):
    session_updated = pyqtSignal()

signal_bus = SignalBus()
