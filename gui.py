"""PySide6 desktop front end for TrueSens. All math comes from calculator.py."""

import argparse
import sys

from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QFont
from PySide6.QtWidgets import (
    QAbstractItemView,
    QApplication,
    QComboBox,
    QDoubleSpinBox,
    QFormLayout,
    QGroupBox,
    QHeaderView,
    QLabel,
    QSpinBox,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)

from calculator import convert_sensitivity, cm360_for_sensitivity, load_games, sensitivity_for_cm360


def game_combo(games):
    """Return a QComboBox listing each game's display name."""
    combo = QComboBox()
    for game in games:
        combo.addItem(game["name"])
    return combo


class TrueSensWindow(QWidget):
    def __init__(self, games):
        super().__init__()
        self.games = games
        self.setWindowTitle("TrueSens")
        self.setFixedSize(560, 620)

        layout = QVBoxLayout(self)
        layout.setSpacing(14)
        layout.addWidget(self._build_setup())
        layout.addWidget(self._build_aim())
        layout.addWidget(self._build_table())
        layout.addWidget(self._build_backwards())

        self.game.currentIndexChanged.connect(self.refresh)
        self.dpi.valueChanged.connect(self.refresh)
        self.sens.valueChanged.connect(self.refresh)
        self.target_cm.valueChanged.connect(self.refresh)
        self.target_game.currentIndexChanged.connect(self.refresh)
        self.refresh()

    def _build_setup(self):
        box = QGroupBox("Your setup")
        form = QFormLayout(box)
        form.setVerticalSpacing(10)

        self.game = game_combo(self.games)

        self.dpi = QSpinBox()
        self.dpi.setRange(100, 32000)
        self.dpi.setSingleStep(100)
        self.dpi.setValue(1600)

        self.sens = QDoubleSpinBox()
        self.sens.setRange(0.01, 100)
        self.sens.setDecimals(3)
        self.sens.setValue(1.0)

        form.addRow("Game", self.game)
        form.addRow("DPI", self.dpi)
        form.addRow("Sensitivity", self.sens)
        return box

    def _build_aim(self):
        box = QGroupBox("Your aim")
        column = QVBoxLayout(box)
        column.setSpacing(4)

        self.cm360 = QLabel()
        big = QFont(self.font())
        big.setPointSize(22)
        big.setBold(True)
        self.cm360.setFont(big)

        self.edpi = QLabel()
        self.edpi.setStyleSheet("color: grey;")

        column.addWidget(self.cm360)
        column.addWidget(self.edpi)
        return box

    def _build_table(self):
        box = QGroupBox("Equivalent sensitivity")
        column = QVBoxLayout(box)

        self.table = QTableWidget(len(self.games), 2)
        self.table.setHorizontalHeaderLabels(["Game", "Sensitivity"])
        self.table.verticalHeader().setVisible(False)
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeToContents)
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table.setSelectionMode(QAbstractItemView.NoSelection)
        self.table.setFocusPolicy(Qt.NoFocus)
        self.table.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.table.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        for row, game in enumerate(self.games):
            self.table.setItem(row, 0, QTableWidgetItem(game["name"]))
            value = QTableWidgetItem()
            value.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            self.table.setItem(row, 1, value)
        self.table.resizeRowsToContents()
        height = self.table.horizontalHeader().height() + 2 * self.table.frameWidth()
        height += sum(self.table.rowHeight(row) for row in range(len(self.games)))
        self.table.setFixedHeight(height)

        column.addWidget(self.table)
        return box

    def _build_backwards(self):
        box = QGroupBox("Or work backwards")
        form = QFormLayout(box)
        form.setVerticalSpacing(10)

        self.target_cm = QDoubleSpinBox()
        self.target_cm.setRange(1.0, 500.0)
        self.target_cm.setDecimals(1)
        self.target_cm.setSuffix(" cm")
        self.target_cm.setValue(30.0)

        self.target_game = game_combo(self.games)

        self.target_sens = QLabel()
        bold = QFont(self.font())
        bold.setBold(True)
        self.target_sens.setFont(bold)
        self.target_sens.setTextInteractionFlags(Qt.TextSelectableByMouse)

        form.addRow("Target cm / 360", self.target_cm)
        form.addRow("Game", self.target_game)
        form.addRow("Sensitivity", self.target_sens)
        return box

    def refresh(self):
        game = self.game.currentText()
        dpi = self.dpi.value()
        sens = self.sens.value()

        cm360 = cm360_for_sensitivity(sens, game, dpi, self.games)
        self.cm360.setText(f"CM / 360: {cm360:.1f}")
        self.edpi.setText(f"eDPI: {round(dpi * sens)}")

        highlight = self.palette().highlight()
        highlight_text = self.palette().highlightedText()
        for row, other in enumerate(self.games):
            value = convert_sensitivity(sens, game, other["name"], dpi, self.games)
            self.table.item(row, 1).setText(f"{value:.2f}")
            selected = other["name"] == game
            for col in range(2):
                item = self.table.item(row, col)
                font = item.font()
                font.setBold(selected)
                item.setFont(font)
                item.setBackground(highlight if selected else Qt.NoBrush)
                item.setForeground(highlight_text if selected else self.palette().text())

        target = sensitivity_for_cm360(
            self.target_cm.value(), self.target_game.currentText(), dpi, self.games
        )
        self.target_sens.setText(f"{target:.3f}  (at {dpi} DPI)")


def parse_args(argv):
    parser = argparse.ArgumentParser(description="TrueSens desktop GUI")
    parser.add_argument("--screenshot", metavar="PATH", help="render the window to PATH and exit")
    return parser.parse_args(argv)


def main(argv=None):
    args = parse_args(sys.argv[1:] if argv is None else argv)
    app = QApplication(sys.argv[:1])
    window = TrueSensWindow(load_games())
    window.show()

    if args.screenshot:
        def capture():
            ok = window.grab().save(args.screenshot)
            app.exit(0 if ok else 1)

        QTimer.singleShot(300, capture)

    return app.exec()


if __name__ == "__main__":
    sys.exit(main())
