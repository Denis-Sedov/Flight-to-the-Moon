from tkinter import *
from tkinter import ttk, font
import Way_to_the_Moon


def center_window(main):  # Центрирование окна на экране.
    w = 960
    h = 720
    sw = main.winfo_screenwidth()
    sh = main.winfo_screenheight()
    x = (sw - w) / 2
    y = (sh - h) / 2
    main.geometry('%dx%d+%d+%d' % (w, h, x, y))


def authorslist():  # Создание окна с авторами проекта.
    frame = ttk.Frame(root)
    back = ttk.Button(frame, text='Back', command=lambda: main())
    author = ttk.Label(frame, text='''
    Authors:
    
    polinashabanan
    atlantida39
    AntonShubnic
    Esmantovich-Maksim
    korzin-andrey
    Denis-Sedov
    ''')
    tutor = ttk.Label(frame, text='''
    Tutors:
    
    Mikhail Dvorkin
    Alexander Zinchik 
    Konstantin Ladutenko
    ''')
    frame.grid(column=0, row=0, sticky=(N, S, E, W))
    author.grid(column=0, row=0, sticky=(N, S))
    tutor.grid(column=0, row=0, sticky=(S, W), padx=20, pady=20)
    back.grid(column=0, row=0, sticky=(S, E), padx=20, pady=40)
    frame.rowconfigure(0, weight=1)
    frame.columnconfigure(0, weight=1)


def main():  # Основное окно выбора этапа для визуализации.
    content = ttk.Frame(root)
    frame = ttk.Frame(content, borderwidth=5, relief="groove", width=200, height=100)
    buttonframe = ttk.Frame(content)
    label = ttk.Label(buttonframe, text="Which part do You want to visualize?")
    start = ttk.Button(buttonframe, text="Start")
    quitB = ttk.Button(buttonframe, text="Quit", command=lambda: quit())
    authors = ttk.Button(buttonframe, text="Project authors", command=lambda: authorslist())
    partvar = StringVar()
    parts = ttk.Combobox(buttonframe, textvariable=partvar)
    content.grid(column=0, row=0, sticky=(N, S, E, W))
    frame.grid(column=0, row=0, columnspan=3, rowspan=4, sticky=(N, S, E, W))
    buttonframe.grid(column=3, row=0, rowspan=4, sticky=(N, S, E, W))
    label.grid(column=0, row=0, sticky=N, pady=10, padx=5)
    parts.grid(column=0, row=1, sticky=(N, E, W), padx=10)
    start.grid(column=0, row=3, sticky=N)
    quitB.grid(column=0, row=3, sticky=S)
    authors.grid(column=0, row=4, sticky=S, pady=50)
    parts.bind('<<ComboboxSelected>>')
    parts['values'] = ('Taking off', 'Way to the Moon', 'Landing on the Moon', 'Taking off the Moon',
                       'Way to the Earth', 'Landing on the Eart', 'All parts')
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)
    content.columnconfigure(0, weight=4)
    content.columnconfigure(1, weight=4)
    content.columnconfigure(2, weight=4)
    content.columnconfigure(3, weight=1)
    content.rowconfigure(0, weight=1)
    buttonframe.columnconfigure(0, weight=1)
    buttonframe.rowconfigure(1, weight=1)
    buttonframe.rowconfigure(2, weight=4)
    buttonframe.rowconfigure(3, weight=2)
    buttonframe.rowconfigure(4, weight=8)


if __name__ == '__main__':
    root = Tk()
    center_window(root)
    root.title('Flight to the Moon')
    main()
    root.mainloop()
