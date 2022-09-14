import tkinter as tk
from typing import List
import re
import math

janela = tk.Tk()
class FuncoesDosBotoes(): #Realiza as operações da calculadora
    def colocar_valor_do_botao_no_display(self,event=None)-> None: #Chama as funções dos botões da interface gráfica
        lista_de_botoes = self.lista_de_botoes

        for linha_dos_botao in lista_de_botoes:
            for botao in linha_dos_botao:
                texto = botao["text"]

                if texto in "0123456789.+-/*()^":
                    botao.bind("<Button-1>",self.insere_valor_no_display)

                if texto == "C":
                    botao.bind("<Button-1>",self.limpa_valores_do_display)

                if texto == "=":
                    botao.bind("<Button-1>",self.calcula_resultado)

    def tratamento_de_valores_digitados(self,texto): #Retira caracteres inválidos para o cálculo
        texto = self.display.get()
        # Remove tudo que não for 0123456789/*-+()
        texto_formatado = re.sub(r'[^\d\.\/\*\-\+\(\^\)\^e]',r'', texto)
        # Remove valores duplicados (.+/-*^)
        texto_formatado = re.sub(r'([\.\+\/\-\*\^])\1+', r'\1', texto_formatado, 0)
        # Remove *() or ()
        texto_formatado = re.sub(r'\*?\(\)', '', texto_formatado)
        # Quando possui exponenciação ela divide em duas tratar casos de resultados muito grandes mais a frente
        texto_formatado = re.split(r'\^',texto_formatado,0)
        return texto_formatado

    def insere_valor_no_display(self,event=None): #Função que insere os valores dos botões no display
        self.display.insert("end",event.widget["text"])
        self.display.focus()
        
    def limpa_valores_do_display(self,event=None): #Função que limpa o display de entrada de valores
        self.display.delete(0,"end")
    
    def calcula_resultado(self,event=None): #Função que realiza o cálculo
        expressao_para_calcular = self.tratamento_de_valores_digitados(self.display.get())
        try:
            if len(expressao_para_calcular) == 1:
                resultado = eval(expressao_para_calcular[0])

            else:
                resultado = eval(expressao_para_calcular[0])
                for expressao in expressao_para_calcular[1:]:
                    resultado = math.pow(resultado, eval(expressao))
            
            self.limpa_valores_do_display()
            self.display.insert("end",resultado)
            self.resultados.config(text= f"{expressao_para_calcular} = {resultado}")

        except OverflowError:
            self.resultados.config(text= "Cálculo Não Suportado!")
        except Exception:
            self.resultados.config(text= "Conta Inválida")

class Calculadora(FuncoesDosBotoes): #Configuração da interface gráfica
    def __init__(self) -> None:
        self.janela = janela
        self.config_janela()
        self.lista_de_botoes = self.criar_botao()
        self.tela_entrada_valor()
        self.label_de_resultado()
        self.colocar_valor_do_botao_no_display()
        janela.mainloop()

    def config_janela(self):
        self.janela.title("Calculadora")
        self.janela.configure(background = "#fff")
        self.janela.geometry("455x465")
        self.janela.resizable(False,False)

    def tela_entrada_valor(self) -> tk.Entry: #Entrada onde é digitado os valores
        self.display = tk.Entry(self.janela)
        self.display.grid(row=0, column=0, columnspan=5, sticky='news', padx=5, pady=5)
        self.display.config(
            font=('Helvetica', 30, 'bold'),
            justify='right', bd=1, relief='flat',
            highlightthickness=1, highlightcolor='#ccc'
        )
        return self.display
    
    def label_de_resultado(self): #Label abaixo da entrada de valores
        self.resultados = tk.Label(self.janela)
        self.resultados.grid(row=1, column=0, columnspan=5, sticky='news', padx=5, pady=0)
        self.resultados.config(
            text='Sem conta ainda',
        anchor='e', justify='right', background='#fff'
        )

    def criar_botao(self) -> List[List[tk.Button]]: #Configurando os botões e adicionando à uma lista
        textos_dos_botoes: List[List[str]] = [['7', '8', '9', '+', 'C'], ['4', '5', '6', '-', '/'], ['1', '2', '3', '*', '^'], ['0', '.', '(', ')', '=']]
        lista_dos_botoes: List[List[tk.Button]] = []

        for linha, linha_value in enumerate(textos_dos_botoes, start=2):
            botao_linha = []

            for coluna, coluna_value in enumerate(linha_value):
                btn = tk.Button(self.janela,text=coluna_value)
                btn.grid(row=linha, column=coluna, sticky='news', padx=5, pady=5)
                btn.config(
                    font=('Helvetica', 13, 'normal'),
                    pady=30, width=1, background='#f1f2f3',bd=0,
                    cursor='hand2', highlightthickness=0,
                    highlightcolor='#ccc', activebackground='#ccc',
                    highlightbackground='#ccc'
                            )
                botao_linha.append(btn)
            lista_dos_botoes.append(botao_linha)
        #Formatando botões de cores diferentes
        for linha_dos_botao in lista_dos_botoes:
            for botao in linha_dos_botao:
                texto = botao["text"]

                if texto in ".+-/*()^":
                    botao.config(bg='#c0c1c2')

                if texto == "C":
                    botao.config(bg='#4785F4', fg='#fff')

                if texto == "=":
                    botao.config(bg='#EA4335', fg='#fff')

        return lista_dos_botoes

Calculadora()
