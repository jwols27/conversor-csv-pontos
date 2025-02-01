import os
import sys
import platform
from pathlib import Path

from conversor import ConversorCoordernadas

from PySide6.QtWidgets import QApplication
from PySide6.QtQml import QQmlApplicationEngine
from PySide6.QtCore import QObject, Signal, Slot, QUrl
from PySide6.QtGui import QIcon

class FileProcessor(QObject):
    fileProcessed = Signal(str)

    @Slot(str, float, float, float)
    def processFile(self, fileUrl, norte, este, altura):
        filePath = fileUrl.replace("file://", "")
        if platform.system() == 'Windows':
            filePath = filePath[:0] + filePath[1:]
            print(filePath)


        if not os.path.exists(filePath):
            self.fileProcessed.emit("Arquivo não encontrado")
            return

        try:
            conversor = ConversorCoordernadas()
            conversor.converter(filePath, norte, este, altura)
            self.fileProcessed.emit("")

        except Exception as e:
            self.fileProcessed.emit(f"Erro: {e}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    engine = QQmlApplicationEngine()

    icon_path = Path(__file__).resolve().parent / "icon.png"
    app.setWindowIcon(QIcon(str(icon_path)))

    fileProcessor = FileProcessor()
    engine.rootContext().setContextProperty("fileProcessor", fileProcessor)

    qml_file = Path(__file__).resolve().parent / "main.qml"
    engine.load(qml_file)

    if not engine.rootObjects():
        sys.exit(-1)

    sys.exit(app.exec())
