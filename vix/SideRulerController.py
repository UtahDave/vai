from .LineBadge import LineBadge
from vixtk import gui

class SideRulerController:
    def __init__(self, side_ruler):
        self._side_ruler = side_ruler
        self._edit_area_model = None
        self._document_model = None

    def setModel(self, document_model, edit_area_model):
        if self._edit_area_model:
            self._edit_area_model.documentPosChanged.disconnect(self.updateTopRow)

        if self._document_model:
            self._document_model.lineMetaInfoChanged.disconnect(self.updateBadges)
            self._document_model.lineDeleted.disconnect(self.updateNumRows)
            self._document_model.lineCreated.disconnect(self.updateNumRows)

        self._edit_area_model = edit_area_model
        self._edit_area_model.documentPosChanged.connect(self.updateTopRow)

        self._document_model = document_model
        self._document_model.lineMetaInfoChanged.connect(self.updateBadges)
        self._document_model.lineDeleted.connect(self.updateNumRows)
        self._document_model.lineCreated.connect(self.updateNumRows)

        self.updateTopRow()
        self.updateNumRows()
        self.updateBadges()

    def updateTopRow(self, *args):
        if self._edit_area_model:
            top_pos = self._edit_area_model.documentPosAtTop()
            self._side_ruler.setTopRow(top_pos[0])

    def updateNumRows(self, *args):
        if self._document_model:
            self._side_ruler.setNumRows(self._document_model.numLines())

    def updateBadges(self, *args):
        if self._document_model:
            for line_num in range(1,self._document_model.numLines()+1):
                meta = self._document_model.lineMeta(line_num)

                if meta.get("change") == "added":
                    self._side_ruler.addBadge(line_num, LineBadge(marker="+", description="",
                              fg_color=gui.VGlobalColor.white, bg_color=gui.VGlobalColor.green))
                elif meta.get("change") == "modified":
                    self._side_ruler.addBadge(line_num, LineBadge(marker=".", description="",
                             fg_color=gui.VGlobalColor.white, bg_color=gui.VGlobalColor.magenta))
                elif meta.get("change") == None:
                    self._side_ruler.removeBadge(line_num)


