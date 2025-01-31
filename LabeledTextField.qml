import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

ColumnLayout {
    id: root
    property string label: ""
    property alias text: input.text

    SystemPalette { id: myPalette; colorGroup: SystemPalette.Active }

    spacing: 5
    Layout.fillWidth: true

    Text {
        id: inputLabel
        text: root.label
        font.pixelSize: 16
        color: myPalette.windowText
    }

    TextField {
        id: input
        placeholderText: root.label
        font.pixelSize: 16
        Layout.fillWidth: true
        validator: DoubleValidator { bottom: 0; notation: DoubleValidator.StandardNotation; locale: "en" }
    }
}
