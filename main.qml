import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 2.15
import Qt.labs.platform

ApplicationWindow {
    visible: true
    width: 600
    height: 500
    title: "Conversor CSV -> Pontos"
    SystemPalette { id: myPalette; colorGroup: SystemPalette.Active }

    FileDialog {
        id: fileDialog
        title: "Selecione um arquivo CSV"
        folder: StandardPaths.standardLocations(StandardPaths.HomeLocation)[0]
        nameFilters: ["CSV files (*.csv)", "All files (*)"]
        onAccepted: {
            fileProcessor.processFile(currentFile, diffNorte.text, diffEste.text, diffAltura.text)
        }
        onRejected: {
            console.log("Seleção de arquivo cancelada.")
        }
    }

    Button {
        text: "Selecione um arquivo CSV"
        anchors.horizontalCenter: parent.horizontalCenter
        anchors.bottom: parent.bottom
        anchors.bottomMargin: 20
        onClicked: fileDialog.open()
    }


    GridLayout {
        id: valores
        anchors.horizontalCenter: parent.horizontalCenter
        anchors.verticalCenter: parent.verticalCenter
        anchors.verticalCenterOffset: -10
        width: parent.width * 0.8
        columns: 3
        columnSpacing: 10
        rowSpacing: 10

        Text {
            Layout.columnSpan: 3
            text: "Base levantada"
            font.pixelSize: 16
            color: myPalette.windowText
            font.bold: true
        }
        LabeledTextField {
            id: levNorte
            label: "Norte"
        }
        LabeledTextField {
            id: levEste
            label: "Este"
        }
        LabeledTextField {
            id: levAltura
            label: "Altura"
        }
        Text {
            Layout.topMargin: 10
            Layout.columnSpan: 3
            text: "Base corrigida"
            font.pixelSize: 16
            color: myPalette.windowText
            font.bold: true
        }
        LabeledTextField {
            id: corNorte
            label: "Norte"
        }
        LabeledTextField {
            id: corEste
            label: "Este"
        }
        LabeledTextField {
            id: corAltura
            label: "Altura"
        }
        Text {
            id: diffNorte
            font.pixelSize: 16
            color: myPalette.windowText
            Component.onCompleted: {
                diffNorte.text = Qt.binding(() => Number(corNorte.text - levNorte.text).toFixed(3))
            }
        }
        Text {
            id: diffEste
            font.pixelSize: 16
            color: myPalette.windowText
            Component.onCompleted: {
                diffEste.text = Qt.binding(() => Number(corEste.text - levEste.text).toFixed(3))
            }
        }
        Text {
            id: diffAltura
            font.pixelSize: 16
            color: myPalette.windowText
            Component.onCompleted: {
                diffAltura.text = Qt.binding(() => Number(corAltura.text - levAltura.text).toFixed(3))
            }
        }
    }

    Text {
        visible: false
        id: resultText
        anchors.horizontalCenter: parent.horizontalCenter
        anchors.top: parent.top
        anchors.topMargin: 20
        font.pixelSize: 16
        color: myPalette.windowText
    }

    Connections {
        target: fileProcessor
        function onFileProcessed(result) {
            if (result != "") {
                resultText.visible = true;
                resultText.text = result
            } else {
                resultText.visible = false;
            }
        }
    }
}

