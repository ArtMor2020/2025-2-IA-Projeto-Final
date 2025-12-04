# SISTEMA ESPECIALISTA: Diagnóstico de Falhas em Computadores

import json
import random
import os

# Persistência dos dados / Base de conhecimento

class Persistence:
    def __init__(self, kb_file='kb.json', history_file='history.json'):
        self.kb_file = kb_file
        self.history_file = history_file
        self.kb = {"symptoms": [], "solutions": [], "rules": []}
        self.history = {}
        self.load_all()

    def load_all(self):
        if not os.path.exists(self.kb_file):
            self._create_default_kb()
        if not os.path.exists(self.history_file):
            with open(self.history_file, 'w') as f:
                json.dump({}, f, indent=2)

        with open(self.kb_file, 'r') as f:
            self.kb = json.load(f)
        with open(self.history_file, 'r') as f:
            self.history = json.load(f)

    def save_all(self):
        with open(self.kb_file, 'w') as f:
            json.dump(self.kb, f, indent=2, ensure_ascii=False)
        with open(self.history_file, 'w') as f:
            json.dump(self.history, f, indent=2, ensure_ascii=False)

    def _create_default_kb(self):
        default_kb = {
            "symptoms": [       # Fatos
                {"id": 1,  "name": "computador não liga"},
                {"id": 2,  "name": "nenhum LED acende"},
                {"id": 3,  "name": "bipes na inicialização"},
                {"id": 4,  "name": "tela azul"},
                {"id": 5,  "name": "lentidão"}
            ],
            "solutions": [
                {"id": 1,  "name": "verificar fonte de alimentação"},
                {"id": 2,  "name": "testar memória RAM"},
                {"id": 3,  "name": "reinstalar sistema operacional"},
                {"id": 4,  "name": "limpar ventoinhas e dissipadores"},
                {"id": 5,  "name": "trocar HD por SSD"}
            ],
            "rules": [          # Regras
                {"id": 1,  "symptoms": [1, 2],  "solution": 1},
                {"id": 2,  "symptoms": [3],     "solution": 2},
                {"id": 3,  "symptoms": [4],     "solution": 3},
                {"id": 4,  "symptoms": [5],     "solution": 4},
                {"id": 5,  "symptoms": [5, 4],  "solution": 5}
            ]
        }
        with open(self.kb_file, 'w') as f:
            json.dump(default_kb, f, indent=2, ensure_ascii=False)
        print("Base de conhecimento padrão criada.")


# Motor de Inferência

class InferenceEngine:
    def __init__(self, kb, history):
        self.kb = kb
        self.history = history

    def match_solutions(self, user_symptoms):
        matched = []

        for rule in self.kb["rules"]:
            match_ratio = len(set(rule["symptoms"]) & set(user_symptoms)) / len(rule["symptoms"])
            if match_ratio > 0:
                precision = self._get_precision(rule["id"])
                score = match_ratio * precision
                sol = self._find_solution(rule["solution"])
                matched.append({
                    "rule_id": rule["id"],
                    "solution": sol["name"],
                    "score": round(score, 3),
                    "precision": round(precision, 2),
                    "match": round(match_ratio, 2)
                })

        matched.sort(key=lambda x: x["score"], reverse=True)
        return matched

    def _get_precision(self, rule_id):
        if str(rule_id) not in self.history:
            return 0.5
        data = self.history[str(rule_id)]
        total = data["success"] + data["fail"]
        if total == 0:
            return 0.5
        return (data["success"] + 1) / (total + 2)  # suavização

    def _find_solution(self, sol_id):
        for s in self.kb["solutions"]:
            if s["id"] == sol_id:
                return s
        return {"name": "Solução desconhecida"}

    def update_history(self, rule_id, success):
        rid = str(rule_id)
        if rid not in self.history:
            self.history[rid] = {"success": 0, "fail": 0}
        if success:
            self.history[rid]["success"] += 1
        else:
            self.history[rid]["fail"] += 1


# Interface do Usuario

