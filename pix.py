from tkinter import *

root = Tk()

root.title("Gerador de Código QR Pix")
root.geometry("500x500")
root.iconbitmap("sources/icon.ico")

configlabel = Label(root, text="Configure o valor", font=25).grid(column=5, row= 0)

perg_valor = Label(root, text="Valor:", font=25)
perg_valor.grid(column=0, row=1, sticky=W, padx=5, pady=5)

simbolo_rs = Label(root, text="R$", font=25)
simbolo_rs.grid(column=1, row = 1, sticky=E)

resp_reais = Entry(root, width=5, font=25, justify=CENTER)
resp_reais.insert(0, "0")
resp_reais.grid(column=2, row=1, sticky=W, pady=5)

virgula = Label(root, text=",", font=25)
virgula.grid(column=3, row=1, pady=5, sticky=W)

resp_centavos = Entry(root, width=2, font=25, justify=CENTER)
resp_centavos.insert(0,"00")
resp_centavos.grid(column=4, row=1, sticky=W, pady=5)

perg_identificador = perg_valor = Label(text="Identificador:", font=25)
perg_identificador.grid(column=0, row=2, padx=5, pady=5)

resp_identificador = Entry(root, font=25, justify=CENTER)
resp_identificador.grid(column=1, row=2, padx=5, pady=5, columnspan=5)

def open() :




    # Faz o QR Code
    cor = "black"
    fundo = "white"
    imagem = ""
    nome = "Del Chiaro"
    chave = "06524647858"
    regiao = "SAO PAULO"
    reais = resp_reais.get()
    centavos = resp_centavos.get()
    identificador = resp_identificador.get()
    if reais == "":
        reais = "0"
    if centavos == "":
        centavos = "00"

    # Faz o código PIX
    from pixqrcode import PixQrCode

    pix = PixQrCode(nome, chave, regiao,f"{reais}{centavos}",identificador)
    save = f"{reais}_codigo_{identificador}"
    codigo = pix.generate_code()

    # Tranforma em QR
    import qrcode
    qr = qrcode.QRCode()
    qr.add_data(codigo)
    qr.make()
    img = qr.make_image(fill_color= cor, back_color=fundo).convert('RGB')

    if imagem != "" :
       from PIL import Image
       logo = Image.open(imagem)
       basewidth = 100

       # Coloca a imagem

       wpercent = (basewidth/float(logo.size[0]))
       hsize = int((float(logo.size[1])*float(wpercent)))
       logo = logo.resize((basewidth, hsize), Image.Resampling.LANCZOS)

       pos = ((img.size[0] - logo.size[0]) // 2,
              (img.size[1] - logo.size[1]) // 2)

       img.paste(logo, pos)
       img.save(f"qrcodes/{save}.png")
    else:
        img.save(f"qrcodes/{save}.png")

    # Abre o QR Code
  
    top = Toplevel()
    top.title("Escaneie para pagar")
    top.iconbitmap("sources/icon.ico")
    pdser = Label(top, text="Pode Ser PIX?", font=80).pack()
    bv = Label(top, text="Abra o aplicativo do seu banco e escaneie:", font=25).pack()
    ivalor = Label(top, text=f"Valor: {reais},{centavos}", font=50)
    ivalor.pack()

    from PIL import ImageTk

    qrimg = ImageTk.PhotoImage(file=f"qrcodes/{save}.png")
    qrlabel = Label(top, image=qrimg).pack()

    # Informações sobre o código

    info = Label(top, text="Informações:")
    inome = Label(top, text=f"Nome: {nome}")
    ichave = Label(top, text=f"Chave: {chave}")
    iregiao = Label(top, text=f"Região: {regiao}")
    iidentificador = Label(top, text=f"Identificador: {identificador}")

    icopy = Text(top, width=20 ,height=1)
    icopy.insert(INSERT, codigo)
    icopy.configure(state=DISABLED)

    def copy_select():
        import pyperclip
        pyperclip.copy(codigo)

    button_copy = Button(top,text="Copiar",command=lambda:copy_select())

    info.pack()
    inome.pack()
    ichave.pack()
    iregiao.pack()
    iidentificador.pack()
    icopy.pack()
    button_copy.pack()

button = Button(root,text="Gerar Código PIX", command=open)
button.grid(column=5, row= 5)

root.mainloop()
