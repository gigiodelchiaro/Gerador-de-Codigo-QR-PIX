from tkinter import *

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
    from pixqrcode import PixQrCode
    pix = PixQrCode(nome, chave, regiao, f"{reais}{centavos}", identificador)
    save = f"{reais}_codigo_{identificador}"
    pix.save_qrcode("qrcodes",save)
    codigo = pix.generate_code()

    # Tranforma em QR
    import qrcode
    qr = qrcode.QRCode()
    qr.add_data(codigo)
    qr.make()
    cor = "black"
    background = "white"
    imagem = ""
    img = qr.make_image(fill_color=cor, back_color=background).convert('RGB')

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
    bv = Label(top, text="Código QR:").pack()
    pdser = Label(top, text="Pode Ser PIX?").pack()
    bv = Label(top, text="Abra o aplicativo do seu banco e escaneie:").pack()
    ivalor = Label(top, text=f"Valor: {reais},{centavos}")
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
button.pack()

root.mainloop()