import pymysql
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import tkinter as tk

root = Tk()
root.title("E-duca system")
root.geometry("1080x720")
my_tree = ttk.Treeview(root)


def JanelaAluno():
    def connection():
        conn = pymysql.connect(
            host='localhost',
            user='root', 
            password='030506',
            db='bancoeduca',
        )
        return conn

    def refreshTable():
        for data in my_tree.get_children():
            my_tree.delete(data)

        for array in read():
            my_tree.insert(parent='', index='end', iid=array, text="", values=(array), tag="orow")

        my_tree.tag_configure('orow', background='#EEEEEE', font=('Arial', 12))
        my_tree.grid(row=8, column=0, columnspan=5, rowspan=11, padx=10, pady=20)

    root = Tk()
    root.title("E-duca system")
    root.geometry("1080x720")
    my_tree = ttk.Treeview(root)

    #placeholders for entry
    ph1 = tk.StringVar()
    ph2 = tk.StringVar()
    ph3 = tk.StringVar()
    ph4 = tk.StringVar()
    ph5 = tk.StringVar()

    #placeholder set value function
    def setph(word,num):
        if num ==1:
            ph1.set(word)
        if num ==2:
            ph2.set(word)
        if num ==3:
            ph3.set(word)
        if num ==4:
            ph4.set(word)
        if num ==5:
            ph5.set(word)

    def read():
        conn = connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM alunos")
        results = cursor.fetchall()
        conn.commit()
        conn.close()
        return results

    def add():
        id = str(idEntry.get())
        cpf = str(cpfEntry.get())
        nome = str(nomeEntry.get())
        curso = str(cursoEntry.get())
        email = str(emailEntry.get())
        if (id.strip() == "" or cpf.strip() == "" or nome.strip() == "" or curso.strip() == "" or email.strip() == ""):
            messagebox.showinfo("Error", "Please fill up the blank entry")
        else:
            try:
                conn = connection()
                cursor = conn.cursor()
                
                # Using parameterized query to avoid SQL injection
                query = "INSERT INTO alunos VALUES (%s, %s, %s, %s, %s)"
                values = (id, cpf, nome, curso, email)
                
                cursor.execute(query, values)
                conn.commit()
            except:
                messagebox.showinfo("Error", "id já cadastrado")
                return
        refreshTable()
        

    def reset():
        decision = messagebox.askquestion("Warning!!", "Delete all data?")
        if decision != "yes":
            return 
        else:
            try:
                conn = connection()
                cursor = conn.cursor()
                cursor.execute("DELETE FROM alunos")
                conn.commit()
                conn.close()
            except:
                messagebox.showinfo("Error", "Sorry an error occured")
                return

            refreshTable()

    def delete():
        decision = messagebox.askquestion("Warning!!", "Delete the selected data?")
        if decision != "yes":
            return 
        else:
            selected_item = my_tree.selection()[0]
            deleteData = str(my_tree.item(selected_item)['values'][0])
            try:
                conn = connection()
                cursor = conn.cursor()
                cursor.execute("DELETE FROM alunos WHERE id='"+str(deleteData)+"'")
                conn.commit()
                conn.close()
            except:
                messagebox.showinfo("Error", "Sorry an error occured")
                return

            refreshTable()

    def select():
        try:
            selected_item = my_tree.selection()[0]
            id = str(my_tree.item(selected_item)['values'][0])
            cpf = str(my_tree.item(selected_item)['values'][1])
            nome = str(my_tree.item(selected_item)['values'][2])
            curso = str(my_tree.item(selected_item)['values'][3])
            email = str(my_tree.item(selected_item)['values'][4])

            setph(id,1)
            setph(cpf,2)
            setph(nome,3)
            setph(curso,4)
            setph(email,5)
        except:
            messagebox.showinfo("Error", "Please select a data row")

    def search():
        id = str(idEntry.get())
        cpf = str(cpfEntry.get())
        nome = str(nomeEntry.get())
        curso = str(cursoEntry.get())
        email = str(emailEntry.get())

        conn = connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM alunos WHERE id='"+
        id+"' or cpf='"+
        cpf+"' or nome='"+
        nome+"' or curso='"+
        curso+"' or email='"+
        email+"' ")
        
        try:
            result = cursor.fetchall()

            for num in range(0,5):
                setph(result[0][num],(num+1))

            conn.commit()
            conn.close()
        except:
            messagebox.showinfo("Error", "No data found")

    def update():
        selectedid = ""

        try:
            selected_item = my_tree.selection()[0]
            selectedid = str(my_tree.item(selected_item)['values'][0])
        except:
            messagebox.showinfo("Error", "Please select a data row")

        id = str(idEntry.get())
        cpf = str(cpfEntry.get())
        nome = str(nomeEntry.get())
        curso = str(cursoEntry.get())
        email = str(emailEntry.get())

        if (id == "" or id == " ") or (cpf == "" or cpf == " ") or (nome == "" or nome == " ") or (curso == "" or curso == " ") or (email == "" or email == " "):
            messagebox.showinfo("Error", "Please fill up the blank entry")
            return
        else:
                conn = connection()
                cursor = conn.cursor()
                cursor.execute("UPDATE alunos SET id='"+
                id+"', cpf='"+
                cpf+"', nome='"+
                nome+"', curso='"+
                curso+"', email='"+
                email+"' WHERE id='"+
                selectedid+"' ")
                conn.commit()
                conn.close()
                return

        refreshTable()

    label = Label(root, text="E-duca registration system", font=('Arial Bold', 30))
    label.grid(row=0, column=0, columnspan=8, rowspan=2, padx=50, pady=40)

