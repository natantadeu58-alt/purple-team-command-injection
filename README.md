# 🛡️ Laboratório Prático de Purple Team: Mitigação de Command Injection

Este repositório contém um laboratório prático de segurança ofensiva e defensiva (**Purple Team**) focado na simulação e na neutralização de falhas de **Injeção de Comando (Command Injection)** em ambientes de API utilizando Python.

O objetivo do projeto é demonstrar como uma má sanitização ou concatenação de entradas do usuário em funções de sistema pode expor o servidor, e como mitigar o risco separando rigidamente comandos de argumentos.

---

## 🏗️ Estrutura do Projeto

- `app.py`: Servidor nativo baseado em HTTP que atua na camada de **Blue Team** (Defesa), recebendo requisições de teste e processando comandos de sistema de forma segura.
- `ataque.py`: Script automatizado de **Red Team** (Ataque) que simula o envio de payloads maliciosos tentando injetar operadores secundários (ex: `& whoami`) no campo de entrada.
- `requirements.txt`: Arquivo com a dependência utilizada pelo script de ataque.

---

## 🕹️ Cenário Prático

### 1. O Ataque (Red Team)
O script de ataque envia um payload estruturado para a rota de testes, emulando uma ação hacker. O objetivo é quebrar a lógica do comando original (um simples `ping`) e forçar a execução de um comando secundário indesejado:

```json
{
    "host": "8.8.8.8 & whoami"
}
```

### 2. A Vulnerabilidade (O erro do Desenvolvedor)
Se o servidor (Blue Team) estivesse configurado de forma insegura, ele concatenaria a string recebida diretamente no terminal do sistema operacional utilizando o argumento `shell=True`:

```python
# CÓDIGO VULNERÁVEL (Exemplo conceitual)
# O comando interpretado pelo sistema seria: ping -c 4 8.8.8.8 & whoami
comando = f"ping -c 4 {data['host']}"
subprocess.run(comando, shell=True)
```
Nesse cenário, o operador `&` faz o terminal executar o `ping` em segundo plano e rodar imediatamente o comando sequencial `whoami`, expondo o privilégio do usuário que roda a aplicação.

### 3. A Mitigação (Blue Team)
A correção aplicada neste laboratório neutraliza o ataque sem a necessidade de criar Expressões Regulares (Regex) complexas. A defesa consiste em duas regras fundamentais:
1. **Desativar o Shell (`shell=False`)**: Impede que o terminal interprete caracteres especiais como `&`, `|`, `;` ou `$()`.
2. **Passagem por Lista de Argumentos**: O comando e seus parâmetros são enviados como elementos estritamente separados em uma lista.

```python
# CÓDIGO SEGURO (Implementado no app.py)
# O sistema operacional entende que "8.8.8.8 & whoami" é uma única string de IP inválida, e não um comando.
comando = ["ping", "-c", "4", data['host']]
subprocess.run(comando, shell=False)
```

---

## 🚀 Como Executar o Laboratório

### Instalação
1. Clone o repositório e acesse a pasta do projeto.
2. Instale a biblioteca necessária para o script de ataque:
   ```bash
   pip install -r requirements.txt
   ```

### Passo 1: Iniciar o Servidor (Blue Team)
Execute a API de defesa. Ela ficará aguardando conexões na porta `8000`:
```bash
python app.py
```

### Passo 2: Executar o Ataque (Red Team)
Em outro terminal, execute o script de automação de ataque:
```bash
python ataque.py
```

### 📊 Resultado Esperado
Como o servidor implementa a mitigação segura, você verá que o comando injetado `whoami` **falhará**. O comando `ping` retornará um erro informando que o host `"8.8.8.8 & whoami"` é desconhecido ou inválido, provando que a injeção foi totalmente neutralizada.

Responsável:

Natan

Estudante de Engenharia de Software Futuro Especialista e Engenheiro de Segurança Cibernética.