class ConsoleUI:
    def __init__(self, persistence, engine):
        self.persistence = persistence
        self.engine = engine

    def run(self):
        print("Sistema Especialista - Diagnóstico de Falhas em Computadores")
        while True:
            print("\nMenu:")
            print("1. Consultar diagnóstico")
            print("2. Adicionar nova solução/regra/sintomas")
            print("3. Sair")
            choice = input("Escolha uma opção: ")

            if choice == "1":
                self.consult()
                self.persistence.save_all()
            elif choice == "2":
                self.add_rule()
                self.persistence.save_all()
            elif choice == "3":
                self.persistence.save_all()
                print("Dados salvos. Encerrando o sistema.")
                break
            else:
                print("Opção inválida.")

    def consult(self):
        print("\nSintomas disponíveis:")
        for s in self.persistence.kb["symptoms"]:
            print(f"{s['id']} - {s['name']}")
        ids = input("Digite os IDs dos sintomas separados por vírgula: ")                      # Add next/previous page function to input field
        user_symptoms = [int(x.strip()) for x in ids.split(",") if x.strip().isdigit()]

        matches = self.engine.match_solutions(user_symptoms)

        if not matches:
            print("Nenhuma solução encontrada.")
            return

        print("\nSoluções sugeridas:")
        for i, m in enumerate(matches, 1):
            print(f"{i}. {m['solution']} (Precisão: {m['precision']} | Aderência: {m['match']})")

        idx = input("\nQual dessas soluções funcionou? (número / Enter se nenhuma): ")         # Add next/previous page function to input field
        if idx.strip().isdigit():
            sel = matches[int(idx)-1]
            self.engine.update_history(sel["rule_id"], True)
            print("Feedback registrado como SUCESSO.")
        else:
            for m in matches:
                self.engine.update_history(m["rule_id"], False)
            print("Feedback registrado como FALHA para as opções mostradas.")

        self.persistence.history = self.engine.history
        self.persistence.save_all()

    def add_rule(self):
        print("\nAdicionar nova solução/regra/sintomas:")
        # Mostra sintomas existentes
        print("\nSintomas existentes:")
        for s in self.persistence.kb["symptoms"]:
            print(f"{s['id']} - {s['name']}")

        add_new = input("\nDeseja adicionar novos sintomas? (s/n): ").lower()    # Add next/previous page function to input field
        new_symptom_ids = []
        if add_new == "s":
            while True:
                name = input("Descrição do novo sintoma (ou Enter para parar): ").strip()  # Add check for duplicated sympthoms
                if not name:
                    break
                new_id = max([s["id"] for s in self.persistence.kb["symptoms"]], default=0) + 1
                self.persistence.kb["symptoms"].append({"id": new_id, "name": name})
                new_symptom_ids.append(new_id)
                print(f"Sintoma '{name}' adicionado com ID {new_id}")

        # Seleciona sintomas existentes ou recém-criados
        ids = input("IDs dos sintomas para associar à regra (ex: 1,2,3): ")              # New sympthoms are added automatically, make the output clearer
        symptom_ids = [int(x.strip()) for x in ids.split(",") if x.strip().isdigit()]
        symptom_ids += new_symptom_ids

        # Adiciona solução
        solution_name = input("Descrição da nova solução: ")
        new_sol_id = max([s["id"] for s in self.persistence.kb["solutions"]], default=0) + 1
        self.persistence.kb["solutions"].append({"id": new_sol_id, "name": solution_name})

        # Cria nova regra
        new_rule_id = max([r["id"] for r in self.persistence.kb["rules"]], default=0) + 1
        self.persistence.kb["rules"].append({
            "id": new_rule_id,
            "symptoms": symptom_ids,
            "solution": new_sol_id
        })

        print("Nova regra/solução/sintomas adicionados com sucesso!")
        self.persistence.save_all()


# Execução do projeto

def main():
    persistence = Persistence()
    engine = InferenceEngine(persistence.kb, persistence.history)
    ui = ConsoleUI(persistence, engine)
    ui.run()

if __name__ == "__main__":
    main()


# TO FIX ---------------------------------------------------------------------------------

# Not enough comments

# KB base seed too small
# "solutions" of KB too undetailed

# When selecting a solution as correct, other solutions arent penalized
# The aderence of a solution will be 1 if all the the problems of the solution are listed but there are remaining problems not to the solution
# Justify conclusions by the IE

# UI becomes cluttered over time due to output stacking
# UI linebreaks arent the best
# UI will become cluttered with large KBs, make paging function


# FIXED ---------------------------------------------

# KB saves more often