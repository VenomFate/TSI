from tkinter import ttk
from tkinter import *

import sqlite3

class Producto:

    db_name = "SI.db"

    def __init__(self, window):
        self.win = window
        self.win.title = "Inventario Enre Lagos "

        # Apartado para agregar materia prima
        frame = LabelFrame(self.win, text = "Materia Prima")
        frame.grid(row = 0, column = 0, columnspan = 2, pady = 20)

        Label(frame, text = "Nombre: ").grid(row = 1, column = 0)
        self.nombre = Entry(frame)
        self.nombre.grid(row = 1, column = 1)

        Label(frame, text = "Stock: ").grid(row = 2, column = 0)
        self.stock = Entry(frame)
        self.stock.grid(row = 2, column = 1) 

        Label(frame, text = "Stock critico: ").grid(row = 3, column = 0)
        self.stockcrit = Entry(frame)
        self.stockcrit.grid(row = 3, column = 1)

        # Boton "Agregar"
        ttk.Button(frame, text = "Agregar", command = self.add_materia).grid(row = 4, columnspan = 2, sticky = W + E)

        # Output Messages 
        self.mensaje = Label(text = '', fg = 'red')
        self.mensaje.grid(row = 4, column = 0, columnspan = 2, sticky = W + E)
        
        # Tabla
        self.tabla = ttk.Treeview(height = 10, columns = ('#1', '#2'))
        self.tabla.grid(row = 5, column = 0, columnspan = 2)
        self.tabla.heading('#0', text = 'Nombre', anchor = CENTER)
        self.tabla.heading('#1', text = 'Stock', anchor = CENTER)
        self.tabla.heading('#2', text = 'Stock Critico', anchor = CENTER)

        # Boton "Eliminar"
        ttk.Button(text = 'Eliminar', command = self.eliminar_materia).grid(row = 6, column = 0, sticky = W + E)
        # Boton "Editar"
        ttk.Button(text = 'Editar', command = self.edit_materia).grid(row = 6, column = 1, sticky = W + E)

        self.get_materia()

    # Funcion para hacer consultas a la base de datos
    def consulta(self, query, parametros = ()):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            result = cursor.execute(query, parametros)
            conn.commit()
        return result
    
    # Funcion para obtener materia prima de la base de datos
    def get_materia(self):
        # F5 tabla
        records = self.tabla.get_children()
        for element in records:
            self.tabla.delete(element)
        # Se consulta la informacion en la base de datos
        query = 'SELECT * FROM Materia_Prima ORDER BY Nombre DESC'
        db_rows = self.consulta(query)
        # Se rellena la tabla con la informacion de la base de datos
        for row in db_rows:
            self.tabla.insert('', 0, text = row[2], values = row[3:5])

    # Se valida los campos de entrada
    def validacion(self):
        return len(self.nombre.get()) != 0 and len(self.stock.get()) != 0 and len(self.stockcrit.get()) != 0

    # Agregar materia prima a la base de datos
    def add_materia(self):
        if self.validacion():
            query = 'INSERT INTO Materia_Prima VALUES(NULL, NULL, ?, ?, ?)'
            parametros =  (self.nombre.get(), self.stock.get(), self.stockcrit.get())
            self.consulta(query, parametros)
            self.mensaje['text'] = '{} se añadio Correctamente!'.format(self.nombre.get())
            self.nombre.delete(0, END)
            self.stock.delete(0, END)
            self.stockcrit.delete(0, END)
        else:
            self.mensaje['text'] = 'Se requiere: Nombre, Stock y Stock critico'
        self.get_materia()

    # Eliminar materia prima de la base de datos
    def eliminar_materia(self):
        self.mensaje['text'] = ''
        try:
           self.tabla.item(self.tabla.selection())['text'][0]
        except IndexError as e:
            self.mensaje['text'] = 'Seleccione un producto'
            return
        self.mensaje['text'] = ''
        nombre = self.tabla.item(self.tabla.selection())['text']
        query = 'DELETE FROM Materia_Prima WHERE Nombre = ?'
        self.consulta(query, (nombre, ))
        self.mensaje['text'] = '{} se ha eliminado Correctamente!'.format(nombre)
        self.get_materia()

    # Editar materia prima de la base de datos
    def edit_materia(self):
        
        self.mensaje['text'] = ''
        try:
            self.tabla.item(self.tabla.selection())['values'][0]
        except IndexError as e:
            self.mensaje['text'] = 'Seleccione un producto'
            return
        old_nombre = self.tabla.item(self.tabla.selection())['text']
        old_stock = self.tabla.item(self.tabla.selection())['values'][0]
        old_stockcrit = self.tabla.item(self.tabla.selection())['values'][1]
        
        self.edit_win = Toplevel()
        self.edit_win.title = "Editar Materia Prima"
        
        # viejo nombre
        Label(self.edit_win, text = 'Anterior Nombre:').grid(row = 0, column = 1)
        Entry(self.edit_win, textvariable = StringVar(self.edit_win, value = old_nombre), state = 'readonly').grid(row = 0, column = 2)
        # Nuevo nombre
        Label(self.edit_win, text = 'Nuevo Nombre:').grid(row = 1, column = 1)
        nuevo_nombre = Entry(self.edit_win)
        nuevo_nombre.grid(row = 1, column = 2)

        # Viejo stock 
        Label(self.edit_win, text = 'Anterior Stock:').grid(row = 2, column = 1)
        Entry(self.edit_win, textvariable = StringVar(self.edit_win, value = old_stock), state = 'readonly').grid(row = 2, column = 2)
        # Nuevo stock
        Label(self.edit_win, text = 'Nuevo Stock:').grid(row = 3, column = 1)
        nuevo_stock = Entry(self.edit_win)
        nuevo_stock.grid(row = 3, column = 2)

        # Viejo stock critico 
        Label(self.edit_win, text = 'Anterior Stock Critico:').grid(row = 4, column = 1)
        Entry(self.edit_win, textvariable = StringVar(self.edit_win, value = old_stockcrit), state = 'readonly').grid(row = 4, column = 2)
        # Nuevo stock critico
        Label(self.edit_win, text = 'Nuevo Stock Critico:').grid(row = 5, column = 1)
        nuevo_stockcrit = Entry(self.edit_win)
        nuevo_stockcrit.grid(row = 5, column = 2)

        Button(self.edit_win, text = 'Actualizar', command = lambda: self.edit_records(nuevo_nombre.get(), old_nombre, nuevo_stock.get(), old_stock, nuevo_stockcrit.get(), old_stockcrit)).grid(row = 6, column = 2, sticky = W)
        self.edit_win.mainloop()
        
        
    def edit_records(self, nuevo_nombre, old_nombre, nuevo_stock, old_stock, nuevo_stockcrit, old_stockcrit):
        query = 'UPDATE product SET Nombre = ?, Stock = ?, Stock_Critico = ? WHERE Nombre = ? AND Stock = ? AND Stock_Critico = ?'
        parametros = (nuevo_nombre, nuevo_stock, nuevo_stockcrit, old_nombre, old_stock, old_stockcrit)
        self.consulta(query, parametros)
        self.edit_win.destroy()
        self.mensaje['text'] = '{} ha sido actualiado Correctamente!'.format(old_nombre)
        self.get_materia()

if __name__ == '__main__':
        window = Tk()
        aplicacion = Producto(window)
        window.mainloop()