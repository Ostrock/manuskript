#!/usr/bin/env python
# --!-- coding: utf8 --!--
from PyQt5.QtWidgets import QWidget, QAbstractItemView
from PyQt5.QtCore import QModelIndex

from manuskript.enums import Outline
from manuskript.ui.views.metadataView_ui import Ui_metadataView
from manuskript.ui import style

class metadataView(QWidget, Ui_metadataView):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.setupUi(self)
        self._lastIndexes = None
        self.txtSummarySituation.setColumn(Outline.summarySituation)
        self.txtSummarySentence.setColumn(Outline.summarySentence)
        self.txtSummarySentence_2.setColumn(Outline.summarySentence)
        self.txtSummaryPara.setColumn(Outline.summaryPara)
        self.txtSummaryPara_2.setColumn(Outline.summaryPara)
        self.txtSummaryPage.setColumn(Outline.summaryPage)
        self.txtSummaryPage_2.setColumn(Outline.summaryPage)
        self.txtSummaryFull.setColumn(Outline.summaryFull)
        self.txtNotes.setColumn(Outline.notes)
        self.revisions.setEnabled(False)
        
        # Ensure editable widgets are not read-only
        self.txtSummaryPara.setReadOnly(False)
        self.txtSummaryPage.setReadOnly(False)
        self.txtSummaryFull.setReadOnly(False)
        
        # Initialize the snowflake summary dropdown
        self.cmbMetadataSummary.setCurrentIndex(0)
        self.cmbMetadataSummary.currentIndexChanged.emit(0)

        self.txtSummarySituation.setStyleSheet(style.lineEditSS())
        self.txtSummarySentence.setStyleSheet(style.lineEditSS())
        self.txtSummarySentence_2.setStyleSheet(style.lineEditSS())
        self.txtSummaryPara.setStyleSheet(style.transparentSS() +
                                          style.simpleScrollBarV())
        self.txtSummaryPara_2.setStyleSheet(style.transparentSS() +
                                            style.simpleScrollBarV())
        self.txtSummaryPage.setStyleSheet(style.transparentSS() +
                                          style.simpleScrollBarV())
        self.txtSummaryPage_2.setStyleSheet(style.transparentSS() +
                                            style.simpleScrollBarV())
        self.txtSummaryFull.setStyleSheet(style.transparentSS() +
                                          style.simpleScrollBarV())
        self.txtNotes.setStyleSheet(style.transparentSS() +
                                    style.simpleScrollBarV())
        self.revisions.setStyleSheet(style.simpleScrollBarV())

    def setModels(self, mdlOutline, mdlCharacter, mdlLabels, mdlStatus):
        self.properties.setModels(mdlOutline, mdlCharacter, mdlLabels, mdlStatus)
        self.txtSummarySituation.setModel(mdlOutline)
        self.txtSummarySentence.setModel(mdlOutline)
        self.txtSummarySentence_2.setModel(mdlOutline)
        self.txtSummaryPara.setModel(mdlOutline)
        self.txtSummaryPara_2.setModel(mdlOutline)
        self.txtSummaryPage.setModel(mdlOutline)
        self.txtSummaryPage_2.setModel(mdlOutline)
        self.txtSummaryFull.setModel(mdlOutline)
        self.txtNotes.setModel(mdlOutline)
        self.revisions.setModel(mdlOutline)

    def getIndexes(self, sourceView):
        """Returns a list of indexes from list of QItemSelectionRange"""
        indexes = []

        if ((sourceView is None) or (not hasattr(sourceView, 'selection'))):
            return indexes

        for i in sourceView.selection().indexes():
            if i.column() != 0:
                continue

            if i not in indexes:
                indexes.append(i)

        return indexes

    def selectionChanged(self):

        if isinstance(self.sender(), QAbstractItemView):
            selectionModel = self.sender().selectionModel()
        else:
            selectionModel = self.sender()

        indexes = self.getIndexes(selectionModel)

        if self._lastIndexes == indexes:
            return

        # No item selected
        if len(indexes) == 0:
            self.setEnabled(False)
            self.revisions.situation.setCurrentModelIndex(QModelIndex())
            self.txtSummarySentence.setCurrentModelIndex(QModelIndex())
            self.txtSummarySentence_2.setCurrentModelIndex(QModelIndex())
            self.txtSummaryPara.setCurrentModelIndex(QModelIndex())
            self.txtSummaryPara_2.setCurrentModelIndex(QModelIndex())
            self.txtSummaryPage.setCurrentModelIndex(QModelIndex())
            self.txtSummaryPage_2.setCurrentModelIndex(QModelIndex())
            self.txtSummaryFull.setCurrentModelIndex(QModelIndex())
            self.txtNotes.setCurrentModelIndex(QModelIndex())

        # One item selected
        elif len(indexes) == 1:
            self.setEnabled(True)
            idx = indexes[0]
            self.txtSummarySituation.setEnabled(True)
            self.txtSummarySentence.setEnabled(True)
            self.txtSummarySentence_2.setEnabled(True)
            self.txtSummaryPara.setEnabled(True)
            self.txtSummaryPara_2.setEnabled(True)
            self.txtSummaryPage.setEnabled(True)
            self.txtSummaryPage_2.setEnabled(True)
            self.txtSummaryFull.setEnabled(True)
            self.txtNotes.setEnabled(True)
            self.txtSummarySituation.setCurrentModelIndex(idx)
            self.txtSummarySentence.setCurrentModelIndex(idx)
            self.txtSummarySentence_2.setCurrentModelIndex(idx)
            self.txtSummaryPara.setCurrentModelIndex(idx)
            self.txtSummaryPara_2.setCurrentModelIndex(idx)
            self.txtSummaryPage.setCurrentModelIndex(idx)
            self.txtSummaryPage_2.setCurrentModelIndex(idx)
            self.txtSummaryFull.setCurrentModelIndex(idx)
            self.txtNotes.setCurrentModelIndex(idx)
            self.revisions.setEnabled(True)
            self.revisions.setCurrentModelIndex(idx)

        # Multiple items selected
        else:
            self.setEnabled(True)

            # Behavior 1:
            # We disable the text areas when multiple indexes are selected
            self.txtSummarySituation.setEnabled(False)
            self.txtSummarySentence.setEnabled(False)
            self.txtSummarySentence_2.setEnabled(False)
            self.txtSummaryPara.setEnabled(False)
            self.txtSummaryPara_2.setEnabled(False)
            self.txtSummaryPage.setEnabled(False)
            self.txtSummaryPage_2.setEnabled(False)
            self.txtSummaryFull.setEnabled(False)
            self.txtNotes.setEnabled(False)
            self.txtSummarySituation.setCurrentModelIndex(QModelIndex())
            self.txtSummarySentence.setCurrentModelIndex(QModelIndex())
            self.txtSummarySentence_2.setCurrentModelIndex(QModelIndex())
            self.txtSummaryPara.setCurrentModelIndex(QModelIndex())
            self.txtSummaryPara_2.setCurrentModelIndex(QModelIndex())
            self.txtSummaryPage.setCurrentModelIndex(QModelIndex())
            self.txtSummaryPage_2.setCurrentModelIndex(QModelIndex())
            self.txtSummaryFull.setCurrentModelIndex(QModelIndex())
            self.txtNotes.setCurrentModelIndex(QModelIndex())

            # Behavior 2:
            # Allow edition of multiple indexes.
            # Bug: Multiple selections of items sometimes gets Notes/references
            #      field to be erased. See #10 on github.
            #self.txtSummarySentence.setCurrentModelIndexes(indexes)
            #self.txtSummaryPara.setCurrentModelIndexes(indexes)
            #self.txtSummaryPage.setCurrentModelIndexes(indexes)
            #self.txtSummaryFull.setCurrentModelIndexes(indexes)
            #self.txtNotes.setCurrentModelIndexes(indexes)

            self.revisions.setEnabled(False)

        self.properties.selectionChanged(selectionModel)
        self._lastIndexes = indexes

    def setDict(self, d):
        self.txtNotes.setDict(d)
        self.txtSummaryFull.setDict(d)

    def toggleSpellcheck(self, v):
        self.txtNotes.toggleSpellcheck(v)
        self.txtSummaryFull.toggleSpellcheck(v)

    def saveState(self):
        return [
            self.grpProperties.saveState(),
            self.grpSummary.saveState(),
            self.grpNotes.saveState(),
            self.grpRevisions.saveState(),
            self.revisions.saveState()
        ]

    def restoreState(self, state):
        self.grpProperties.restoreState(state[0])
        self.grpSummary.restoreState(state[1])
        self.grpNotes.restoreState(state[2])
        self.grpRevisions.restoreState(state[3])
