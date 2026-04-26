# ✈️ Air Lesti — Sistema de Bilhetes de Avião

Um sistema de gestão de bilhetes de avião para o **Aeroporto de Faro**, com interface em consola e suporte a múltiplos perfis de utilizador.

---

## O que este programa faz

Permite gerir voos, passageiros e bilhetes diretamente pelo terminal. Consoante o perfil escolhido, tens acesso a diferentes funcionalidades:

| Perfil       | O que pode fazer                                              |
|--------------|---------------------------------------------------------------|
| **Admin**      | Ver voos, adicionar voos, ver histórico, ver passageiros por voo |
| **Balconista** | Tudo o que o Admin faz + vender e cancelar bilhetes           |
| **Cliente**    | Listar voos, comprar e cancelar bilhetes                      |

---

## Estrutura do Projeto

```
projeto/
│
├── main.py              # Ponto de entrada — arranca o programa
├── database.json        # Base de dados local (criada automaticamente)
│
└── src/
    ├── modelos.py       # Classes principais: Voo, Passageiro, Bilhete, Sistema
    ├── consola.py       # Interface visual do terminal (menus, cores, inputs)
    ├── voos.py          # Tabela fixa de rotas do Aeroporto de Faro
    ├── base_dados.py    # Leitura e escrita do ficheiro JSON
    ├── bilhetes.py      # (Reservado para lógica futura de bilhetes)
    └── __init__.py
```

---

## Como Instalar e Correr

### 1. Pré-requisitos
- Python 3.8 ou superior instalado

### 2. Instalar dependências
```bash
pip install colorama
```

### 3. Correr o programa
```bash
python main.py
```

---

## Rotas Disponíveis

O sistema tem **15 rotas pré-definidas** a partir de Faro, entre nacionais e internacionais:

- **Nacionais:** Lisboa, Porto, Funchal, Ponta Delgada
- **Internacionais:** Londres, Paris, Berlim, Madrid, Roma, Amesterdão, Barcelona, Zurique, Tunes, Casablanca, Praia

Podes também inserir uma rota manualmente ao escolher a opção **99** no menu de voos.

---

##  Como os dados são guardados

Todos os dados são guardados automaticamente no ficheiro `database.json` após cada operação. Da próxima vez que abrires o programa, o estado anterior é restaurado — voos, passageiros e bilhetes incluídos.

---

##  Exemplo de utilização

1. Corre `python main.py`
2. Escolhe o perfil **Balconista**
3. Adiciona um voo (ex: TP1902 para Lisboa)
4. Vende um bilhete a um passageiro
5. Cancela o bilhete se necessário
6. Sai pelo menu principal — os dados ficam guardados

---
