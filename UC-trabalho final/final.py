

import random
import string

# ================= ESTILO =================
def cor(texto, codigo):
    return f"\033[{codigo}m{texto}\033[0m"

def titulo(txt):
    print(cor("\n" + "="*40, "96"))
    print(cor(txt.center(40), "96"))
    print(cor("="*40, "96"))

def sucesso(txt):
    print(cor("✅ " + txt, "92"))

def erro(txt):
    print(cor("❌ " + txt, "91"))

def aviso(txt):
    print(cor("⚠️ " + txt, "93"))

# ================= GERADOR DE CÓDIGO =================
def gerar_codigo(tipo):
    letras = ''.join(random.choices(string.ascii_uppercase, k=3))
    numeros = ''.join(random.choices(string.digits, k=4))
    return f"{tipo}-{letras}{numeros}"

# ================= DADOS =================
pessoas_cadastradas = []

produtos_disponiveis = [
    "Arroz", "Feijão", "Óleo", "Açúcar", "Macarrão",
    "Café", "Leite", "Farinha", "Sal", "Biscoito",
    "Milho", "Ervilha", "Molho", "Aveia", "Fubá",
    "Sardinha", "Atum", "Achocolatado", "Macarrão instantâneo", "Canjica",
    "Sabonete", "Pasta de dente", "Papel higiênico", "Shampoo", "Detergente"
]

pontos_coleta = [
    "CRAS Centro",
    "Escola Municipal Esperança",
    "Igreja Solidária",
    "ONG Mãos Unidas",
    "Posto de Saúde Bairro Norte"
]
estoque = {

}

higiene = ["sabão", "condicionador"]

# ================= MENU =================
def menu():
    titulo("SISTEMA DE CESTA BÁSICA")
    print("1 - Cadastro")
    print("2 - Listar pessoas")
    print("3 - Selecionar produtos")
    print("4 - Pontos de coleta")
    print("5 - Doar")
    print("6 - Sair")

# ================= CADASTRO =================
def cadastrar():
    titulo("CADASTRO")

    nome = input("Nome: ").strip()

    while True:
        cpf = input("CPF (11 números): ").strip()
        if cpf.isdigit() and len(cpf) == 11:
            break
        erro("CPF inválido!")
    while True:
        telefone = input("Telefone (apenas números com DDD): ").strip()
        if telefone.isdigit() and len(telefone) in (10, 11):
         break
        erro("Telefone inválido! Use 10 ou 11 números com DDD.")
    

    try:
        moradores = int(input("Número de moradores na casa: "))
        renda = float(input("Renda total da familia: "))
        if moradores <= 0:
            raise ValueError
    except:
        erro("Dados inválidos!")
        return

    renda_familia = renda / moradores

    if  renda_familia >=800:
        status = "Doador"
        codigo = gerar_codigo("DOA")
    elif  renda_familia <= 800:
        status = "Recebe cesta básica"
        if renda_familia <= 109:
            status += " + Higiene"
            
        codigo = gerar_codigo("REC")
    else:
        status = "Não tem direito"
        codigo = None

    cadastro = {
        "nome": nome,
        "cpf": cpf,
        "telefone": telefone,
        "renda": renda,
        "moradores": moradores,
        "status": status,
        "cesta": [],
        "ponto_coleta": "Não definido",
        "codigo": codigo,
        "doacoes": []
    }

    pessoas_cadastradas.append(cadastro)

    sucesso(f"{nome} cadastrado!")
    print(cor(f"Status: {status}", "94"))

    if codigo:
        print(cor(f"Código: {codigo}", "96"))

# ================= LISTAR =================
def listar():
    titulo("LISTA")

    if not pessoas_cadastradas:
        aviso("Nenhum cadastro.")
        return

    for i, p in enumerate(pessoas_cadastradas, 1):
        print(cor(f"\n{i}. {p['nome']}", "95"))
        print(f"Status: {p['status']}")
        print(f"Renda: R$ {p['renda']}")
        print(f"Ponto: {p['ponto_coleta']}")
        print(f"Código: {p['codigo']}")

        print("Itens:")
        if p["cesta"]:
            for item in p["cesta"]:
                print(" -", item)
        else:
            print("Nenhum item")

# ================= PRODUTOS =================
def selecionar_produtos():
    titulo("SELEÇÃO DE PRODUTOS")

    if not pessoas_cadastradas:
        erro("Nenhuma pessoa cadastrada!")
        return

    listar()

    try:
        pessoa = pessoas_cadastradas[int(input("Escolha a pessoa: ")) - 1]
    except:
        erro("Escolha inválida!")
        return

    if "Recebe" not in pessoa["status"]:
        erro("Essa pessoa não tem direito!")
        return

    print("\n1 - Infantil\n2 - Emergencial\n3 - Nutricional")
    tipo = input("Tipo: ")
    
    if tipo == "1":
        obrigatorios = ["Leite", "Achocolatado", "Biscoito"]
        limite = 10

    elif tipo == "2":
        obrigatorios = ["Arroz", "Feijão", "Óleo"]
        limite = 8
    elif tipo == "3":
        obrigatorios = ["Arroz", "Feijão", "Aveia", "Leite"]
        limite = 7
    else:
        erro("Tipo inválido!")
        return

    cesta = obrigatorios.copy()

    extras = []
    while len(extras) < limite:
        for i, item in enumerate(produtos_disponiveis, 1):
            print(f"{i} - {item}")
        escolha = input("Escolha (0 sair): ")

        if escolha == "0":
            break

        if not escolha.isdigit():
            erro("Digite número!")
            continue

        item = produtos_disponiveis[int(escolha) - 1]

        if item in cesta or item in extras:
            aviso("Item repetido!")
        else:
            extras.append(item)
            sucesso(f"{item} adicionado")
    

    pessoa["cesta"] = cesta + extras

    sucesso("Cesta pronta!")

# ================= PONTO =================
def definir_ponto():
    titulo("PONTO DE COLETA")

    if not pessoas_cadastradas:
        erro("Nenhum cadastro!")
        return

    listar()

    try:
        pessoa = pessoas_cadastradas[int(input("Pessoa: ")) - 1]
    except:
        erro("Erro!")
        return

    for i, p in enumerate(pontos_coleta, 1):
        print(f"{i} - {p}")

    try:
        pessoa["ponto_coleta"] = pontos_coleta[int(input("Escolha: ")) - 1]
        sucesso("Ponto definido!")
    except:
        erro("Erro!")

# ================= DOAÇÃO =================
def doar():
    titulo("DOAÇÃO")

    if not pessoas_cadastradas:
        erro("Nenhum cadastro!")
        return

    listar()

    try:
        pessoa = pessoas_cadastradas[int(input("Pessoa: ")) - 1]
    except:
        erro("Erro!")
        return

    if pessoa["status"] != "Doador":
        erro("Não é doador!")
        return

    while True:
        for i, item in enumerate(produtos_disponiveis, 1):
            print(f"{i} - {item}")

        escolha = input("Item (0 sair): ")

        if escolha == "0":
            break

        if escolha.isdigit():
            item = produtos_disponiveis[int(escolha) - 1]
            pessoa["doacoes"].append(item)
            sucesso(f"{item} doado!")

    sucesso("Doação finalizada!")

# ================= LOOP =================
while True:
    menu()
    op = input("Escolha: ")

    if op == "1":
        cadastrar()
    elif op == "2":
        listar()
    elif op == "3":
        selecionar_produtos()
    elif op == "4":
        definir_ponto()
    elif op == "5":
        doar()
    elif op == "6":
        print("Saindo...")
        break
    else:
        erro("Opção inválida!")