#o que vai aparecer para o usuário introduzir
    idLabel = Label(root, text="ID", font=('Arial', 15))
    cpfLabel = Label(root, text="CPF", font=('Arial', 15))
    nomeLabel = Label(root, text="Nome", font=('Arial', 15))
    cursoLabel = Label(root, text="Curso", font=('Arial', 15))
    emailLabel = Label(root, text="E-mail", font=('Arial', 15))

    idLabel.grid(row=3, column=0, columnspan=1, padx=50, pady=5)
    cpfLabel.grid(row=4, column=0, columnspan=1, padx=50, pady=5)
    nomeLabel.grid(row=5, column=0, columnspan=1, padx=50, pady=5)
    cursoLabel.grid(row=6, column=0, columnspan=1, padx=50, pady=5)
    emailLabel.grid(row=7, column=0, columnspan=1, padx=50, pady=5)

#como fica a área para colocar os dados
    idEntry = Entry(root, width=55, bd=5, font=('Arial', 15), textvariable = ph1)
    cpfEntry = Entry(root, width=55, bd=5, font=('Arial', 15), textvariable = ph2)
    nomeEntry = Entry(root, width=55, bd=5, font=('Arial', 15), textvariable = ph3)
    cursoEntry = Entry(root, width=55, bd=5, font=('Arial', 15), textvariable = ph4)
    emailEntry = Entry(root, width=55, bd=5, font=('Arial', 15), textvariable = ph5)

    idEntry.grid(row=3, column=1, columnspan=4, padx=5, pady=0)
    cpfEntry.grid(row=4, column=1, columnspan=4, padx=5, pady=0)
    nomeEntry.grid(row=5, column=1, columnspan=4, padx=5, pady=0)
    cursoEntry.grid(row=6, column=1, columnspan=4, padx=5, pady=0)
    emailEntry.grid(row=7, column=1, columnspan=4, padx=5, pady=0)

