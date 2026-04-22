import random
import string
import time  # para os timers

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

estoque_roupas = {
    "CRAS Centro": {"Camisa": 20, "Calça": 15, "Sapato": 10},
    "Escola Municipal Esperança": {"Camisa": 10, "Calça": 8, "Sapato": 5},
    "Igreja Solidária": {"Camisa": 12, "Calça": 10, "Sapato": 7},
    "ONG Mãos Unidas": {"Camisa": 18, "Calça": 12, "Sapato": 9},
    "Posto de Saúde Bairro Norte": {"Camisa": 14, "Calça": 11, "Sapato": 6}
}

# ================= MENU =================
def menu():
    titulo("==== SISTEMA DE CESTA BÁSICA ====")
    print("1 - Cadastro")
    print("2 - Listar pessoas")
    print("3 - Selecionar produtos")
    print("4 - Pontos de coleta")
    print("5 - Doar")
    print("6 - Ver estoque")
    print("7 - Doação/pedido de roupa")
    print("8 - Sair")

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

    while True:
        tem_crianca = input("Tem crianças na casa? (s/n): ").strip().lower()
        if tem_crianca in ["s", "n"]:
            break
        erro("Digite apenas 's' ou 'n'")

    if tem_crianca == "s":
        try:
            qtd_criancas = int(input("Quantas crianças? "))
            if qtd_criancas < 0 or qtd_criancas > moradores:
                raise ValueError
        except:
            erro("Quantidade inválida!")
            return
    else:
        qtd_criancas = 0

    renda_familia = renda / moradores

    if renda_familia >= 800:
        status = "Doador"
        codigo = gerar_codigo("DOA")
    elif renda_familia <= 800:
        status = "Recebe cesta básica"
        if renda_familia <= 300:
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
        "criancas": qtd_criancas,
        "status": status,
        "cesta": {},
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
        print(f"Renda: R$ {p['renda']:.2f}")
        print(f"Moradores: {p.get('moradores', 'Não informado')}")
        print(f"Crianças: {p.get('criancas', 0)}")
        print(f"Ponto: {p['ponto_coleta']}")
        
        print("Itens:")
        itens_mostrados = False
        
        if p["cesta"]:
            if isinstance(p["cesta"], list):
                for item in p["cesta"]:
                    print(" -", item)
            else:
                for item, qtd in p["cesta"].items():
                    print(f" - {item}: {qtd}")
            itens_mostrados = True
        
        if "Higiene" in p["status"]:
            print(" - Sabonete")
            print(" - Pasta de dente")
            print(" - Papel higiênico")
            print(" - Shampoo")
            print(" - Detergente")
            itens_mostrados = True
        
        if not itens_mostrados:
            print("Nenhum item")
        
        if p["doacoes"]:
            print("Roupas doadas/pedidas:")
            for d in p["doacoes"]:
                if "roupas" in d:
                    for roupa, qtd in d["roupas"].items():
                        print(f" - {roupa}: {qtd}")

# ================= ESTOQUE =================
estoque = {}

def inicializar_estoque():
    for ponto in pontos_coleta:
        estoque[ponto] = {}
        for produto in produtos_disponiveis:
            estoque[ponto][produto] = 50

inicializar_estoque()

# ================= PONTO DE COLETA =================
def definir_ponto():
    titulo("DEFINIR PONTO DE COLETA")
    
    if not pessoas_cadastradas:
        erro("Nenhuma pessoa cadastrada!")
        return
    
    listar()
    
    try:
        idx = int(input("Escolha a pessoa: ")) - 1
        if idx < 0 or idx >= len(pessoas_cadastradas):
            raise ValueError
        pessoa = pessoas_cadastradas[idx]
    except:
        erro("Escolha inválida!")
        return
    
    print("\nPontos de coleta disponíveis:")
    for i, ponto in enumerate(pontos_coleta, 1):
        print(f"{i} - {ponto}")
    
    try:
        idx_ponto = int(input("Escolha o ponto: ")) - 1
        if idx_ponto < 0 or idx_ponto >= len(pontos_coleta):
            raise ValueError
        ponto = pontos_coleta[idx_ponto]
        pessoa["ponto_coleta"] = ponto
        sucesso(f"Ponto de coleta definido: {ponto}")
    except:
        erro("Ponto inválido!")

