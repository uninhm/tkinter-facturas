import tkinter as tk
import tkinter.ttk as ttk
import tkinter.messagebox as msgbox
import sqlite3

class Program:
    db_name = 'facturas.db'

    def __init__(self):
        self.root = tk.Tk()
        self.root.title('Facturas')
        self.root.resizable(False, False)

        # Label client's DNI
        tk.Label((self.root), text='DNI Cliente:').grid(row=0, column=0)

        # Entry client's DNI
        self.cliente = tk.StringVar()
        tk.Entry((self.root), textvariable=(self.cliente)).grid(row=0, column=1, pady=10)

        # Products list
        self.tree = ttk.Treeview((self.root), height=10, columns=('id', 'precio', 'cantidad'))
        self.tree.grid(row=1, column=0, rowspan=4, columnspan=5, padx=10)
        self.tree.heading('#0', text='ID', anchor='center')
        self.tree.heading('#1', text='Producto', anchor='center')
        self.tree.heading('#2', text='Precio', anchor='center')
        self.tree.heading('#3', text='Cantidad', anchor='center')
        self.tree.column('#0', width=70, minwidth=0)
        self.tree.column('#1', width=300)
        self.tree.column('#2', width=100)
        self.tree.column('#3', width=60)

        # "Add product" frame
        self.frame = ttk.Labelframe((self.root), text='Agregar Producto')
        self.frame.grid(row=5, column=0, columnspan=5, padx=10, pady=10)

        # Label product's ID
        tk.Label((self.frame), text='ID:').grid(row=0, column=0, padx=5, pady=3)

        # Entry product's ID
        self.id_producto = tk.StringVar()
        self.ety_id = tk.Entry((self.frame), textvariable=(self.id_producto))
        self.ety_id.grid(row=0, column=1, padx=3, pady=3)
        self.ety_id.focus()
        self.ety_id.bind('<Return>', lambda event: self.ety_cant.focus())

        # Label number of product
        tk.Label((self.frame), text='Cantidad:').grid(row=0, column=2, padx=5, pady=3)

        # Entry number of product
        self.cantidad = tk.StringVar()
        self.ety_cant = tk.Entry((self.frame), textvariable=(self.cantidad))
        self.ety_cant.grid(row=0, column=3, padx=3, pady=3)
        self.ety_cant.bind('<Return>', lambda event: self.agregar())

        # Buttons
        tk.Button((self.frame), text='Agregar', command=(self.agregar)).grid(row=0, column=4, padx=3, pady=3)
        tk.Button((self.root), text='Eliminar', command=(self.eliminar)).grid(row=1, column=5, padx=5, sticky='WE')
        tk.Button((self.root), text='Vender', command=(self.vender)).grid(row=2, column=5, padx=5, sticky='WE')

        self.root.mainloop()

    def run_query(self, query, parameters=()):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            result = cursor.execute(query, parameters)
            conn.commit()
        return result

    def get_product(self, id):
        return self.run_query('SELECT * FROM productos WHERE id = ?', (id,))

    def agregar(self):
        if self.id_producto.get() != '' and self.cantidad.get() != '' and int(self.cantidad.get()) > 0:
            for i in self.get_product(int(self.id_producto.get())):
                self.tree.insert('', 0, text=(i[0]), values=(i[1], i[2], self.cantidad.get()))
            else:
                self.id_producto.set('')
                self.cantidad.set('')
                self.ety_id.focus()

        else:
            msgbox.showerror('Error', 'No puede haber campos vacios ni con el valor 0')
            if self.cantidad.get() == '' or int(self.cantidad.get()) <= 0 and self.id_producto.get() != '':
                self.cantidad.set('')
                self.ety_cant.focus()
            else:
                self.ety_id.focus()

    def eliminar(self):
        if self.tree.item(self.tree.selection())['text'] != '':
            self.tree.delete(self.tree.selection())
            self.ety_id.focus()
        else:
            msgbox.showerror('Error', 'Debe seleccionar un producto')

    def vender(self):
        total = 0
        records = self.tree.get_children()
        actual_stock = 0
        if len(records) != 0:
            for i in records:
                cantidad = int(self.tree.item(i)['values'][2])
                id = self.tree.item(i)['text']
                for row in self.get_product(id):
                    actual_stock = int(row[3])
                else:
                    total += float(self.tree.item(i)['values'][1]) * int(self.tree.item(i)['values'][2])
                    self.run_query('UPDATE productos SET stock = ? WHERE id = ?', (actual_stock - cantidad, id))
                    self.tree.delete(i)

            else:
                msgbox.showinfo('Total', f"Total: {total}")

        else:
            msgbox.showerror('Error', 'Debe agregar al menos un producto')


if __name__ == '__main__':
    programa = Program()
