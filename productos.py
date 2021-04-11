# decompyle3 version 3.3.2
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.6 (default, Dec 13 2020, 20:23:23) 
# [GCC 9.3.0]
# Embedded file name: /home/unai/Documentos/Codigos/Python/Tkinter/Programas Stock/productos.py
# Compiled at: 2019-11-24 22:56:28
# Size of source mod 2**32: 7619 bytes
import tkinter as tk
import tkinter.ttk as ttk
import tkinter.messagebox as msgbox
import sqlite3

class Product:
    db_name = 'facturas.db'

    def __init__(self, window):
        self.wind = window
        self.wind.title('Products Application')
        self.wind.resizable(False, False)
        frame = tk.LabelFrame((self.wind), text='Registrar un producto')
        frame.grid(row=0, column=0, columnspan=3, pady=20)
        tk.Label(frame, text='ID:').grid(row=0, column=0)
        self.idstr = tk.StringVar()
        self.id = tk.Entry(frame, textvariable=(self.idstr))
        self.id.grid(row=0, column=1)
        self.id.focus()
        self.id.bind('<Return>', lambda event: self.name.focus())
        tk.Label(frame, text='Nombre:').grid(row=1, column=0)
        self.namestr = tk.StringVar()
        self.name = tk.Entry(frame, textvariable=(self.namestr))
        self.name.grid(row=1, column=1)
        self.name.bind('<Return>', lambda event: self.price.focus())
        tk.Label(frame, text='Precio:').grid(row=2, column=0)
        self.price_str = tk.StringVar()
        self.price = tk.Entry(frame, textvariable=(self.price_str))
        self.price.grid(row=2, column=1)
        self.price.bind('<Return>', lambda event: self.stock.focus())
        tk.Label(frame, text='Stock:').grid(row=3, column=0)
        self.stock_str = tk.StringVar()
        self.stock = tk.Entry(frame, textvariable=(self.stock_str))
        self.stock.grid(row=3, column=1)
        self.stock.bind('<Return>', lambda event: self.add_product())
        tk.Button(frame, text='Enter', command=(self.add_product)).grid(row=4, column=0, columnspan=2, sticky='WE')
        self.etiq = tk.Label((self.wind), text='', font=('Arial', 8, 'italic'), fg='red')
        self.etiq.grid(row=1, column=0, columnspan=3, sticky='WE')
        self.tree = ttk.Treeview((self.wind), height=10, columns=('id', 'precio', 'stock'))
        self.tree.grid(row=2, column=0, columnspan=3)
        self.tree.heading('#0', text='ID', anchor='center')
        self.tree.heading('#1', text='Nombre', anchor='center')
        self.tree.heading('#2', text='Precio', anchor='center')
        self.tree.heading('#3', text='Stock', anchor='center')
        self.tree.column('#0', width=70)
        self.tree.column('#1', width=300)
        self.tree.column('#2', width=100)
        self.tree.column('#3', width=50)
        self.btn_eliminar = tk.Button((self.wind), text='ELIMINAR', command=(self.delete_product))
        self.btn_editar = tk.Button((self.wind), text='EDITAR', command=(self.edit_product))
        self.btn_actualizar = tk.Button((self.wind), text='ACTUALIZAR', command=(self.actualizar))
        self.btn_eliminar.grid(row=3, column=0, sticky='WE')
        self.btn_editar.grid(row=3, column=1, sticky='WE')
        self.btn_actualizar.grid(row=3, column=2, sticky='WE')
        self.get_products()

    def actualizar(self):
        self.get_products()
        self.etiq.configure(text='Se ha actualizado la tabla correctamente')

    def run_query(self, query, parameters=()):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            result = cursor.execute(query, parameters)
            conn.commit()
        return result

    def get_products(self):
        records = self.tree.get_children()
        for i in records:
            self.tree.delete(i)
        else:
            db_rows = self.run_query('SELECT * FROM productos ORDER BY nombre DESC')
            for row in db_rows:
                self.tree.insert('', 0, text=(row[0]), values=(row[1], row[2], row[3]))

    def add_product(self):
        if self.namestr.get() != ''and self.price_str.get() != '' and self.price_str.get() != '' and self.idstr.get() != '':
            self.run_query('INSERT INTO productos VALUES(?, ?, ?, ?)', (
             self.idstr.get(), self.namestr.get(), self.price_str.get(), self.stock_str.get()))
            self.namestr.set('')
            self.price_str.set('')
            self.stock_str.set('')
            self.idstr.set('')
            self.get_products()
            self.etiq.configure(text='El producto ha sido agregado correctamente')
            self.id.focus()
        else:
            self.etiq.configure(text='El id, el nombre, el precio y el stock no pueden estar vacios')

    def delete_product(self):
        id = self.tree.item(self.tree.selection())['text']
        if id != '':
            self.run_query('DELETE FROM productos WHERE id = ?', (id,))
            self.etiq.configure(text='Se ha eliminado el producto correctamente')
            self.get_products()
        else:
            self.etiq.configure(text='Debe seleccionar un producto')

    def edit_product(self):
        try:
            self.edit_id = self.tree.item(self.tree.selection())['text']
            self.edit_name = self.tree.item(self.tree.selection())['values'][0]
            self.edit_price = self.tree.item(self.tree.selection())['values'][1]
            self.edit_stock = self.tree.item(self.tree.selection())['values'][2]
        except IndexError:
            self.etiq.configure(text='Debe seleccionar un producto')
        else:
            if self.edit_id != '':
                self.toplevel = tk.Toplevel()
                self.toplevel.resizable(False, False)
                lbl = tk.Label((self.toplevel), text='Nombre:')
                self.etystr = tk.StringVar()
                self.etystr.set(self.edit_name)
                ety = tk.Entry((self.toplevel), textvariable=(self.etystr))
                ety.focus()
                ety.bind('<Return>', lambda event: ety2.focus())
                lbl2 = tk.Label((self.toplevel), text='Precio:')
                self.ety2str = tk.StringVar()
                self.ety2str.set(self.edit_price)
                ety2 = tk.Entry((self.toplevel), textvariable=(self.ety2str))
                ety2.bind('<Return>', lambda event: ety3.focus())
                lbl3 = tk.Label((self.toplevel), text='Stock:')
                self.ety3str = tk.StringVar()
                self.ety3str.set(self.edit_stock)
                ety3 = tk.Entry((self.toplevel), textvariable=(self.ety3str))
                ety3.bind('<Return>', lambda event: self.enter_editar())
                btn = tk.Button((self.toplevel), text='Enter', command=(self.enter_editar))
                lbl.grid(row=0, column=0, sticky='WE')
                ety.grid(row=1, column=0, sticky='WE')
                lbl2.grid(row=2, column=0, sticky='WE')
                ety2.grid(row=3, column=0, sticky='WE')
                lbl3.grid(row=4, column=0, sticky='WE')
                ety3.grid(row=5, column=0, sticky='WE')
                btn.grid(row=6, column=0, sticky='WE')

    def enter_editar(self):
        if self.etystr.get() != '' and self.ety2str.get() != '':
            self.run_query('UPDATE productos SET nombre = ?, precio = ?, stock = ? WHERE id = ?', (
             self.etystr.get(), self.ety2str.get(), self.ety3str.get(), self.edit_id))
            self.toplevel.destroy()
            self.etiq.configure(text='El producto ha sido actualizado correctamente')
            self.get_products()
        else:
            msgbox.showerror('Error', 'No puede haber campos vacios')


if __name__ == '__main__':
    window = tk.Tk()
    app = Product(window)
    window.mainloop()
