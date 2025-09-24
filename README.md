# API Locadora de Veículos

## Descrição
Sistema de locadora de veículos com API REST e interface CLI, baseado em modelo relacional.

## Estrutura do Banco de Dados
- **Tipo de Veículos**: Modelo, tipo de combustível, capacidade de passageiros
- **Veículos**: Placa, cor, marca, quilometragem, valor, ar condicionado, tipo (FK)
- **Clientes**: Código, nome, CPF, endereço, CNH, data nascimento
- **Funcionários**: ID, nome, CPF, cargo, endereço, salário, data nascimento, ativo
- **Reservas**: Código, cliente (FK), funcionário (FK), tipo de veículo (FK), valor, datas, status

## Funcionalidades
- Gestão de tipos de veículos
- Gestão de veículos
- Gestão de clientes
- Gestão de funcionários
- Sistema de reservas por tipo de veículo
- Interface CLI interativa

então execute ```python3 app.py``` para rodar o servidor localmente e ter acesso às rotas http no seu navegador no endereço ```http://127.0.0.1:8080```
depois disso, em outro terminal, execute o comando ```python3 main.py```

## Set up

### Linux
1. Instale o gerenciador de pacotes do Python (caso não tenha):
	```bash
	sudo apt install python3-pip
	```
2. Crie e ative o ambiente virtual:
	```bash
	python3 -m venv .venv
	source .venv/bin/activate
	```
3. Instale as dependências do projeto:
	```bash
	pip install -r requirements.txt
	```
4. Certifique-se de que a porta 8080 está livre:
	```bash
	lsof -i :8080
	```
	Se aparecer algum processo, mate-o:
	```bash
	sudo kill -9 <PID>
	```
5. Execute o servidor:
	```bash
	python3 app.py
	```
6. Em outro terminal (com o venv ativado), execute:
	```bash
	python3 main.py
	```

### Windows
1. Certifique-se de ter o Python instalado (https://www.python.org/downloads/).
2. Crie e ative o ambiente virtual:
	```powershell
	python -m venv .venv
	.\.venv\Scripts\Activate.ps1
	```
3. Instale as dependências do projeto:
	```powershell
	pip install -r requirements.txt
	```
4. Certifique-se de que a porta 8080 está livre:
	```powershell
	netstat -ano | findstr :8080
	```
	Se aparecer algum processo, mate-o:
	```powershell
	taskkill /PID <PID> /F
	```
5. Execute o servidor:
	```powershell
	python app.py
	```
6. Em outro terminal (com o venv ativado), execute:
	```powershell
	python main.py
	```

## Rotas da API
- `/get_all_tipo_veiculos` - Listar tipos de veículos
- `/cadastrar_tipo_veiculo` - Cadastrar tipo de veículo
- `/get_all_veiculos` - Listar veículos
- `/adicionar_veiculo` - Adicionar veículo
- `/get_all_clientes` - Listar clientes
- `/cadastrar_cliente` - Cadastrar cliente
- `/get_all_funcionarios` - Listar funcionários
- `/cadastrar_funcionario` - Cadastrar funcionário
- `/fazer_reserva` - Fazer reserva
- `/get_all_reservas` - Listar reservas