#colocar os botões na tela
    addBtn = Button(
        root, text="Add", padx=65, pady=25, width=10,
        bd=5, font=('Arial', 15), bg="#002a7c", command=add)
    updateBtn = Button(
        root, text="Update", padx=65, pady=25, width=10,
        bd=5, font=('Arial', 15), bg="#002d82", command=update)
    deleteBtn = Button(
        root, text="Delete", padx=65, pady=25, width=10,
        bd=5, font=('Arial', 15), bg="#5b61a1", command=delete)
    searchBtn = Button(
        root, text="Search", padx=65, pady=25, width=10,
        bd=5, font=('Arial', 15), bg="#838abd", command=search)
    resetBtn = Button(
        root, text="Reset", padx=65, pady=25, width=10,
        bd=5, font=('Arial', 15), bg="#c5d4eb", command=reset)
    selectBtn = Button(
        root, text="Select", padx=65, pady=25, width=10,
        bd=5, font=('Arial', 15), bg="#dfe9f5", command=select)

    addBtn.grid(row=3, column=5, columnspan=1, rowspan=2)
    updateBtn.grid(row=5, column=5, columnspan=1, rowspan=2)
    deleteBtn.grid(row=7, column=5, columnspan=1, rowspan=2)
    searchBtn.grid(row=9, column=5, columnspan=1, rowspan=2)
    resetBtn.grid(row=11, column=5, columnspan=1, rowspan=2)
    selectBtn.grid(row=13, column=5, columnspan=1, rowspan=2)

#configuração da árvore
    style = ttk.Style()
    style.configure("Treeview.Heading", font=('Arial Bold', 15))

#colunas da árvore
    my_tree['columns'] = ("ID","CPF","Nome","Curso","email")

#identificação de cada coluna
    my_tree.column("#0", width=0, stretch=NO)
    my_tree.column("ID", anchor=W, width=170)
    my_tree.column("CPF", anchor=W, width=150)
    my_tree.column("Nome", anchor=W, width=150)
    my_tree.column("Curso", anchor=W, width=165)
    my_tree.column("email", anchor=W, width=150)

#o que vai dentro da coluna
    my_tree.heading("ID", text="ID", anchor=W)
    my_tree.heading("CPF", text="CPF", anchor=W)
    my_tree.heading("Nome", text="Nome", anchor=W)
    my_tree.heading("Curso", text="Curso", anchor=W)
    my_tree.heading("email", text="email", anchor=W)

    refreshTable()

    root.mainloop()

