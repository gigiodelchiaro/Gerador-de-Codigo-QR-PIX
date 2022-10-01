from PIL import ImageTk
from tkinter import *
from pixqrcode import PixQrCode
import qrcode
import pyperclip
root = Tk()

root.title("Gerador de Código QR Pix")
root.geometry("500x500")
root.iconbitmap("sources/icon.ico")
configlabel = Label(root, text="Configure a conta bancária que irá receber").pack()
perg_nome = Label(root, text="Nome da Empresa:").pack()
resp_nome = Entry(root)
resp_nome.pack()
perg_chave = Label(root, text="Chave PIX:").pack()
resp_chave = Entry(root)
resp_chave.pack()
perg_regiao = Label(root, text="Região (Ex. São Paulo):").pack()
resp_regiao = Entry(root)
resp_regiao.pack()
perg_reais = Label(root, text="Reais:").pack()
resp_reais = Entry(root)
resp_reais.pack()
perg_centavos = Label(root, text="Centavos:").pack()
resp_centavos = Entry(root)
resp_centavos.pack()
perg_identificador = perg_valor = Label(text="Identificação (opcional):").pack()
resp_identificador = Entry(root)
resp_identificador.pack()

def open() :
    global qrcode
    # Faz o QR Code

    nome = resp_nome.get()
    chave = resp_chave.get()
    regiao = resp_regiao.get()
    reais = resp_reais.get()
    centavos = resp_centavos.get()
    if reais == "":
        reais = "0"
    if centavos == "":
        centavos = "00"
    if nome ==  "":
        nome = "Del Chiaro"
    if chave == "":
        chave = "05622974000120"
    if regiao == "":
        regiao = "SAO PAULO"

    identificador = resp_identificador.get()
    pix = PixQrCode(str(nome), str(chave), str(regiao), reais + centavos, str(identificador))
    save = reais + "_codigo_" + identificador
    pix.save_qrcode("qrcodes",save)
    codigo = pix.generate_code()

    # Abre o QR Code
  
    top = Toplevel()
    top.title("Escaneie para pagar")
    bv = Label(top, text="Código QR:").pack()
    top.iconbitmap("sources/icon.ico")
    qrcode = ImageTk.PhotoImage(file="qrcodes/" + save + ".png")
    qrlabel = Label(top, image=qrcode).pack()

    # Informações sobre o código

    info = Label(top, text="Informações:")
    inome = Label(top, text="Nome: " + nome)
    ichave = Label(top, text="Chave: " + chave)
    iregiao = Label(top, text="Região: " + regiao)
    ivalor = Label(top, text="Valor:" + reais + "," + centavos)
    iidentificador = Label(top, text="Identificador: " + identificador)

    icopy = Text(top, width=20 ,height=1)
    icopy.insert(INSERT, codigo)
    icopy.configure(state=DISABLED)

    def copy_select():
        pyperclip.copy(codigo)

    button_copy = Button(top,text="Copiar",command=lambda:copy_select())

    info.pack()
    inome.pack()
    ichave.pack()
    iregiao.pack()
    ivalor.pack()
    iidentificador.pack()
    icopy.pack()
    button_copy.pack()

button = Button(root,text="Gerar Código PIX", command=open)
button.pack()

root.mainloop()