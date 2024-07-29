import os
import sys
from customtkinter import CTk, CTkFrame, CTkButton, CTkLabel
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

def soma(x, y):
    return x + y

def subtracao(x, y):
    return x - y

def multiplicacao(x,y):
    return x * y

def dividir(x, y):
    if y == 0:
        raise ValueError ("Divisão por zero!")
    return x / y

def quadrado(x):
    return x * x

def sqrt(x):
    return x ** 0.5

def log(x):
    return 1 / x

def porcentagem(x):
    return x / 100

def calcular_expressao(current_num):
    if not current_num:  # Se current_num estiver vazio, retorna um erro
        pass

    numeros = []
    op = []
    temp = ''

    for char in current_num:
        if char in '+-*/^√l%i':
            if temp:  # Se temp não estiver vazio, adiciona ao numeros
                numeros.append(float(temp))
                temp = ''
            op.append(char)
        else:
            temp += char
        
    if temp:  # Se temp não estiver vazio, adiciona ao numeros
        numeros.append(float(temp))

    # Processando o Sinal
    # i = 0
    # while i < len(op):
    #     if op[i] == 'i':
    #         numeros[i] = -numeros[i]
    #         del op[i]
    #     else:
    #         i += 1

    # Processando a Porcentagems
    i = 0
    while i < len(op):
        if op[i] == '%':
            numeros[i] = porcentagem(numeros[i])
            del op[i]
        else:
            i += 1

    # Processando o Logaritmo Natural
    i = 0
    while i < len(op):
        if op[i] == 'l':
            numeros[i] = log(numeros[i])
            del op[i]
        else:
            i += 1

    # Processando a Potência e Raiz Quadrada
    i = 0
    while i < len(op):
        if op[i] == '^':
            numeros[i] = quadrado(numeros[i])
            del op[i]
        elif op[i] == '√':
            numeros[i] = sqrt(numeros[i])
            del op[i]
        else:
            i += 1

    # Multiplicação e Divisão
    i = 0
    while i < len(op):
        if op[i] == '*':
            numeros[i] = multiplicacao(numeros[i], numeros[i+1])
            del numeros[i+1]
            del op[i]
        elif op[i] == '/':
            numeros[i] = dividir(numeros[i], numeros[i+1])
            del numeros[i+1]
            del op[i]
        else:
            i += 1

    # Processando a Soma e Subtração
    i = 0
    while i < len(op):
        if op[i] == '+':
            numeros[i] = soma(numeros[i], numeros[i+1])
            del numeros[i+1]
            del op[i]
        elif op[i] == '-':
            numeros[i] = subtracao(numeros[i], numeros[i+1])
            del numeros[i+1]
            del op[i]
        else:
            i += 1
    return numeros[0]

# Classe para lidar com eventos de arquivo
class ReloadHandler(FileSystemEventHandler):
    def __init__(self, app):
        self.app = app

    def on_modified(self, event):
        if event.src_path.endswith('.py'):
            print(f'{event.src_path} modificado, recarregando aplicação...')
            os.execv(sys.executable, ['python'] + sys.argv)

