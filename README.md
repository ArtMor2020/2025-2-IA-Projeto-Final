## Equipe

Este projeto foi desenvolvido por:
* Arthur Romanatto Moro - Desenvolvimento, modelagem do conhecimento e redação

---

# Sistema Especialista para Diagnóstico de Falhas em Computadores

* Repositório do Trabalho Final – Inteligencia Artificial - Unidades III e IV
* Este repositório contém o código-fonte, documentação, evidências e artefatos produzidos para o desenvolvimento de um Sistema Especialista baseado em regras de produção, conforme exigido no trabalho final da disciplina de Sistemas Inteligentes.
* O projeto segue o domínio de aplicação definido previamente no relatório de concepção e viabilidade e implementa um sistema especialista funcional para auxiliar a tomada de decisão no diagnóstico de falhas em computadores.

---

## Objetivo do Projeto

* Desenvolver um Sistema Especialista completo, capaz de:
* Representar conhecimento especializado por meio de fatos e regras de produção.
* Utilizar um motor de inferência (encadeamento para frente) para gerar conclusões.
* Permitir consultas, explicações e justificativas das inferências realizadas.
* Operar através de uma interface simples (texto).
* Cumprir todas as etapas do ciclo de desenvolvimento de sistemas especialistas.

---

## Funcionalidades Implementadas

* Base de conhecimento persistente (JSON)
* Fatos iniciais e fatos derivados
* Conjunto de regras (mínimo de 10 regras)
* Mecanismo de inferência (forward chaining)
* Interface textual interativa
* Sistema de navegação e seleção por sintomas
* Justificativas para cada decisão tomada
* Histórico de consultas e resultados
* Versões incrementais documentadas

---

## Tecnologias Utilizadas

* Linguagem:	Python 3.x
* Paradigma:	Forward Chaining (Encadeamento para Frente)
* Persistência:	Arquivos JSON
* Execução:	Google Colab / Ambiente local
* Repositório:	GitHub
* Ferramentas sugeridas pelo trabalho: PyKnow / Experta , mas optou-se por implementação manual, garantindo maior compreensão do motor de inferência.

---

## Estrutura do Repositório

```bash
├── project/
│   ├── engine.py              # Codigo Fonte
│   ├── kb.json                # Base de conhecimento
│   ├── history.json           # Registro de consultas
│
├── evidence/
│   ├── versions/              # Versões antigas
│
├── docs/
│   ├── artigo.pdf             # Artigo acadêmico completo
│
└── README.md                  # Este documento
```

---

## Como Executar

1. Clone o repositório
```bash
git clone https://github.com/ArtMor2020/2025-2-IA-Projeto-Final.git
cd .\2025-2-IA-Projeto-Final\project\
```

2. Execute o sistema
```bash
py engine.py
```

Nenhuma dependência externa é necessária além do Python padrão.

---

## Interface e Uso

A interface funciona via terminal e permite:

* Seleção de sintomas por número
* Navegação entre páginas via < e >
* Inferência automática de causas
* Apresentação de justificativas
* Sugestão de soluções

---

## Artigo Acadêmico

O PDF completo do artigo está disponível na pasta:

```bash
docs/artigo.pdf
```

O artigo aborda:

* Fundamentação teórica
* Representação do conhecimento
* Modelo de inferência
* Descrição da implementação
* Resultados e discussão
* Conclusão

---

## Evidências do Processo

Inclui:

* Versões anteriores

Localizado na pasta:

```bash
evidence/
```
---

## Demonstração da Aplicação

* link: https://colab.research.google.com/drive/1tqNJil0gIHWUJRzPSoDoflQWtW2C5JDz

