# Trabalho Final da Disciplina de Inteligencia Artificial


# SISTEMA ESPECIALISTA: Diagnóstico de Falhas em Computadores

#from IPython.display import clear_output                                # Somente necessário em ambiente Colab
import json
import random
import os

# Função para limpar a tela, diferente para Windows e Unix/Linux
def clear():
    #clear_output() # Somente necessário em ambiente Colab               # Somente necessário em ambiente Colab
    os.system("cls" if os.name == "nt" else "clear")
    print("Sistema Especialista - Diagnóstico de Falhas em Computadores")

# Persistência dos dados / Base de conhecimento
# Esta classe gerencia os arquivos de dados (base de conhecimento e histórico de feedback)

class Persistence:
    def __init__(self, kb_file='kb.json', history_file='history.json'):
        self.kb_file = kb_file         # Arquivo da base de conhecimento (KB)
        self.history_file = history_file # Arquivo do histórico de diagnósticos
        self.kb = {"symptoms": [], "solutions": [], "rules": []}  # Estrutura da base de conhecimento
        self.history = {}  # Histórico de feedback
        self.load_all()  # Carrega os dados existentes, se houver

    def load_all(self):
        # Se os arquivos não existirem, cria um padrão
        if not os.path.exists(self.kb_file):
            self._create_default_kb()
        if not os.path.exists(self.history_file):
            with open(self.history_file, 'w') as f:
                json.dump({}, f, indent=2)  # Cria o arquivo de histórico vazio

        # Carrega a base de conhecimento e o histórico dos arquivos JSON
        with open(self.kb_file, 'r') as f:
            self.kb = json.load(f)
        with open(self.history_file, 'r') as f:
            self.history = json.load(f)

    def save_all(self):
        # Salva os dados atualizados da base de conhecimento e histórico
        with open(self.kb_file, 'w') as f:
            json.dump(self.kb, f, indent=2, ensure_ascii=False)
        with open(self.history_file, 'w') as f:
            json.dump(self.history, f, indent=2, ensure_ascii=False)

    def _create_default_kb(self):
        # Cria a base de conhecimento padrão caso os arquivos não existam
        default_kb = {
            "symptoms": [
                {"id": 1,  "name": "computador não liga"},
                {"id": 2,  "name": "nenhum LED acende"},
                {"id": 3,  "name": "bipes na inicialização"},
                {"id": 4,  "name": "tela azul"},
                {"id": 5,  "name": "lentidão geral"},
                {"id": 6,  "name": "travamentos após alguns minutos"},
                {"id": 7,  "name": "reinicializações inesperadas"},
                {"id": 8,  "name": "cheiro de queimado"},
                {"id": 9,  "name": "superaquecimento"},
                {"id": 10, "name": "cooler fazendo muito ruído"},
                {"id": 11, "name": "sem imagem no monitor"},
                {"id": 12, "name": "HD fazendo ruído de clique"},
                {"id": 13, "name": "uso de CPU constantemente alto"},
                {"id": 14, "name": "uso de disco constantemente alto"},
                {"id": 15, "name": "tela congelando"},
                {"id": 16, "name": "programas abrindo muito lentamente"},
                {"id": 17, "name": "mensagens de erro de memória"},
                {"id": 18, "name": "drivers desatualizados"},
                {"id": 19, "name": "internet muito instável"},
                {"id": 20, "name": "periféricos não respondem"}
            ],

            "solutions": [
                {"id": 1,  "name": "verificar fonte de alimentação"},
                {"id": 2,  "name": "testar memória RAM"},
                {"id": 3,  "name": "reinstalar sistema operacional"},
                {"id": 4,  "name": "limpar ventoinhas e dissipadores"},
                {"id": 5,  "name": "trocar HD por SSD"},
                {"id": 6,  "name": "atualizar drivers"},
                {"id": 7,  "name": "verificar pasta térmica do processador"},
                {"id": 8,  "name": "substituir fonte de alimentação"},
                {"id": 9,  "name": "substituir cooler defeituoso"},
                {"id": 10, "name": "verificar placa-mãe para curto"},
                {"id": 11, "name": "reinstalar drivers de vídeo"},
                {"id": 12, "name": "rodar verificação de disco (CHKDSK)"},
                {"id": 13, "name": "escaneamento de malware"},
                {"id": 14, "name": "atualizar BIOS"},
                {"id": 15, "name": "resetar CMOS"},
                {"id": 16, "name": "trocar cabo de vídeo"},
                {"id": 17, "name": "reparar arquivos corrompidos (SFC/DISM)"},
                {"id": 18, "name": "resetar configurações de energia"},
                {"id": 19, "name": "verificar rede e roteador"},
                {"id": 20, "name": "verificar conexões internas"}
            ],

            "rules": [
                {"id": 1,  "symptoms": [1, 2],  "solution": 1},
                {"id": 2,  "symptoms": [3],     "solution": 2},
                {"id": 3,  "symptoms": [4],     "solution": 3},
                {"id": 4,  "symptoms": [5, 14], "solution": 5},
                {"id": 5,  "symptoms": [6, 9],  "solution": 7},
                {"id": 6,  "symptoms": [7],     "solution": 9},
                {"id": 7,  "symptoms": [8],     "solution": 10},
                {"id": 8,  "symptoms": [9, 10], "solution": 4}, 
                {"id": 9,  "symptoms": [10],    "solution": 9}, 
                {"id": 10, "symptoms": [11],    "solution": 11},
                {"id": 11, "symptoms": [12],    "solution": 12},
                {"id": 12, "symptoms": [13],    "solution": 13},
                {"id": 13, "symptoms": [14],    "solution": 6}, 
                {"id": 14, "symptoms": [15],    "solution": 17},
                {"id": 15, "symptoms": [16],    "solution": 5}, 
                {"id": 16, "symptoms": [17],    "solution": 2}, 
                {"id": 17, "symptoms": [18],    "solution": 6}, 
                {"id": 18, "symptoms": [19],    "solution": 19},
                {"id": 19, "symptoms": [20],    "solution": 20},
                {"id": 20, "symptoms": [5, 13], "solution": 3},
            ]
        }

        # Salva a base de conhecimento padrão no arquivo
        with open(self.kb_file, 'w') as f:
            json.dump(default_kb, f, indent=2, ensure_ascii=False)
        print("Base de conhecimento padrão criada.")