class Calculator:
    def __init__(self, master):
        self.master = master
        self.master.title("Calculator")
        self.master.geometry("318x500")
        self.master.resizable(False, False)
        self.master.configure(bg="white")
        
        self.current_num = ""
        self.current_list = []
        self.resultado = ""

        # Criando os botões:
        self.screen_app = CTkFrame(self.master, bg_color="white", corner_radius=False)
        self.screen_app.pack(fill="both", expand=True)

        # Exibir o resultado:
        self.show_result = CTkLabel(self.screen_app, width=318, height=140, fg_color="transparent", text="", text_color='white', font=('Arial', 75), bg_color="#44343c", justify="right", anchor="se")
        self.show_result.place(x=0, y=0)

        # Copiando o resultado da expressão para a tela da calculadora:
        def update_display():
            self.show_result.configure(text=self.current_num)

        # Atualiza o display com o resultado
        def display_resultado():
            self.show_result.configure(text=self.resultado)

        def expression(num):
            if num != "":
                self.current_list.append(str(num))
                self.current_num = ''.join(self.current_list)
                update_display()

        def calcular():
            try:
                self.resultado = str(calcular_expressao(self.current_num))
                display_resultado()
            except Exception as e:
                print(f"Erro ao calcular a expressão: {e}")
                self.current_num = ""
                self.current_list = []
                self.resultado = ""

        def clear_current_num(self):
            self.current_num = ""
            self.current_list = []
            self.resultado = ""
            update_display()

        def clear_pop_num(self):
            self.current_num = self.current_num[:-1]
            update_display()

        # Front-End ->  Com os espaçamentos e tamanhos dos botões
        button_posx = 0
        button_posy = 380
        button_width = 79
        button_height = 60
        font_buttons = ("Arial", 20)
        self.buttons = []

        button = CTkButton(self.screen_app, text=" = ", width=button_width, height=button_height, fg_color="#34648c", hover_color="#44343c", corner_radius= False, font=(font_buttons), command=lambda:calcular())
        button.place(x=238.5, y=440)

        button = CTkButton(self.screen_app, text="+/-", width=button_width, height=button_height, fg_color="transparent", hover_color="#44343c", corner_radius= False,font=(font_buttons), command=lambda:calcular())
        button.place(x=0, y=440)

        button = CTkButton(self.screen_app, text="0", width=button_width, height=button_height, fg_color="transparent", hover_color="#44343c", corner_radius= False,font=(font_buttons), command=lambda:expression("0"))
        button.place(x=79.5, y=440)

        button = CTkButton(self.screen_app, text=" . ", width=button_width, height=button_height, fg_color="transparent", hover_color="#44343c", corner_radius= False,font=(font_buttons), command=lambda:expression("."))
        button.place(x=159, y=440)

        button= CTkButton(self.screen_app, text="+", width=button_width, height=button_height, fg_color="transparent", hover_color="#44343c", corner_radius= False, font=(font_buttons), command=lambda:expression("+"))
        button.place(x=238.5, y=380)

        button = CTkButton(self.screen_app, text="-", width=button_width, height=button_height, fg_color="transparent", hover_color="#44343c", corner_radius= False, font=(font_buttons), command=lambda:expression("-"))
        button.place(x=238.5, y=320)

        button = CTkButton(self.screen_app, text="X", width=button_width, height=button_height, fg_color="transparent", hover_color="#44343c", corner_radius= False, font=(font_buttons), command=lambda:expression("*"))
        button.place(x=238.5, y=260)

        button = CTkButton(self.screen_app, text="÷", width=button_width, height=button_height, fg_color="transparent", hover_color="#44343c", corner_radius= False, font=(font_buttons), 
        command=lambda:expression("/"))
        button.place(x=238.5, y=200)

        button = CTkButton(self.screen_app, text="1/x", width=button_width, height=button_height, fg_color="transparent", hover_color="#44343c", corner_radius= False,font=(font_buttons), command=lambda:expression("l"))
        button.place(x=0, y=200)

        button = CTkButton(self.screen_app, text="x²", width=button_width, height=button_height, fg_color="transparent", hover_color="#44343c", corner_radius= False, font=(font_buttons), command=lambda:expression("^"))
        button.place(x=79.5, y=200)

        button = CTkButton(self.screen_app, text="√x", width=button_width, height=button_height, fg_color="transparent",hover_color="#44343c", corner_radius= False, font=(font_buttons), command=lambda:expression("√"))
        button.place(x=159, y=200)

        button = CTkButton(self.screen_app, text="%", width=button_width, height=button_height, fg_color="transparent",hover_color="#44343c", corner_radius= False, font=(font_buttons), command=lambda:expression("%"))
        button.place(x=0, y=140)

        button = CTkButton(self.screen_app, text="CE", width=button_width, height=button_height, fg_color="transparent",hover_color="#44343c", corner_radius= False, font=(font_buttons), command=lambda:clear_current_num(self))
        button.place(x=79.5, y=140)

        # Não implementado
        # button = CTkButton(self.screen_app, text="C", width=button_width, height=button_height, fg_color="transparent",hover_color="#44343c", font=(font_buttons), command=lambda:expression("clear_all"))
        # button.place(x=159, y=140)'

        button = CTkButton(self.screen_app, text="⌫", width=button_width, height=button_height, fg_color="transparent",hover_color="#44343c", font=(font_buttons), command=lambda:clear_pop_num(self))
        button.place(x=238.5, y=140)

        for i in range(9):
            button_num = i + 1
            button = CTkButton(self.screen_app, text=i+1, width=button_width, height=button_height, fg_color="transparent", hover_color="#44343c", corner_radius= False,font=(font_buttons),command=lambda num = button_num : expression(num))
            button.place(x=button_posx, y=button_posy)
            self.buttons.append(button)

            button_posx += button_width

            if button_posx + button_width > button_width * 3:
                button_posx = 0
                button_posy -= button_height

def run_app():
    root = CTk()
    app = Calculator(root)
    root.mainloop()

if __name__ == "__main__":
    observer = Observer()
    observer.schedule(ReloadHandler(None), path='.', recursive=False)
    observer.start()
    try:
        run_app()
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
