from PyQt5.QtWidgets import QMessageBox


class MessageBox:

    def __init__(self, mensagem: str, windowTitle: str = "Message", informativeText: str = "",  icon = QMessageBox.Information):
        self.msg = QMessageBox()
        self.msg.setIcon(icon)
        self.msg.setText(mensagem)
        self.msg.setInformativeText(informativeText)
        self.msg.setWindowTitle(windowTitle)
        self.msg.exec_()

class MessageBoxInfo(MessageBox):
    def __init__(self, mensagem: str, windowTitle: str = "Informação", informativeText: str = ""):
        super().__init__(mensagem, windowTitle, informativeText, QMessageBox.Information)

class MessageBoxError(MessageBox):
    def __init__(self, mensagem: str, windowTitle: str = "Erro", informativeText: str = ""):
        super().__init__(mensagem, windowTitle, informativeText, QMessageBox.Critical)

class MessageBoxWarning(MessageBox):
    def __init__(self, mensagem: str, windowTitle: str = "Aviso", informativeText: str = ""):
        super().__init__(mensagem, windowTitle, informativeText, QMessageBox.Warning)