# ================= VERIFICAR PONTO =================
def verificar_ponto(pessoa):
    if pessoa["ponto_coleta"] == "Não definido":
        erro(f"{pessoa['nome']} não tem ponto de coleta definido!")
        aviso("Por favor, defina o ponto de coleta primeiro (opção 4 do menu)")
        return False
    return True

# ================= PRODUTOS =================
def selecionar_produtos():
    titulo("SELEÇÃO DE PRODUTOS")

    if not pessoas_cadastradas:
        erro("Nenhuma pessoa cadastrada!")
        return

    listar()

    try:
        idx = int(input("Escolha a pessoa: ")) - 1
        if idx < 0 or idx >= len(pessoas_cadastradas):
            raise ValueError
        pessoa = pessoas_cadastradas[idx]
    except:
        erro("Escolha inválida!")
        return

    if "Recebe" not in pessoa["status"]:
        erro("Essa pessoa não tem direito a receber cesta básica!")
        return

    if not verificar_ponto(pessoa):
        return

    print("\n1 - Infantil\n2 - Emergencial\n3 - Nutricional")
    tipo = input("Tipo: ")

    if tipo == "1":
        obrigatorios = ["Leite", "Achocolatado", "Biscoito"]
        limite = 20
    elif tipo == "2":
        obrigatorios = ["Arroz", "Feijão", "Óleo"]
        limite = 18
    elif tipo == "3":
        obrigatorios = ["Arroz", "Feijão", "Aveia", "Leite"]
        limite = 15
    else:
        erro("Tipo inválido!")
        return

    if pessoa["criancas"] > 0:
        limite += 5
        aviso(f"{pessoa['nome']} tem crianças na casa, ganhou direito a +5 itens extras!")

    cesta = {item: 1 for item in obrigatorios}
    total_itens = len(obrigatorios)

    # Timer de 3 segundos antes de começar a escolha
    print("\nPreparando a seleção...")
    for i in range(3, 0, -1):
        print(f"{i}...", end=" ", flush=True)
        time.sleep(1)
    print("\n")

    while total_itens < limite:
        print(f"\n📦 Você pode escolher mais {limite - total_itens} itens:")
        print("0 - Finalizar seleção\n")
        
        opcoes = [p for p in produtos_disponiveis if p not in cesta]
        for i, item in enumerate(opcoes, 1):
            print(f"{i} - {item}")
        
        escolha = input("Escolha o item: ")

        if escolha == "0":
            break

        if not escolha.isdigit():
            erro("Digite número!")
            continue

        idx_item = int(escolha) - 1
        if idx_item < 0 or idx_item >= len(opcoes):
            erro("Opção inválida!")
            continue
            
        item = opcoes[idx_item]
        
        try:
            quantidade = int(input(f"Quantas unidades de {item} deseja adicionar? "))
            if quantidade <= 0:
                erro("Quantidade inválida! Use número maior que 0.")
                continue
            if total_itens + quantidade > limite:
                erro(f"Limite excedido! Você pode adicionar no máximo {limite - total_itens} itens.")
                continue
        except:
            erro("Digite um número válido!")
            continue

        cesta[item] = quantidade
        total_itens += quantidade
        sucesso(f"{quantidade} {item}(s) adicionados")

    pessoa["cesta"] = cesta
    ponto = pessoa["ponto_coleta"]

    print("\n" + "="*40)
    print("VERIFICANDO ESTOQUE...")
    print("="*40)
    
    estoque_ok = True
    for produto, qtd in cesta.items():
        if estoque[ponto][produto] >= qtd:
            sucesso(f"✅ {produto}: {qtd} disponível")
        else:
            erro(f"❌ {produto}: Estoque insuficiente! Disponível: {estoque[ponto][produto]}")
            estoque_ok = False
    
    if not estoque_ok:
        erro("Não foi possível completar a seleção devido à falta de estoque!")
        aviso("Sua cesta não foi registrada. Tente novamente com menos itens ou aguarde reposição.")
        pessoa["cesta"] = {}
        return
    
    print("\n" + "="*40)
    print("ATUALIZANDO ESTOQUE...")
    print("="*40)
    
    for produto, qtd in cesta.items():
        estoque[ponto][produto] -= qtd
        sucesso(f"📦 {qtd} {produto}(s) retirados do estoque de {ponto}")
    
    print("\n" + "="*40)
    sucesso("✅ CESTA REGISTRADA COM SUCESSO!")
    print("="*40)
    time.sleep(1.5)  # pequeno delay