# Motor de Inferência
# O motor de inferência recebe os sintomas e aplica regras para sugerir soluções

class InferenceEngine:
    def __init__(self, kb, history):
        self.kb = kb  # A base de conhecimento
        self.history = history  # Histórico de feedbacks de soluções

    def match_solutions(self, user_symptoms):

        # Retorna soluções ordenadas por score baseadas nos sintomas do usuário.
        # A aderência (match) é calculada como uma média ponderada entre precisão e recall usando F1 score.
        # Além disso, o histórico de precisão (suavizado) é levado em consideração no cálculo do score final.
        # :param user_symptoms: Lista de IDs dos sintomas fornecidos pelo usuário.
        # :return: Lista de soluções possíveis, ordenadas por score.

        matched = []  # Lista para armazenar as soluções com seus scores e detalhes
        user_set = set(user_symptoms) if user_symptoms else set()  # Converte os sintomas do usuário para um conjunto para facilitar as comparações

        # Percorre todas as regras na base de conhecimento
        for rule in self.kb["rules"]:
            rule_set = set(rule.get("symptoms", []))  # Conjunto de sintomas associados à regra
            intersection = len(rule_set & user_set)  # Interseção entre os sintomas da regra e os sintomas fornecidos pelo usuário

            if not rule_set:
                # Se a regra não tem sintomas, seu match é 0
                match = 0.0
                precision_rule = 0.0
                recall_user = 0.0
            else:
                # Calcula a precisão da regra (quanto da regra foi coberta pelos sintomas fornecidos)
                precision_rule = intersection / len(rule_set)
                # Calcula o recall do usuário (quanto dos sintomas fornecidos foram cobertos pela regra)
                recall_user = intersection / len(user_set) if len(user_set) > 0 else 0.0

                # Se tanto precisão quanto recall forem zero, a aderência será zero
                if precision_rule + recall_user == 0:
                    match = 0.0
                else:
                    # F1 score (média harmônica entre precisão e recall)
                    match = 2 * (precision_rule * recall_user) / (precision_rule + recall_user)

            # Considera a precisão histórica (a "experiência" passada sobre a eficácia da regra)
            hist_precision = self._get_precision(rule["id"])
            # O score final é uma combinação do match (aderência) e a precisão histórica
            score = match * hist_precision

            # Encontra a solução associada à regra
            sol = self._find_solution(rule["solution"])
            # Adiciona a solução com seus detalhes ao resultado final
            matched.append({
                "rule_id": rule["id"],
                "solution": sol["name"],
                "score": round(score, 4),  # Score final, arredondado
                "precision": round(hist_precision, 3),  # Precisão histórica
                "match": round(match, 4),  # Aderência (F1 score)
                "rule_precision": round(precision_rule, 4),  # Precisão da regra
                "user_recall": round(recall_user, 4)  # Recall do usuário
            })

        # Remove soluções com score igual a 0 (sem aderência)
        matched = [m for m in matched if m["match"] > 0]

        # Ordena as soluções por score (do maior para o menor)
        matched.sort(key=lambda x: x["score"], reverse=True)

        return matched

    def _get_precision(self, rule_id):
        
        # Retorna a precisão histórica de uma regra, com suavização.
        # A precisão é calculada com base no número de sucessos e falhas, utilizando suavização Laplace.
        # :param rule_id: ID da regra para obter a precisão histórica.
        # :return: Precisão suavizada da regra.
        
        # Verifica se a regra já tem feedback no histórico
        if str(rule_id) not in self.history:
            return 0.5  # Se não houver histórico, assume precisão inicial de 50%
        
        data = self.history[str(rule_id)]  # Obtém os dados de feedback da regra
        total = data.get("success", 0) + data.get("fail", 0)  # Total de tentativas (sucessos + falhas)

        if total == 0:
            return 0.5  # Se não houver tentativas, retorna precisão inicial de 50%
        
        # Calcula a precisão suavizada (Laplace smoothing)
        return (data.get("success", 0) + 1) / (total + 2)  # +1 e +2 para evitar divisão por zero

    def _find_solution(self, sol_id):
        
        # Encontra a solução associada a um ID de solução.
        # :param sol_id: ID da solução a ser procurada.
        # :return: O nome da solução ou uma solução desconhecida.
        
        # Procura a solução na base de conhecimento pelo ID
        for s in self.kb["solutions"]:
            if s["id"] == sol_id:
                return s
        return {"name": "Solução desconhecida"}  # Se não encontrar a solução, retorna "desconhecida"

    def update_history(self, rule_id, success, penalty_factor=0.1):
        
        # Atualiza o histórico com o resultado de uma consulta.
        # Se a solução for bem-sucedida, incrementa o sucesso. Caso contrário, penaliza a falha.
        # :param rule_id: ID da regra para atualizar o histórico.
        # :param success: Booleano indicando se a solução foi bem-sucedida.
        # :param penalty_factor: Fator de penalização para falhas (por padrão 0.1).
        
        rid = str(rule_id)
        if rid not in self.history:
            self.history[rid] = {"success": 0, "fail": 0}  # Se não houver histórico, inicializa com zero sucesso e falha
        
        if success:
            # Incrementa o número de sucessos
            self.history[rid]["success"] = self.history[rid].get("success", 0) + 1
        else:
            # Incrementa o número de falhas, podendo aplicar uma penalização leve
            self.history[rid]["fail"] = self.history[rid].get("fail", 0) + penalty_factor

