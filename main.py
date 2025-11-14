import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import json, random

# ====== Carregar perguntas ======
with open("perguntas.json", "r", encoding="utf-8") as f:
    perguntas = json.load(f)["perguntas"]

random.shuffle(perguntas)

# ====== Variáveis globais ======
pontuacao = 0
indice = 0
tela_cheia = False
ajudas_usadas = {"50/50": False, "pular": False, "dica": False}
fundo_photo = None

# ====== Funções ======
def toggle_fullscreen(event=None):
    global tela_cheia
    tela_cheia = not tela_cheia
    root.attributes("-fullscreen", tela_cheia)

def sair_fullscreen(event=None):
    global tela_cheia
    tela_cheia = False
    root.attributes("-fullscreen", False)

def mostrar_pergunta():
    global indice
    if indice < len(perguntas):
        pergunta = perguntas[indice]
        pergunta_label.config(text=pergunta["enunciado"])
        for i, alt in enumerate(pergunta["alternativas"]):
            botoes[i].config(text=alt, state="normal", bg="#1e3a8a", fg="white")
    else:
        messagebox.showinfo("Fim do jogo", f"🎉 Parabéns! Você fez {pontuacao} pontos!")
        voltar_para_tela_inicial()

def verificar_resposta(opcao):
    global indice, pontuacao
    pergunta = perguntas[indice]
    correta = pergunta["resposta_correta"]

    for b in botoes:
        b.config(state="disabled")

    if opcao == correta:
        pontuacao += 100
        botoes[opcao].config(bg="#22c55e")  # Verde para acerto
        messagebox.showinfo("Correto!", f"✅ Resposta certa!\n\n{pergunta['explicacao']}")
    else:
        botoes[opcao].config(bg="#dc2626")  # Vermelho para erro
        botoes[correta].config(bg="#22c55e")  # Verde para resposta correta
        messagebox.showerror("Errado!", f"❌ Resposta errada.\n\n{pergunta['explicacao']}")

    indice += 1
    lbl_pontuacao.config(text=f"💰 Pontuação: {pontuacao}")
    root.after(500, mostrar_pergunta)

def ajuda_5050():
    if ajudas_usadas["50/50"]:
        messagebox.showinfo("Ajuda 50/50", "❗Você já usou essa ajuda.")
        return
    pergunta = perguntas[indice]
    correta = pergunta["resposta_correta"]
    erradas = [i for i in range(4) if i != correta]
    remover = random.sample(erradas, 2)
    for i in remover:
        botoes[i].config(state="disabled", text="", bg="#6b7280")
    ajudas_usadas["50/50"] = True
    btn_5050.config(state="disabled", bg="#6b7280")

def ajuda_pular():
    if ajudas_usadas["pular"]:
        messagebox.showinfo("Ajuda Pular", "❗Você já usou essa ajuda.")
        return
    messagebox.showinfo("Pular Pergunta", "🔁 Pergunta pulada sem perder pontos.")
    ajudas_usadas["pular"] = True
    btn_pular.config(state="disabled", bg="#6b7280")
    global indice
    indice += 1
    mostrar_pergunta()

def ajuda_dica():
    if ajudas_usadas["dica"]:
        messagebox.showinfo("Ajuda Dica", "❗Você já usou essa ajuda.")
        return
    pergunta = perguntas[indice]
    dica = pergunta.get("dica", "Sem dica disponível.")
    messagebox.showinfo("💡 Dica", dica)
    ajudas_usadas["dica"] = True
    btn_dica.config(state="disabled", bg="#6b7280")

def iniciar_jogo():
    global pontuacao, indice, ajudas_usadas
    pontuacao = 0
    indice = 0
    ajudas_usadas = {"50/50": False, "pular": False, "dica": False}
    lbl_pontuacao.config(text="💰 Pontuação: 0")
    
    # Resetar botões de ajuda
    btn_5050.config(state="normal", bg="#f59e0b")
    btn_pular.config(state="normal", bg="#f59e0b")
    btn_dica.config(state="normal", bg="#f59e0b")
    
    frame_tela_inicial.pack_forget()
    frame_jogo.pack(fill="both", expand=True)
    mostrar_pergunta()

def sair_jogo():
    root.destroy()

