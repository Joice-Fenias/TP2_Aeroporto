# Air Lesti — Sistema de Gestão de Bilhetes de Avião
Sistema desenvolvido em *Python* para gestão de voos e bilhetes no *Aeroporto de Faro*, com interface em consola e suporte a múltiplos perfis de utilizador.

---

## Objetivo do Projeto
Este projeto simula um sistema real de gestão de bilhetes de avião, permitindo:

- Gestão de voos
- Registo de passageiros
- Venda e cancelamento de bilhetes
- Consulta de dados e histórico

Os dados são persistidos em ficheiro JSON, garantindo continuidade entre execuções.

---

## Funcionalidades
- Criar e listar voos  
- Registar passageiros  
- Vender bilhetes  
- Cancelar bilhetes  
- Consultar passageiros por voo  
- Visualizar histórico de transações  
- Guardar dados automaticamente  

---

## Perfis de Utilizador

| Perfil         | Permissões |
|---------------|-----------|
| *Admin*      | Criar voos, listar voos, ver histórico, ver passageiros |
| *Balconista* | Todas as do Admin + vender e cancelar bilhetes |
| *Cliente*    | Consultar voos, comprar e cancelar bilhetes |

---
## Estrutura do Projeto

```
TP2_AEROPORTO/
│
├── docs/
│   ├── _build/
│   │   ├── doctrees/
│   │   └── html/
│   ├── conf.py
│   ├── index.rst
│   ├── src.base_dados.rst
│   ├── src.consola.rst
│   ├── src.main.rst
│   ├── src.modelos.rst
│   ├── src.rst
│   └── src.voos.rst
│
├── src/
│   ├── __init__.py
│   ├── base_dados.py
│   ├── consola.py
│   ├── main.py
│   ├── modelos.py
│   └── voos.py
│
├── database.json
├── README.md
└── .gitignore
```

---

## Tecnologias Utilizadas
- Python 3.10+
- colorama (interface de consola)
- JSON (armazenamento de dados)
- Sphinx (documentação)

---

## Como Executar
## Instalar dependências 
pip install colorama

##  Executar o programa
python src/main.py

---
## Persistência de Dados
Os dados são guardados automaticamente em database.json
Estrutura base:
```
{
  "passageiros": [],
  "voos": [],
  "bilhetes": []
}
```
Os dados são carregados automaticamente ao iniciar o programa

---
## Rotas Disponíveis
O sistema inclui 15 rotas pré-definidas com origem em Faro:

- Nacionais: Lisboa, Porto, Funchal, Ponta Delgada
- Internacionais: Londres, Paris, Berlim, Madrid, Roma, Amesterdão, Barcelona, Zurique, Tunes, Casablanca, Praia

Também é possível adicionar voos manualmente.

---
## Funcionamento do Sistema
- O sistema carrega os dados do ficheiro JSON
- O utilizador escolhe um perfil
- Acede a um menu específico
- Executa operações
- Os dados são guardados automaticamente após cada ação

---
## Documentação
A documentação foi gerada com Sphinx e pode ser consultada em:

docs/_build/html/index.html
