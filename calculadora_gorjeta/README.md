# Calculadora de Gorjeta (Flask)

Projeto didático em **Python + Flask** para praticar:
- formulário HTML com método POST;
- validação no back-end;
- cálculo de gorjeta e divisão por pessoa;
- classificação por percentual;
- uso de Bootstrap com templates Jinja2.

---

## ✅ Pré-requisitos

- Windows com **PowerShell**
- Python 3.11+ instalado

> Para conferir se o Python está disponível no PowerShell:

```powershell
python --version
```

---

## 📁 1) Entrar na pasta do projeto

No PowerShell, vá até a raiz do repositório e depois para a pasta da aplicação:

```powershell
cd C:\caminho\para\Programa-o-para-Internet-ILP951
cd .\calculadora_gorjeta\
```

---

## 🐍 2) Criar o ambiente virtual (venv)

```powershell
python -m venv .venv
```

Esse comando cria a pasta `.venv` com um Python isolado para o projeto.

---

## ⚡ 3) Ativar o ambiente virtual no PowerShell

```powershell
.\.venv\Scripts\Activate.ps1
```

Se deu certo, o prompt ficará parecido com:

```text
(.venv) PS C:\...\calculadora_gorjeta>
```

### Se o PowerShell bloquear execução de script

Execute **uma vez**:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

Depois feche e abra o PowerShell novamente e rode o comando de ativação outra vez.

---

## 📦 4) Instalar as dependências (Flask)

Com o venv ativo:

```powershell
pip install -r .\requirements.txt
```

Se quiser instalar manualmente apenas o Flask:

```powershell
pip install Flask
```

---

## ▶️ 5) Rodar a aplicação

Ainda com o venv ativo, execute:

```powershell
python .\app.py
```

A aplicação ficará disponível em:

- http://127.0.0.1:5000

---

## 🧪 6) Como usar

1. Informe o **valor da conta**.
2. Informe a **quantidade de pessoas**.
3. Informe o **percentual de gorjeta**.
4. Clique em **Calcular**.
5. Veja os resultados:
   - valor da gorjeta;
   - total com gorjeta;
   - valor por pessoa;
   - classificação (*Mão de vaca*, *Legal* ou *Generoso*).

---

## 🛑 7) Desativar o venv quando terminar

```powershell
deactivate
```

---

## 📌 Observações

- O projeto usa `Decimal` para cálculos monetários com 2 casas decimais.
- A lógica de classificação é:
  - `< 5%` → **Mão de vaca**
  - `5% até 15%` → **Legal**
  - `> 15%` → **Generoso**
- O fluxo usa PRG (Post-Redirect-Get), evitando reenvio de formulário ao atualizar a página de resultado.