# ================= DOAÇÃO =================
def doar():
    titulo("DOAÇÃO")

    if not pessoas_cadastradas:
        erro("Nenhum cadastro!")
        return

    listar()

    try:
        idx = int(input("Pessoa: ")) - 1
        if idx < 0 or idx >= len(pessoas_cadastradas):
            raise ValueError
        pessoa = pessoas_cadastradas[idx]
    except:
        erro("Erro!")
        return

    if pessoa["status"] != "Doador":
        erro("Essa pessoa não é doadora! Apenas doadores podem doar.")
        return

    cesta = {}

    while True:
        print("\n=== PRODUTOS DISPONÍVEIS PARA DOAÇÃO ===\n")
        print("0 - Finalizar doação\n")
        for i, produto in enumerate(produtos_disponiveis, 1):
            print(f"{i} - {produto}")

        try:
            opcao = int(input("Escolha o produto: "))
        except:
            erro("Digite um número válido!")
            continue

        if opcao == 0:
            break
        
        if opcao < 1 or opcao > len(produtos_disponiveis):
            erro("Opção inválida!")
            continue

        produto = produtos_disponiveis[opcao - 1]
        
        try:
            quantidade = int(input(f"Qual a quantidade de {produto} que você quer doar? "))
            if quantidade <= 0:
                erro("Quantidade deve ser maior que 0!")
                continue
        except:
            erro("Digite um número válido!")
            continue

        cesta[produto] = cesta.get(produto, 0) + quantidade
        sucesso(f"{quantidade} {produto}(s) adicionados à doação")

    if not cesta:
        aviso("Nenhum item doado!")
        return

    print("\nEscolha o ponto de coleta para doar:")
    for i, p in enumerate(pontos_coleta, 1):
        print(f"{i} - {p}")

    try:
        idx_ponto = int(input("Ponto: ")) - 1
        if idx_ponto < 0 or idx_ponto >= len(pontos_coleta):
            raise ValueError
        ponto = pontos_coleta[idx_ponto]
    except:
        erro("Ponto inválido!")
        return

    for item, qtd in cesta.items():
        estoque[ponto][item] += qtd

    pessoa["doacoes"].append({"ponto": ponto, "itens": cesta})

    print("\n=== RESUMO DA DOAÇÃO ===")
    for item, qtd in cesta.items():
        print(f"📦 {item}: {qtd}")

    sucesso(f"Doação registrada no ponto {ponto} e estoque atualizado!")
    time.sleep(1)  # pequeno delay

# ================= VER ESTOQUE =================
def ver_estoque():
    titulo("ESTOQUE DE PRODUTOS")

    for ponto, itens in estoque.items():
        print(cor(f"\n📍 {ponto}", "96"))
        print("-" * 30)
        for produto, qtd in itens.items():
            if qtd < 5:
                alerta = "⚠️ (ESTOQUE BAIXO)"
            elif qtd < 10:
                alerta = "⚠️"
            else:
                alerta = "✅"
            print(f"{produto:20} : {qtd:3} {alerta}")

# ================= DOAÇÃO DE ROUPAS =================
def doar_roupas():
    titulo("DOAÇÃO DE ROUPAS")

    if not pessoas_cadastradas:
        erro("Nenhum cadastro!")
        return

    listar()
    try:
        idx = int(input("Pessoa: ")) - 1
        if idx < 0 or idx >= len(pessoas_cadastradas):
            raise ValueError
        pessoa = pessoas_cadastradas[idx]
    except:
        erro("Erro!")
        return

    cesta = {}
    while True:
        print("\n=== ROUPAS DISPONÍVEIS PARA DOAR ===")
        print("0 - Finalizar doação")
        print("1 - Camisa")
        print("2 - Calça")
        print("3 - Sapato")

        try:
            opcao = int(input("Escolha a roupa: "))
        except:
            erro("Digite um número válido!")
            continue

        if opcao == 0:
            break

        match opcao:
            case 1: roupa = "Camisa"
            case 2: roupa = "Calça"
            case 3: roupa = "Sapato"
            case _:
                erro("Opção inválida!")
                continue

        try:
            quantidade = int(input(f"Quantidade de {roupa}: "))
            if quantidade <= 0:
                erro("Quantidade inválida!")
                continue
        except:
            erro("Digite um número válido!")
            continue

        cesta[roupa] = cesta.get(roupa, 0) + quantidade
        sucesso(f"{quantidade} {roupa}(s) adicionados à doação")

    if not cesta:
        aviso("Nenhuma roupa doada!")
        return

    print("\nEscolha o ponto de coleta para doar:")
    for i, p in enumerate(pontos_coleta, 1):
        print(f"{i} - {p}")

    try:
        idx_ponto = int(input("Ponto: ")) - 1
        if idx_ponto < 0 or idx_ponto >= len(pontos_coleta):
            raise ValueError
        ponto = pontos_coleta[idx_ponto]
    except:
        erro("Ponto inválido!")
        return

    for item, qtd in cesta.items():
        estoque_roupas[ponto][item] += qtd

    pessoa["doacoes"].append({"ponto": ponto, "roupas": cesta})
    sucesso(f"Doação de roupas registrada no ponto {ponto} e estoque atualizado!")
    time.sleep(1)