def JanelaAula():
    def connection():
        conn = pymysql.connect(
            host='localhost',
            user='root', 
            password='030506',
            db='bancoeduca',
        )
        return conn

    def refreshTable():
        for data in my_tree.get_children():
            my_tree.delete(data)

        for array in read():
            my_tree.insert(parent='', index='end', iid=array, text="", values=(array), tag="orow")

        my_tree.tag_configure('orow', background='#EEEEEE', font=('Arial', 12))
        my_tree.grid(row=8, column=0, columnspan=5, rowspan=11, padx=10, pady=20)

    root = Tk()
    root.title("E-duca system")
    root.geometry("1080x720")
    my_tree = ttk.Treeview(root)

    #placeholders for entry
    ph1 = tk.StringVar()
    ph2 = tk.StringVar()
    ph3 = tk.StringVar()
    ph4 = tk.StringVar()
    ph5 = tk.StringVar()

    #placeholder set value function
    def setph(word,num):
        if num ==1:
            ph1.set(word)
        if num ==2:
            ph2.set(word)
        if num ==3:
            ph3.set(word)
        if num ==4:
            ph4.set(word)
        if num ==5:
            ph5.set(word)

    def read():
        conn = connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM cursos")
        results = cursor.fetchall()
        conn.commit()
        conn.close()
        return results

    def add():
        id = str(idEntry.get())
        professor = str(professorEntry.get())
        nome = str(nomeEntry.get())
        duracao = str(duracaoEntry.get())
        formacao = str(formacaoEntry.get())
        if (id.strip() == "" or professor.strip() == "" or nome.strip() == "" or formacao.strip() == "" or duracao.strip() == ""):
            messagebox.showinfo("Error", "Please fill up the blank entry")
        else:
            try:    
                conn = connection()
                cursor = conn.cursor()
                
                # Using parameterized query to avoid SQL injection
                query = "INSERT INTO cursos VALUES (%s, %s, %s, %s, %s)"
                values = (id, professor, nome, duracao, formacao)
                
                cursor.execute(query, values)
                conn.commit()
            except:
                messagebox.showinfo("Error", "ID já cadastrado")
        refreshTable()
        

    def reset():
        decision = messagebox.askquestion("Warning!!", "Delete all data?")
        if decision != "yes":
            return 
        else:
            try:
                conn = connection()
                cursor = conn.cursor()
                cursor.execute("DELETE FROM cursos")
                conn.commit()
                conn.close()
            except:
                messagebox.showinfo("Error", "Sorry an error occured")
                return

            refreshTable()

    def delete():
        decision = messagebox.askquestion("Warning!!", "Delete the selected data?")
        if decision != "yes":
            return 
        else:
            selected_item = my_tree.selection()[0]
            deleteData = str(my_tree.item(selected_item)['values'][0])
            try:
                conn = connection()
                cursor = conn.cursor()
                cursor.execute("DELETE FROM cursos WHERE id='"+str(deleteData)+"'")
                conn.commit()
                conn.close()
            except:
                messagebox.showinfo("Error", "Sorry an error occured")
                return

            refreshTable()

    def select():
        try:
            selected_item = my_tree.selection()[0]
            id = str(my_tree.item(selected_item)['values'][0])
            professor = str(my_tree.item(selected_item)['values'][1])
            nome = str(my_tree.item(selected_item)['values'][2])
            formacao = str(my_tree.item(selected_item)['values'][3])
            duracao = str(my_tree.item(selected_item)['values'][4])

            setph(id,1)
            setph(professor,2)
            setph(nome,3)
            setph(formacao,4)
            setph(duracao,5)
        except:
            messagebox.showinfo("Error", "Please select a data row")

    def search():
        id = str(idEntry.get())
        professor = str(professorEntry.get())
        nome = str(nomeEntry.get())
        formacao = str(formacaoEntry.get())
        duracao = str(duracaoEntry.get())

        conn = connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM cursos WHERE id='"+
        id+"' or professor='"+
        professor+"' or nome='"+
        nome+"' or formacao='"+
        formacao+"' or duracao='"+
        duracao+"' ")
        
        try:
            result = cursor.fetchall()

            for num in range(0,5):
                setph(result[0][num],(num+1))

            conn.commit()
            conn.close()
        except:
            messagebox.showinfo("Error", "No data found")

    def update():
        selectedid = ""
        try:
            selected_item = my_tree.selection()[0]
            selectedid = str(my_tree.item(selected_item)['values'][0])
        except:
            messagebox.showinfo("Error", "Please select a data row")

        id = str(idEntry.get())
        professor = str(professorEntry.get())
        nome = str(nomeEntry.get())
        formacao = str(formacaoEntry.get())
        duracao = str(duracaoEntry.get())

        if (id == "" or id == " ") or (professor == "" or professor == " ") or (nome == "" or nome == " ") or (formacao == "" or formacao == " ") or (duracao == "" or duracao == " "):
            messagebox.showinfo("Error", "Please fill up the blank entry")
            return
        else:
                conn = connection()
                cursor = conn.cursor()
                cursor.execute("UPDATE cursos SET id='"+
                id+"', professor='"+
                professor+"', nome='"+
                nome+"', formacao='"+
                formacao+"', duracao='"+
                duracao+"' WHERE id='"+
                selectedid+"' ")
                conn.commit()
                conn.close()

        refreshTable()

    label = Label(root, text="E-duca registration system", font=('Arial Bold', 30))
    label.grid(row=0, column=0, columnspan=8, rowspan=2, padx=50, pady=40)

#o que vai aparecer para o usuário introduzir
    idLabel = Label(root, text="ID", font=('Arial', 15))
    professorLabel = Label(root, text="Professor", font=('Arial', 15))
    nomeLabel = Label(root, text="nome", font=('Arial', 15))
    formacaoLabel = Label(root, text="formacao", font=('Arial', 15))
    duracaoLabel = Label(root, text="duracao", font=('Arial', 15))

    idLabel.grid(row=3, column=0, columnspan=1, padx=50, pady=5)
    professorLabel.grid(row=4, column=0, columnspan=1, padx=50, pady=5)
    nomeLabel.grid(row=5, column=0, columnspan=1, padx=50, pady=5)
    formacaoLabel.grid(row=6, column=0, columnspan=1, padx=50, pady=5)
    duracaoLabel.grid(row=7, column=0, columnspan=1, padx=50, pady=5)

