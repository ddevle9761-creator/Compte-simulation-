from PySide6.QtCore import QObject, Signal, Slot


class Emain_thread(QObject):
    finished = Signal(object)
    error = Signal(str)

    def __init__(self, target=None, *args, **kwargs):
        super().__init__()
        self._target = target
        self._args = ()
        self._kwargs = {}

        

    @Slot()
    def run(self):
        try:
            if self._target is None:
                self.finished.emit(None)
                return
            result = self._target(*self._args, **self._kwargs)
            self.finished.emit(result)
        except Exception as e:
            self.error.emit(str(e))