# ================= PEDIDO DE ROUPAS =================
def pedir_roupas():
    titulo("PEDIDO DE ROUPAS")

    if not pessoas_cadastradas:
        erro("Nenhum cadastro!")
        return

    listar()
    try:
        idx = int(input("Pessoa: ")) - 1
        if idx < 0 or idx >= len(pessoas_cadastradas):
            raise ValueError
        pessoa = pessoas_cadastradas[idx]
    except:
        erro("Erro!")
        return

    if not verificar_ponto(pessoa):
        return

    ponto = pessoa["ponto_coleta"]

    cesta = {}
    while True:
        print(f"\n=== ROUPAS DISPONÍVEIS EM {ponto} ===")
        print(f"Camisa: {estoque_roupas[ponto]['Camisa']}")
        print(f"Calça: {estoque_roupas[ponto]['Calça']}")
        print(f"Sapato: {estoque_roupas[ponto]['Sapato']}")
        print("\n0 - Finalizar pedido")
        print("1 - Camisa")
        print("2 - Calça")
        print("3 - Sapato")

        try:
            opcao = int(input("Escolha a roupa: "))
        except:
            erro("Digite um número válido!")
            continue

        if opcao == 0:
            break

        match opcao:
            case 1: roupa = "Camisa"
            case 2: roupa = "Calça"
            case 3: roupa = "Sapato"
            case _:
                erro("Opção inválida!")
                continue

        try:
            quantidade = int(input(f"Quantidade de {roupa}: "))
            if quantidade <= 0:
                erro("Quantidade inválida!")
                continue
        except:
            erro("Digite um número válido!")
            continue

        if estoque_roupas[ponto][roupa] >= quantidade:
            estoque_roupas[ponto][roupa] -= quantidade
            cesta[roupa] = cesta.get(roupa, 0) + quantidade
            sucesso(f"{quantidade} {roupa}(s) retirados do estoque")
        else:
            erro(f"Estoque insuficiente de {roupa}! Disponível: {estoque_roupas[ponto][roupa]}")

    if cesta:
        if isinstance(pessoa["cesta"], list):
            for item, qtd in cesta.items():
                pessoa["cesta"].append(f"{qtd} {item}")
        else:
            for item, qtd in cesta.items():
                pessoa["cesta"][item] = pessoa["cesta"].get(item, 0) + qtd
        sucesso("Pedido de roupas registrado!")
    else:
        aviso("Nenhum pedido realizado!")

# ================= TIMER DE SAÍDA =================
def timer_saida(segundos=5):
    print(cor("\n🔚 Encerrando o sistema", "96"))
    for i in range(segundos, 0, -1):
        print(f"  Saindo em {i} segundo{'s' if i > 1 else ''}...", end="\r")
        time.sleep(1)
    print("\n" + cor("✅ Sistema finalizado.", "92"))

# ================= LOOP PRINCIPAL =================
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
        ver_estoque()
    elif op == "7":
        print("\n1 - Doar roupas")
        print("2 - Pedir roupas")
        escolha = input("Escolha: ")
        if escolha == "1":
            doar_roupas()
        elif escolha == "2":
            pedir_roupas()
        else:
            erro("Opção inválida!")
    elif op == "8":
        timer_saida(5)
        break
    else:
        erro("Opção inválida!")
