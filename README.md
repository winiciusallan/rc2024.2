# Projeto: Protocolo de Transferência de Arquivos Personalizado – FTCP

Este repositório contém a implementação do projeto **FTCP (File Transfer Custom Protocol)**, um sistema cliente-servidor para transferência de arquivos utilizando os protocolos TCP e UDP de forma customizada, conforme especificado nas instruções.

## Equipe

*   **Integrante 1:** Danielly Rayanne Macedo Lima
*   **Integrante 2:** Eliane Tamara Lima Oliveira
*   **Integrante 3:** Ronaldd Feliph Matias Costa
*   **Integrante 4:** Winicius Allan Bezerra Silva  

## Visão Geral do Projeto

O objetivo principal é desenvolver um cliente e um servidor que se comunicam através de um protocolo próprio (FTCP). A negociação inicial ocorre via UDP, onde o cliente requisita um arquivo (`a.txt` ou `b.txt`) e especifica o protocolo de transferência (obrigatoriamente TCP nesta versão). O servidor responde com a porta TCP designada para a transferência. Em seguida, o cliente estabelece uma conexão TCP nessa porta, solicita o arquivo, o recebe e confirma o recebimento antes de encerrar a conexão.

## Como Executar

1.  **Configuração:** Certifique-se de que o arquivo `config.ini` está presente na mesma pasta dos scripts e configurado corretamente com as portas desejadas e os caminhos para os arquivos `a.txt` e `b.txt`.
2.  **Iniciar o Servidor:**
    ```bash
    # Exemplo (adapte ao seu ambiente/linguagem)
    python server.py
    ```
3.  **Executar o Cliente (em outro terminal):**
    ```bash
    # Exemplo (adapte ao seu ambiente/linguagem)
    # Formato: python client.py <protocolo_desejado> <arquivo_solicitado>
    python client.py TCP a.txt
    ```
---
