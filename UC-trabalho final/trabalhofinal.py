
salario_minimo = 1412 
pessoas = [] 

def menu():
    print("\n--- SISTEMA DE CESTA BÁSICA ---")
    print("1 - Cadastro de benefício")
    print("2 - Listar pessoas")
    print("3 - Sair")

def cadastrar():
    global pessoas 
    print("\n--- CADASTRO ---")
    
    nome = input("Nome: ").strip()
    
    while True:
        cpf = input("Digite seu CPF (apenas números): ").strip()
        if cpf.isdigit() and len(cpf) == 11:
            break
        print("CPF inválido! Digite exatamente 11 números.")

    numero = input("Digite seu número de telefone: ")
    
    try:
        qtd_pessoas = int(input("Quantas pessoas tem na sua casa: "))
        renda = float(input("Renda mensal total da casa (R$): "))
    except ValueError:
        print("Erro: Digite apenas números para quantidade e renda.")
        return

    
    status = "Recebe ajuda" if renda <= salario_minimo else "Pode doar"

    novo_cadastro = {
        "nome": nome,
        "cpf": cpf,
        "renda": renda,
        "status": status,
        "moradores": qtd_pessoas,
        "telefone": numero
    }

    pessoas.append(novo_cadastro)
    print(f"\n✅ {nome} cadastrado com sucesso! Situação: {status}")

def listar():
    print("\n--- LISTA DE PESSOAS ---")
    if not pessoas:
        print("Nenhuma pessoa cadastrada.")
        return

    for i, p in enumerate(pessoas, start=1):
        print(f"{i}. Nome: {p['nome']} | Status: {p['status']}")
        print(f"   Renda: R$ {p['renda']:.2f} | Moradores: {p['moradores']}")
        print("-" * 30)

def definir_cesta(renda_per_capita):
    global pessoas
    renda_per_capita = renda / pessoas
    
    
    LIMITE_POBREZA = 300.00

    produtos_basicos = ["Arroz", "Feijão", "Óleo", "Açúcar", "Macarrão"]
    produtos_higiene = ["Sabonete", "Creme Dental", "Papel Higiênico", "Shampoo"]

    print(f"\n--- Resultado da Avaliação ---")
    print(f"Renda por pessoa: R$ {renda_per_capita:.2f}")

    if renda_per_capita <= LIMITE_POBREZA:
        cesta_final = produtos_basicos + produtos_higiene
        print("Status: Direito a Cesta Completa (Alimentação + Higiene)")
    else:
        cesta_final = produtos_basicos
        print("Status: Direito a Cesta Básica Padrão")

    print("\nItens liberados:")
    for item in cesta_final:
        print(f"- {item}")

renda = float(input("Digite a renda total da família: "))
pessoas = int(input("Digite o número de pessoas na casa: "))

definir_cesta(renda, pessoas)











while True:
    menu()
    opcao = input("Escolha uma opção: ")

    if opcao == "1":
        cadastrar()
    elif opcao == "2":
        listar()
    elif opcao == "3":
        print("Encerrando sistema...")
        break
    else:
        print("Opção inválida.")