def voltar_para_tela_inicial():
    frame_jogo.pack_forget()
    frame_tela_inicial.pack(fill="both", expand=True)

# ====== Efeitos hover modernos ======
def hover_in_btn_resposta(event):
    if event.widget['state'] == 'normal':
        event.widget.config(bg="#3b82f6", fg="white")

def hover_out_btn_resposta(event):
    if event.widget['state'] == 'normal':
        event.widget.config(bg="#1e3a8a", fg="white")

def hover_in_btn_acao(event):
    if event.widget['state'] == 'normal':
        event.widget.config(bg="#fbbf24")

def hover_out_btn_acao(event):
    if event.widget['state'] == 'normal':
        event.widget.config(bg="#f59e0b")

def hover_in_btn_principal(event):
    event.widget.config(bg="#fbbf24")

def hover_out_btn_principal(event):
    event.widget.config(bg="#f59e0b")

# ====== Tkinter ======
root = tk.Tk()
root.title("💰 O Bilhão da Computação 💰")
root.geometry("1366x768")
root.configure(bg="#0f172a")
root.bind("<F11>", toggle_fullscreen)
root.bind("<Escape>", sair_fullscreen)

# ====== Fundo ======
try:
    fundo_original = Image.open("fundo.png").convert("RGBA")
except FileNotFoundError:
    # Criar um fundo azul escuro elegante se a imagem não existir
    fundo_original = Image.new('RGBA', (1366, 768), (15, 23, 42, 255))
    messagebox.showwarning("Aviso", "Imagem de fundo não encontrada. Usando fundo padrão.")

def redimensionar_fundo(event, lbl_bg):
    global fundo_photo
    largura, altura = event.width, event.height
    img = fundo_original.resize((largura, altura), Image.Resampling.LANCZOS)
    fundo_photo = ImageTk.PhotoImage(img)
    lbl_bg.config(image=fundo_photo)
    lbl_bg.image = fundo_photo

# ====== Tela inicial ======
frame_tela_inicial = tk.Frame(root, bg="#0f172a")
frame_tela_inicial.pack(fill="both", expand=True)

lbl_bg_inicio = tk.Label(frame_tela_inicial, bg="#0f172a")
lbl_bg_inicio.place(x=0, y=0, relwidth=1, relheight=1)
frame_tela_inicial.bind("<Configure>", lambda e: redimensionar_fundo(e, lbl_bg_inicio))

# Título principal com estilo de show
lbl_titulo_inicio = tk.Label(frame_tela_inicial, text="💰 O BILHÃO DA COMPUTAÇÃO 💰",
                             font=("Arial", 48, "bold"), fg="#fbbf24", bg="#0f172a")
lbl_titulo_inicio.pack(pady=80)

lbl_subtitulo = tk.Label(frame_tela_inicial, text="TESTE SEUS CONHECIMENTOS EM COMPUTAÇÃO",
                        font=("Arial", 20, "bold"), fg="#60a5fa", bg="#0f172a")
lbl_subtitulo.pack(pady=10)

# Botões com estilo dourado
btn_iniciar = tk.Button(frame_tela_inicial, text="🎯 INICIAR JOGO", width=25, height=2,
                        bg="#f59e0b", fg="#0f172a", font=("Arial", 18, "bold"),
                        command=iniciar_jogo, relief="raised", bd=4)
btn_iniciar.pack(pady=30)
btn_iniciar.bind("<Enter>", hover_in_btn_principal)
btn_iniciar.bind("<Leave>", hover_out_btn_principal)

btn_sair = tk.Button(frame_tela_inicial, text="🚪 SAIR", width=25, height=2,
                     bg="#f59e0b", fg="#0f172a", font=("Arial", 18, "bold"),
                     command=sair_jogo, relief="raised", bd=4)
btn_sair.pack()
btn_sair.bind("<Enter>", hover_in_btn_principal)
btn_sair.bind("<Leave>", hover_out_btn_principal)

# ====== Tela do jogo ======
frame_jogo = tk.Frame(root, bg="#0f172a")
lbl_bg_jogo = tk.Label(frame_jogo, bg="#0f172a")
lbl_bg_jogo.place(x=0, y=0, relwidth=1, relheight=1)
frame_jogo.bind("<Configure>", lambda e: redimensionar_fundo(e, lbl_bg_jogo))

