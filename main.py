import sys
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import random
import pyqtgraph as pg
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *


class MoviesWindow(QtWidgets.QWidget):
    df = pd.read_csv('netflix_titles.csv')
    row_size = df.shape[0]
    column_size = df.shape[1]

    def __init__(self, row_size, column_size):
        super().__init__()
        self.setWindowTitle("Movies")
        self.row_size = row_size
        self.column_size = column_size
        self.table = QtWidgets.QTableWidget(self.row_size, self.column_size)
        self.button = QtWidgets.QPushButton("Recommend Movies")
        self.button_2 = QtWidgets.QPushButton("Show Cosine Similarities")
        self.graphWidget = pg.PlotWidget()
        self.scatter = pg.ScatterPlotItem(
            size=10, brush=pg.mkBrush(30, 255, 35, 255))
        self.graphWidget.addItem(self.scatter)
        t_box = QtWidgets.QHBoxLayout()
        t_box.addWidget(self.table)
        t_box.addWidget(self.button)
        s_box = QtWidgets.QHBoxLayout()
        s_box.addWidget(self.graphWidget)
        s_box.addWidget(self.button_2)
        v_box = QtWidgets.QVBoxLayout()
        v_box.addLayout(t_box)
        v_box.addLayout(s_box)
        v_box.addStretch()
        self.setLayout(v_box)
        for row in range(0, row_size):
            for column in range(0, column_size):
                self.table.setItem(row, column, QTableWidgetItem(str(self.df.iloc[row, column])))
        column_headers = list(self.df.columns.values)
        self.table.setHorizontalHeaderLabels(column_headers)

        self.setGeometry(1000, 1000, 1000, 1000)
        self.button.clicked.connect(self.click)
        self.button_2.clicked.connect(self.show_similarity)
        self.show()

    def cos_similarity(self):
        def merge_name(director):
            merged_name = str(director).lower()
            return merged_name.replace(' ', '')

        self.df['director'] = self.df['director'].apply(merge_name)
        self.df['title'] = self.df['title'].str.lower()
        self.df['listed_in'] = self.df['listed_in'].str.lower()
        df_new = self.df.drop(['show_id', 'type', 'cast', 'country', 'date_added', 'release_year', 'rating', 'duration',
                               'description'], axis=1)
        df_new['data'] = df_new[df_new.columns[1:]].apply(
            lambda x: ' '.join(x.dropna().astype(str)), axis=1)
        vectorize = CountVectorizer()
        vectorized = vectorize.fit_transform(df_new['data'])
        similarities = cosine_similarity(vectorized)
        return similarities

    def click(self):
        similarity = self.cos_similarity()
        print(similarity)
        self.df = pd.DataFrame(similarity, columns=self.df['title'], index=self.df['title']).reset_index()
        movie = random.choice(self.df['title'])
        recommendations = pd.DataFrame(self.df.nlargest(20, movie)['title'])
        recommendations = recommendations[recommendations['title'] != movie]
        selected_movie = "Selected Movie: " + movie
        result = selected_movie + '\n' + 'Recommended Movies: ' + "\n" + recommendations.to_string()
        messagebox = QMessageBox()
        messagebox.setText(result)
        messagebox.setWindowTitle("Result")
        messagebox.exec()

    def show_similarity(self):

        cos_similarity = self.cos_similarity()
        print(cos_similarity)
        self.graphWidget.setXRange(0, 1)
        self.graphWidget.setYRange(0, 1)
        self.scatter.setData(cos_similarity[:, 0], cos_similarity[:, 1])


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MoviesWindow(row_size=MoviesWindow.row_size, column_size=MoviesWindow.column_size)
    sys.exit(app.exec_())