#como fica a área para colocar os dados
    idEntry = Entry(root, width=55, bd=5, font=('Arial', 15), textvariable = ph1)
    professorEntry = Entry(root, width=55, bd=5, font=('Arial', 15), textvariable = ph2)
    nomeEntry = Entry(root, width=55, bd=5, font=('Arial', 15), textvariable = ph3)
    formacaoEntry = Entry(root, width=55, bd=5, font=('Arial', 15), textvariable = ph4)
    duracaoEntry = Entry(root, width=55, bd=5, font=('Arial', 15), textvariable = ph5)

    idEntry.grid(row=3, column=1, columnspan=4, padx=5, pady=0)
    professorEntry.grid(row=4, column=1, columnspan=4, padx=5, pady=0)
    nomeEntry.grid(row=5, column=1, columnspan=4, padx=5, pady=0)
    formacaoEntry.grid(row=6, column=1, columnspan=4, padx=5, pady=0)
    duracaoEntry.grid(row=7, column=1, columnspan=4, padx=5, pady=0)

#colocar os botões na tela
    addBtn = Button(
        root, text="Add", padx=65, pady=25, width=10,
        bd=5, font=('Arial', 15), bg="#002a7c", command=add)
    updateBtn = Button(
        root, text="Update", padx=65, pady=25, width=10,
        bd=5, font=('Arial', 15), bg="#002d82", command=update)
    deleteBtn = Button(
        root, text="Delete", padx=65, pady=25, width=10,
        bd=5, font=('Arial', 15), bg="#5b61a1", command=delete)
    searchBtn = Button(
        root, text="Search", padx=65, pady=25, width=10,
        bd=5, font=('Arial', 15), bg="#838abd", command=search)
    resetBtn = Button(
        root, text="Reset", padx=65, pady=25, width=10,
        bd=5, font=('Arial', 15), bg="#c5d4eb", command=reset)
    selectBtn = Button(
        root, text="Select", padx=65, pady=25, width=10,
        bd=5, font=('Arial', 15), bg="#dfe9f5", command=select)

    addBtn.grid(row=3, column=5, columnspan=1, rowspan=2)
    updateBtn.grid(row=5, column=5, columnspan=1, rowspan=2)
    deleteBtn.grid(row=7, column=5, columnspan=1, rowspan=2)
    searchBtn.grid(row=9, column=5, columnspan=1, rowspan=2)
    resetBtn.grid(row=11, column=5, columnspan=1, rowspan=2)
    selectBtn.grid(row=13, column=5, columnspan=1, rowspan=2)

#configuração do banco
    style = ttk.Style()
    style.configure("Treeview.Heading", font=('Arial Bold', 15))

#colunas da árvore
    my_tree['columns'] = ("ID","Nome","Duração","Professor","Formacao")

#identificação de cada coluna
    my_tree.column("#0", width=0, stretch=NO)
    my_tree.column("ID", anchor=W, width=170)
    my_tree.column("Nome", anchor=W, width=150)
    my_tree.column("Duração", anchor=W, width=150)
    my_tree.column("Professor", anchor=W, width=165)
    my_tree.column("Formacao", anchor=W, width=150)

#o que vai dentro da coluna
    my_tree.heading("ID", text="ID", anchor=W)
    my_tree.heading("Nome", text="Nome", anchor=W)
    my_tree.heading("Duração", text="Duração", anchor=W)
    my_tree.heading("Professor", text="Professor", anchor=W)
    my_tree.heading("Formacao", text="Formacao", anchor=W)



    refreshTable()

    root.mainloop()

def main():
    root.title("E-duca system")
    root.geometry("250x180")
    my_tree = ttk.Treeview(root)

    BtnAluno = Button(
        root, text="Alunos", padx=65, pady=25, width=10,
        bd=5, font=('Arial', 15), bg="#002a7c", command=JanelaAluno)
    BtnAula = Button(
        root, text="Aulas", padx=65, pady=25, width=10,
        bd=5, font=('Arial', 15), bg="#002d82", command=JanelaAula)

    BtnAluno.grid(row=3, column=5, columnspan=1, rowspan=2)
    BtnAula.grid(row=5, column=5, columnspan=1, rowspan=2)

main()
root.mainloop()