# Paginação para a UI
def paginate_list(items, page_size):
    
    # Função que divide uma lista de itens em várias páginas para navegação.
    # :param items: Lista de itens a serem paginados.
    # :param page_size: Quantidade de itens por página.
    # :return: O número total de páginas e uma função para acessar os itens de cada página.

    # Calcula o número total de páginas
    total_pages = max(1, (len(items) + page_size - 1) // page_size)

    # Função interna que retorna os itens de uma página específica
    def get_page(page):
        
        # Retorna os itens de uma página específica.
        # :param page: Número da página (1-indexed).
        # :return: Lista de itens da página solicitada.
        
        start = (page - 1) * page_size  # Calcula o índice inicial dos itens para a página
        end = start + page_size  # Calcula o índice final dos itens para a página
        return items[start:end]  # Retorna os itens entre os índices start e end

    return total_pages, get_page  # Retorna o número total de páginas e a função get_page para acessar cada página

# Interface do Usuario

class ConsoleUI:
    def __init__(self, persistence, engine):
        
        # Inicializa a interface de usuário com os componentes de persistência (para salvar/recuperar dados) e o motor de inferência (para calcular as soluções).
        # :param persistence: Objeto responsável pela persistência dos dados (base de conhecimento e histórico).
        # :param engine: Objeto do motor de inferência que irá calcular as soluções com base nos sintomas fornecidos.
        
        self.persistence = persistence
        self.engine = engine
    
    def run(self):
    
        #Método principal da interface de usuário. Exibe o menu, recebe a entrada do usuário e executa as ações apropriadas.
        
        while True:
            clear()  # Limpa a tela para exibir o menu
            print("\nMenu:")  # Exibe o menu principal
            print("1. Consultar diagnóstico")  # Opção para consultar diagnóstico
            print("2. Adicionar nova solução/regra/sintomas")  # Opção para adicionar nova solução, regra ou sintoma
            print("3. Sair")  # Opção para sair do sistema
            choice = input("Escolha uma opção: ")  # Recebe a escolha do usuário

            # Verifica qual opção o usuário escolheu
            if choice == "1":
                self.consult()  # Chama o método de consulta de diagnóstico
                self.persistence.save_all()  # Salva os dados após a consulta
            elif choice == "2":
                self.add_rule()  # Chama o método para adicionar nova solução, regra ou sintoma
                self.persistence.save_all()  # Salva os dados após adicionar nova regra
            elif choice == "3":
                self.persistence.save_all()  # Salva os dados antes de sair
                clear()  # Limpa a tela
                print("Dados salvos. Encerrando o sistema.")  # Exibe mensagem de encerramento
                break  # Encerra o loop e sai do programa
            else:
                print("Opção inválida.")  # Exibe mensagem de erro se a opção for inválida
    
    def consult(self):
        
        # Método responsável por realizar o diagnóstico com base nos sintomas fornecidos pelo usuário.
        # O usuário escolhe os sintomas, e o sistema sugere soluções baseadas nas regras da base de conhecimento.
        

        # PAGINAÇÃO DE SINTOMAS
        symptoms = self.persistence.kb["symptoms"]  # Obtém a lista de sintomas da base de conhecimento
        page_size = 30  # Define o número de sintomas exibidos por página
        page = 0  # Inicia a página na posição 0 (primeira página)
        total_pages = (len(symptoms) - 1) // page_size + 1  # Calcula o total de páginas necessárias para exibir todos os sintomas

        user_symptoms = []  # Lista para armazenar os sintomas escolhidos pelo usuário

        while True:
            clear()  # Limpa a tela antes de exibir a página de sintomas
            start = page * page_size  # Índice inicial dos sintomas a serem exibidos na página
            end = start + page_size  # Índice final dos sintomas a serem exibidos na página
            page_items = symptoms[start:end]  # Obtém os sintomas para a página atual

            # Exibe os sintomas disponíveis para o usuário
            print("\nSintomas disponíveis (p/ navegar: <  > / números para consultar / ENTER para sair):\n")
            for s in page_items:
                print(f"{s['id']} - {s['name']}")  # Exibe o ID e o nome do sintoma

            print(f"\nPágina {page+1}/{total_pages}")  # Exibe a página atual e o total de páginas

            choice = input("Comando: ").strip()  # Recebe o comando do usuário

            # ENTER -> encerrar
            if choice == "":
                return  # Se o usuário pressionar ENTER, encerra o método e volta ao menu

            # Navegação entre as páginas
            if choice == "<":
                if page > 0:
                    page -= 1  # Vai para a página anterior
                continue

            if choice == ">":
                if page < total_pages - 1:
                    page += 1  # Vai para a próxima página
                continue

            # Números -> executar consulta imediatamente
            if any(c.isdigit() for c in choice):  # Verifica se a entrada contém números
                try:
                    user_symptoms = [int(x.strip()) for x in choice.split(",") if x.strip().isdigit()]  # Converte os números em uma lista de IDs de sintomas
                    break  # Encerra o loop e segue para o processamento dos sintomas escolhidos
                except:
                    print("Entrada inválida.")  # Se a conversão falhar, exibe mensagem de erro
                    continue


        # APLICA AS REGRAS / MATCH
        matches = self.engine.match_solutions(user_symptoms)  # Chama o motor de inferência para obter as soluções para os sintomas fornecidos

        if not matches:
            clear()  # Limpa a tela
            print("\nNenhuma solução encontrada.")  # Se não houver soluções, exibe mensagem de erro
            input("Pressione ENTER para continuar.")  # Aguarda o usuário pressionar ENTER para voltar
            return

        
        # PAGINAÇÃO DE SOLUÇÕES
        sol_page_size = 10  # Define o número de soluções exibidas por página
        sol_page = 0  # Inicia a página de soluções na posição 0
        sol_total_pages = (len(matches) - 1) // sol_page_size + 1  # Calcula o total de páginas de soluções

        selected_solution = None  # Variável para armazenar a solução escolhida pelo usuário

        while selected_solution is None:
            clear()  # Limpa a tela antes de exibir as soluções
            start = sol_page * sol_page_size  # Índice inicial das soluções a serem exibidas na página
            end = start + sol_page_size  # Índice final das soluções a serem exibidas
            page_items = matches[start:end]  # Obtém as soluções para a página atual

            # Exibe as soluções sugeridas para o usuário
            print("\nSoluções sugeridas (p/ navegar: <  > / número para escolher / ENTER = nenhuma):\n")

            for i, m in enumerate(matches, 1):  # Itera sobre as soluções e exibe seus detalhes
                print(f"\n{i}. Solução: {m['solution']}")  # Exibe o número e o nome da solução
                print(f"   • Aderência (F1): {m['match']}")  # Exibe o score de aderência (F1)
                print(f"   • Cobertura da regra: cobre {m['rule_precision']*100:.1f}% dos sintomas da regra")  # Exibe a cobertura da regra
                print(f"   • Cobertura dos sintomas do usuário: cobre {m['user_recall']*100:.1f}% dos sintomas informados")  # Exibe a cobertura dos sintomas fornecidos pelo usuário
                print(f"   • Precisão histórica: {m['precision']*100:.1f}%")  # Exibe a precisão histórica da solução

            print(f"\nPágina {sol_page+1}/{sol_total_pages}")  # Exibe a página atual e o total de páginas

            choice = input("Comando: ").strip()  # Recebe o comando do usuário

            # ENTER = nenhuma solução
            if choice == "":
                break  # Se o usuário pressionar ENTER sem escolher nenhuma solução, encerra o método

            # Navegação entre as páginas
            if choice == "<":
                if sol_page > 0:
                    sol_page -= 1  # Vai para a página anterior
                continue

            if choice == ">":
                if sol_page < sol_total_pages - 1:
                    sol_page += 1  # Vai para a próxima página
                continue

            # Número -> escolher solução
            if choice.isdigit():  # Se a entrada for um número
                idx = int(choice)  # Converte a entrada para um número
                if 1 <= idx <= len(page_items):  # Se o número for válido, escolhe a solução correspondente
                    selected_solution = page_items[idx - 1]
                    break  # Encerra o loop e continua com o feedback da solução escolhida

                print("Índice inválido.")  # Se o número for inválido, exibe mensagem de erro
                continue


        # FEEDBACK E APRENDIZADO

        clear()  # Limpa a tela

        if selected_solution:
            # Se o usuário escolheu uma solução, aplica o feedback positivo
            self.engine.update_history(selected_solution["rule_id"], True)

            # Penaliza levemente as soluções não escolhidas
            for m in matches:
                if m["rule_id"] != selected_solution["rule_id"]:
                    self.engine.update_history(m["rule_id"], False, penalty_factor=0.1)

            print("\nFeedback registrado: solução escolhida recebeu reforço positivo.")  # Exibe mensagem de reforço positivo
            input("Pressione ENTER para continuar.")  # Aguarda o usuário pressionar ENTER para voltar
        else:
            # Se nenhuma solução foi escolhida, aplica penalização nas soluções sugeridas
            for m in matches:
                self.engine.update_history(m["rule_id"], False)

            print("\nFeedback registrado: nenhuma solução válida, penalização aplicada a todas.")  # Exibe mensagem de penalização
            input("Pressione ENTER para continuar.")  # Aguarda o usuário pressionar ENTER para voltar

        self.persistence.history = self.engine.history  # Atualiza o histórico de feedback
        self.persistence.save_all()  # Salva os dados após o feedback

    def add_rule(self):
        
        # Método responsável por adicionar novos sintomas, soluções e regras à base de conhecimento.
        # O usuário pode adicionar novos sintomas, associar sintomas existentes a uma nova regra, e fornecer uma nova solução para essa regra.
        
        print("\nAdicionar nova solução/regra/sintomas:")


        # Exibindo Sintomas Existentes
        print("\nSintomas existentes:")
        for s in self.persistence.kb["symptoms"]:
            print(f"{s['id']} - {s['name']}")  # Exibe os sintomas existentes com seus respectivos IDs

        add_new = input("\nDeseja adicionar novos sintomas? (s/n): ").lower()  # Pergunta se o usuário quer adicionar novos sintomas
        new_symptom_ids = []  # Lista para armazenar os IDs dos novos sintomas

        # Se o usuário deseja adicionar novos sintomas
        if add_new == "s":
            while True:
                # Solicita a descrição de um novo sintoma
                name = input("Descrição do novo sintoma (ou Enter para parar): ").strip()

                if not name:
                    break  # Se o usuário pressionar ENTER sem digitar nada, encerra o loop e não adiciona mais sintomas

                # Gera um novo ID para o sintoma
                new_id = max([s["id"] for s in self.persistence.kb["symptoms"]], default=0) + 1
                # Adiciona o novo sintoma à lista de sintomas
                self.persistence.kb["symptoms"].append({"id": new_id, "name": name})
                new_symptom_ids.append(new_id)  # Armazena o ID do novo sintoma
                print(f"Sintoma '{name}' adicionado com ID {new_id}")  # Exibe mensagem de sucesso

        
        # Selecionando Sintomas Existentes
        # Pergunta ao usuário os IDs dos sintomas para associar à nova regra
        print("Sintomas novos serão incluidos na regra automaticamente.")
        ids = input("IDs dos sintomas para associar à regra (ex: 1,2,3)(): ")
        symptom_ids = [int(x.strip()) for x in ids.split(",") if x.strip().isdigit()]  # Converte os IDs digitados em uma lista de números inteiros
        symptom_ids += new_symptom_ids  # Inclui os novos sintomas na lista

        
        # Adicionando Nova Solução
        solution_name = input("Descrição da nova solução: ")  # Solicita a descrição da nova solução
        new_sol_id = max([s["id"] for s in self.persistence.kb["solutions"]], default=0) + 1  # Gera um novo ID para a solução
        self.persistence.kb["solutions"].append({"id": new_sol_id, "name": solution_name})  # Adiciona a nova solução à lista de soluções

        
        # Criando Nova Regra
        new_rule_id = max([r["id"] for r in self.persistence.kb["rules"]], default=0) + 1  # Gera um novo ID para a regra
        # Adiciona a nova regra à lista de regras
        self.persistence.kb["rules"].append({
            "id": new_rule_id,  # ID da nova regra
            "symptoms": symptom_ids,  # Lista de sintomas associados à regra
            "solution": new_sol_id  # ID da solução associada à regra
        })

        print("Nova regra/solução/sintomas adicionados com sucesso!")  # Exibe mensagem de sucesso
        self.persistence.save_all()  # Salva os dados atualizados na persistência


def main():
    
    # Função principal que configura os componentes do sistema e inicia a execução do programa.
    # Ela cria as instâncias necessárias da persistência, motor de inferência e interface de usuário,
    # e chama o método 'run()' para iniciar a interação com o usuário.
    
    # Inicializa a persistência dos dados
    persistence = Persistence()  # Cria uma instância da classe Persistence para carregar os dados da base de conhecimento (kb.json) e histórico (history.json)

    # Inicializa o motor de inferência
    engine = InferenceEngine(persistence.kb, persistence.history)  # Cria uma instância da classe InferenceEngine com a base de conhecimento e histórico carregados

    # Inicializa a interface do usuário
    ui = ConsoleUI(persistence, engine)  # Cria uma instância da classe ConsoleUI, passando a persistência e o motor de inferência

    # Inicia a execução do sistema
    ui.run()  # Chama o método run da classe ConsoleUI, que entra no loop de interação com o usuário

# Se o script for executado diretamente (não importado como módulo), chama a função main()
if __name__ == "__main__":
    main()  # Chama a função main para iniciar o sistema
