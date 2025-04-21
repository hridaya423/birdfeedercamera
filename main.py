import tensorflow as tf
import tensorflow_hub as hub
from detection.species_classifier import SpeciesClassifier

species_classifier = SpeciesClassifier()
species_classifier._load_model()

from PyQt5 import QtWidgets
from ui.main_window import MainWindow
import sys

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow(classifier=species_classifier)
    window.show()
    sys.exit(app.exec_())
