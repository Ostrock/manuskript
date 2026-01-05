#!/usr/bin/env python
# --!-- coding: utf8 --!--
from PyQt5.QtWidgets import QWidget, QAbstractItemView

from manuskript.enums import Outline
from manuskript.ui.views.basicItemView_ui import Ui_basicItemView


class basicItemView(QWidget, Ui_basicItemView):
    def __init__(self, parent=None):
        QWidget.__init__(self)
        self.setupUi(self)
        self.txtSummarySituation.setColumn(Outline.summarySituation)
        self.txtSummarySentence.setColumn(Outline.summarySentence)
        self.txtSummarySentence_2.setColumn(Outline.summarySentence)
        self.txtSummaryPara.setColumn(Outline.summaryPara)
        self.txtSummaryPara_2.setColumn(Outline.summaryPara)
        self.txtSummaryPage.setColumn(Outline.summaryPage)
        self.txtSummaryPage_2.setColumn(Outline.summaryPage)
        self.txtSummaryFull.setColumn(Outline.summaryFull)
        self.txtGoal.setColumn(Outline.setGoal)
        
        # Ensure editable widgets are not read-only
        self.txtSummaryPara.setReadOnly(False)
        self.txtSummaryPage.setReadOnly(False)
        self.txtSummaryFull.setReadOnly(False)
        
        # Initialize the snowflake summary dropdown
        self.cmbOutlineSummary.setCurrentIndex(0)
        self.cmbOutlineSummary.currentIndexChanged.emit(0)

    def setModels(self, mdlOutline, mdlCharacter, mdlLabels, mdlStatus):
        self.cmbPOV.setModels(mdlCharacter, mdlOutline)
        self.txtSummarySituation.setModel(mdlOutline)
        self.txtSummarySentence.setModel(mdlOutline)
        self.txtSummarySentence_2.setModel(mdlOutline)
        self.txtSummaryPara.setModel(mdlOutline)
        self.txtSummaryPara_2.setModel(mdlOutline)
        self.txtSummaryPage.setModel(mdlOutline)
        self.txtSummaryPage_2.setModel(mdlOutline)
        self.txtSummaryFull.setModel(mdlOutline)
        self.txtGoal.setModel(mdlOutline)

    def getIndexes(self, sourceView):
        """Returns a list of indexes from list of QItemSelectionRange"""
        indexes = []

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

        if len(indexes) == 0:
            self.setEnabled(False)

        elif len(indexes) == 1:
            self.setEnabled(True)
            idx = indexes[0]
            self.txtSummarySituation.setCurrentModelIndex(idx)
            self.txtSummarySentence.setCurrentModelIndex(idx)
            self.txtSummarySentence_2.setCurrentModelIndex(idx)
            self.txtSummaryPara.setCurrentModelIndex(idx)
            self.txtSummaryPara_2.setCurrentModelIndex(idx)
            self.txtSummaryPage.setCurrentModelIndex(idx)
            self.txtSummaryPage_2.setCurrentModelIndex(idx)
            self.txtSummaryFull.setCurrentModelIndex(idx)
            self.cmbPOV.setCurrentModelIndex(idx)
            self.txtGoal.setCurrentModelIndex(idx)

        else:
            self.setEnabled(True)
            self.txtSummarySituation.setCurrentModelIndexes(indexes)
            self.txtSummarySentence.setCurrentModelIndexes(indexes)
            self.txtSummarySentence_2.setCurrentModelIndexes(indexes)
            self.txtSummaryPara.setCurrentModelIndexes(indexes)
            self.txtSummaryPara_2.setCurrentModelIndexes(indexes)
            self.txtSummaryPage.setCurrentModelIndexes(indexes)
            self.txtSummaryPage_2.setCurrentModelIndexes(indexes)
            self.txtSummaryFull.setCurrentModelIndexes(indexes)
            self.cmbPOV.setCurrentModelIndexes(indexes)
            self.txtGoal.setCurrentModelIndexes(indexes)

    def setDict(self, d):
        self.txtSummaryFull.setDict(d)

    def toggleSpellcheck(self, v):
        self.txtSummaryFull.toggleSpellcheck(v)
