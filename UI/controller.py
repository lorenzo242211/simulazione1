import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

    def fillDDGenre(self):
        for g in self._model.idMapGenere:
            self._view._ddGenre.options.append(ft.dropdown.Option(key=g, text=self._model.idMapGenere[g]))
        self._view.update_page()

    def handleCreaGrafo(self, e):
        self.fillDDGenre()
        genere = self._view._ddGenre.value
        if not genere:
            self._view.create_alert("Selezionare un genere!")
            self._view.update_page()
            return
        self._model.creaGrafo(int(genere))


    def handleCammino(self,e):
        pass