# Cabeçalho do jogo
frame_cabecalho = tk.Frame(frame_jogo, bg="#1e3a8a", height=100)
frame_cabecalho.pack(fill="x", pady=(0, 20))
frame_cabecalho.pack_propagate(False)

lbl_titulo = tk.Label(frame_cabecalho, text="💰 O BILHÃO DA COMPUTAÇÃO 💰",
                      font=("Arial", 28, "bold"), fg="#fbbf24", bg="#1e3a8a")
lbl_titulo.pack(side="left", padx=20)

lbl_pontuacao = tk.Label(frame_cabecalho, text="💰 Pontuação: 0",
                         font=("Arial", 20, "bold"), fg="white", bg="#1e3a8a")
lbl_pontuacao.pack(side="right", padx=20)

# Área da pergunta
frame_pergunta = tk.Frame(frame_jogo, bg="#1e3a8a", relief="raised", bd=3)
frame_pergunta.pack(fill="x", padx=50, pady=20)

pergunta_label = tk.Label(frame_pergunta, text="", wraplength=1000, justify="center",
                          font=("Arial", 20, "bold"), fg="white", bg="#1e3a8a",
                          height=4)
pergunta_label.pack(padx=20, pady=15)

# ====== Botões de resposta ======
frame_respostas = tk.Frame(frame_jogo, bg="#0f172a")
frame_respostas.pack(fill="both", expand=True, padx=50)

botoes = []
cores_alternativas = ["#dc2626", "#2563eb", "#16a34a", "#9333ea"]  # Vermelho, Azul, Verde, Roxo

for i in range(4):
    frame_linha = tk.Frame(frame_respostas, bg="#0f172a")
    frame_linha.pack(fill="x", pady=8)
    
    btn = tk.Button(frame_linha, text="", width=80, height=2,
                    font=("Arial", 16, "bold"), bg=cores_alternativas[i], fg="white",
                    relief="raised", bd=3, command=lambda i=i: verificar_resposta(i))
    btn.pack(fill="x", padx=20)
    btn.bind("<Enter>", hover_in_btn_resposta)
    btn.bind("<Leave>", hover_out_btn_resposta)
    botoes.append(btn)

# ====== Ajudas ======
frame_ajudas = tk.Frame(frame_jogo, bg="#0f172a", height=80)
frame_ajudas.pack(fill="x", side="bottom", pady=10)
frame_ajudas.pack_propagate(False)

tk.Label(frame_ajudas, text="AJUDAS DISPONÍVEIS:", 
         font=("Arial", 14, "bold"), fg="#fbbf24", bg="#0f172a").pack(pady=5)

frame_botoes_ajuda = tk.Frame(frame_ajudas, bg="#0f172a")
frame_botoes_ajuda.pack()

btn_5050 = tk.Button(frame_botoes_ajuda, text="🎯 50/50", bg="#f59e0b", fg="#0f172a",
                     width=15, height=1, font=("Arial", 12, "bold"),
                     bd=3, relief="raised", command=ajuda_5050)
btn_5050.grid(row=0, column=0, padx=15)
btn_5050.bind("<Enter>", hover_in_btn_acao)
btn_5050.bind("<Leave>", hover_out_btn_acao)

btn_pular = tk.Button(frame_botoes_ajuda, text="⏭️ PULAR", bg="#f59e0b", fg="#0f172a",
                      width=15, height=1, font=("Arial", 12, "bold"),
                      bd=3, relief="raised", command=ajuda_pular)
btn_pular.grid(row=0, column=1, padx=15)
btn_pular.bind("<Enter>", hover_in_btn_acao)
btn_pular.bind("<Leave>", hover_out_btn_acao)

btn_dica = tk.Button(frame_botoes_ajuda, text="💡 DICA", bg="#f59e0b", fg="#0f172a",
                     width=15, height=1, font=("Arial", 12, "bold"),
                     bd=3, relief="raised", command=ajuda_dica)
btn_dica.grid(row=0, column=2, padx=15)
btn_dica.bind("<Enter>", hover_in_btn_acao)
btn_dica.bind("<Leave>", hover_out_btn_acao)

# ====== Iniciar ======
frame_tela_inicial.pack(fill="both", expand=True)
root.mainloop()