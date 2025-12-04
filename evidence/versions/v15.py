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
            "symptoms": [   # Fatos
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

            "rules": [      # Regras
                {"id": 1,  "symptoms": [1, 2],          "solution": 1},
                {"id": 2,  "symptoms": [1, 8],          "solution": 8},
                {"id": 3,  "symptoms": [3],             "solution": 2},
                {"id": 4,  "symptoms": [4, 17],         "solution": 2},
                {"id": 5,  "symptoms": [4, 13],         "solution": 17},
                {"id": 6,  "symptoms": [5, 14],         "solution": 5},
                {"id": 7,  "symptoms": [5, 16],         "solution": 3},
                {"id": 8,  "symptoms": [6, 9],          "solution": 7},
                {"id": 9,  "symptoms": [6, 10],         "solution": 4},
                {"id": 10, "symptoms": [7, 20],         "solution": 20},
                {"id": 11, "symptoms": [7, 13],         "solution": 18},
                {"id": 12, "symptoms": [8],             "solution": 10},
                {"id": 13, "symptoms": [9, 10],         "solution": 9},
                {"id": 14, "symptoms": [9],             "solution": 4},
                {"id": 15, "symptoms": [10],            "solution": 9},
                {"id": 16, "symptoms": [11],            "solution": 11},
                {"id": 17, "symptoms": [11, 16],        "solution": 16},
                {"id": 18, "symptoms": [12],            "solution": 12},
                {"id": 19, "symptoms": [12, 5],         "solution": 5},
                {"id": 20, "symptoms": [13],            "solution": 13},
                {"id": 21, "symptoms": [13, 18],        "solution": 6},
                {"id": 22, "symptoms": [14],            "solution": 12},
                {"id": 23, "symptoms": [15, 4],         "solution": 17},
                {"id": 24, "symptoms": [15, 6],         "solution": 7},
                {"id": 25, "symptoms": [16],            "solution": 5},
                {"id": 26, "symptoms": [17],            "solution": 2},
                {"id": 27, "symptoms": [18],            "solution": 6},
                {"id": 28, "symptoms": [19],            "solution": 19},
                {"id": 29, "symptoms": [20],            "solution": 20},
                {"id": 30, "symptoms": [15, 13, 14],    "solution": 3}
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
        user_set = set(user_symptoms) if user_symptoms else set()

        for rule in self.kb["rules"]:
            rule_set = set(rule.get("symptoms", []))
            intersection = len(rule_set & user_set)

            if not rule_set:
                # regra sem sintomas:ignorar ou tratar com aderência 0
                match = 0.0
                precision_rule = 0.0
                recall_user = 0.0
            else:
                precision_rule = intersection / len(rule_set)  # quanto da regra foi coberta
                recall_user = intersection / len(user_set) if len(user_set) > 0 else 0.0  # quanto dos sintomas do usuário estão cobertos

                if precision_rule + recall_user == 0:
                    match = 0.0
                else:
                    # F1 score
                    match = 2 * (precision_rule * recall_user) / (precision_rule + recall_user)

            # pegamos a precisão histórica e combinamos com o match
            hist_precision = self._get_precision(rule["id"])
            score = match * hist_precision

            sol = self._find_solution(rule["solution"])
            matched.append({
                "rule_id": rule["id"],
                "solution": sol["name"],
                "score": round(score, 4),
                "precision": round(hist_precision, 3),  # precisão histórica
                "match": round(match, 4),                # aderência (F1)
                "rule_precision": round(precision_rule, 4),
                "user_recall": round(recall_user, 4)
            })

        # remove regras sem aderência (match == 0)
        matched = [m for m in matched if m["match"] > 0]

        # ordenar pelo score final
        matched.sort(key=lambda x: x["score"], reverse=True)

        return matched

    def _get_precision(self, rule_id):
        if str(rule_id) not in self.history:
            return 0.5
        data = self.history[str(rule_id)]
        total = data.get("success", 0) + data.get("fail", 0)
        if total == 0:
            return 0.5
        return (data.get("success", 0) + 1) / (total + 2)  # suavização

    def _find_solution(self, sol_id):
        for s in self.kb["solutions"]:
            if s["id"] == sol_id:
                return s
        return {"name": "Solução desconhecida"}

    def update_history(self, rule_id, success, penalty_factor=0.1):
        """
        Atualiza histórico. penalty_factor permite penalizações leves (ex: 0.1).
        """
        rid = str(rule_id)
        if rid not in self.history:
            self.history[rid] = {"success": 0, "fail": 0}
        if success:
            self.history[rid]["success"] = self.history[rid].get("success", 0) + 1
        else:
            self.history[rid]["fail"] = self.history[rid].get("fail", 0) + penalty_factor


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
            print(f"\n{i}. Solução: {m['solution']}")
            print(f"   • Aderência (F1): {m['match']}")
            print(f"   • Cobertura da regra: cobre {m['rule_precision']*100:.1f}% dos sintomas da regra")
            print(f"   • Cobertura dos sintomas do usuário: cobre {m['user_recall']*100:.1f}% dos sintomas informados")
            print(f"   • Precisão histórica: {m['precision']*100:.1f}%")

        idx = input("\nQual dessas soluções funcionou? (número / Enter se nenhuma): ")         # Add next/previous page function to input field

        if idx.strip().isdigit():
            # Solução escolhida
            selected = matches[int(idx) - 1]

            # Reforço positivo
            self.engine.update_history(selected["rule_id"], True)

            # Penalização leve para as não escolhidas
            for m in matches:
                if m["rule_id"] != selected["rule_id"]:
                    self.engine.update_history(m["rule_id"], False, penalty_factor=0.1)

            print("Feedback registrado: sucesso para a solução escolhida e penalização leve para as demais.")

        else:
            # Todas foram ruins -> penalização normal
            for m in matches:
                self.engine.update_history(m["rule_id"], False)

            print("Feedback registrado: falha para todas as opções mostradas.")


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

# UI becomes cluttered over time due to output stacking
# UI linebreaks arent the best
# UI will become cluttered with large KBs, make paging function


# FIXED ---------------------------------------------

# KB saves more often
# Precision is now penalized for not chosen solutions
# Adherence is now fixed
# Conclusions now justified
# KB expanded