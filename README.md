# API Locadora de Veículos

## Descrição
Sistema de locadora de veículos com API REST e interface CLI. Migrado para utilizar MongoDB como banco de dados.

## Estrutura do Banco de Dados (MongoDB - Modelo de Documentos)
- **Tipo de Veículos**: `_id` (ObjectId), `modelo`, `tipo_combustivel`, `capacidade_passageiros`
- **Veículos**: `_id` (ObjectId), `placa`, `cor`, `marca`, `quilometragem`, `valor`, `ar_condicionado`, `id_tipo` (ObjectId - referência à coleção Tipo de Veículos), `ativo`
- **Clientes**: `_id` (ObjectId), `nome`, `cpf`, `endereco`, `cnh`, `dt_nasc`
- **Funcionários**: `_id` (ObjectId), `nome`, `cpf`, `cargo`, `endereco`, `salario`, `dt_nasc`, `ativo`
- **Reservas**: `_id` (ObjectId), `cod_cliente` (ObjectId - referência à coleção Clientes), `id_funcionario` (ObjectId - referência à coleção Funcionários), `placa_veiculo` (referência à coleção Veículos), `valor`, `dt_reserva` (ISO String), `dt_devolucao` (ISO String), `status`

## Funcionalidades
- Gestão de tipos de veículos
- Gestão de veículos (inclui listagem completa antes da remoção da frota)
- Gestão de clientes (com exibição otimizada da lista de clientes ao alterar endereço)
- Gestão de funcionários (apenas funcionários ativos são listados para promoção)
- Sistema de reservas por placa de veículo específica
- Interface CLI interativa
- Relatório: Listar veículos mais alugados
- Relatório: Faturamento por período
- Relatório: Clientes com mais reservas

## Set up

Para rodar a aplicação, siga os passos abaixo:

### 1. Instalação e Configuração do MongoDB

Certifique-se de ter o MongoDB instalado e em execução no seu sistema.

*   **Instalar MongoDB:**
    *   **Windows:** Baixe o instalador do MongoDB Community Server em [https://www.mongodb.com/try/download/community](https://www.mongodb.com/try/download/community). Siga as instruções do instalador. Recomenda-se instalar como um serviço.
    *   **macOS (via Homebrew):**
        ```bash
        brew tap mongodb/brew
        brew install mongodb-community@6.0 # Ou a versão mais recente
        ```
    *   **Linux (apt/Debian):** Siga as instruções específicas para a sua distribuição Linux no site oficial do MongoDB.

*   **Iniciar o Servidor MongoDB:**
    *   Se instalado como um serviço, ele deve iniciar automaticamente.
    *   **macOS (via Homebrew):**
        ```bash
        brew services start mongodb-community@6.0
        ```
    *   Verifique se o MongoDB está rodando (geralmente na porta `27017`).

### 2. Instalação das Dependências Python

1.  **Navegue até o diretório do projeto:**
    ```bash
    cd "C:\Users\gabri\Desktop\BAN II - TF PARTE 2\LocadoraVeiculos_Python-main"
    ```

2.  **Crie e ative um ambiente virtual (recomendado):**
    *   **Windows:**
        ```powershell
        python -m venv venv
        .\venv\Scripts\activate
        ```
    *   **macOS/Linux:**
        ```bash
        python3 -m venv venv
        source venv/bin/activate
        ```

3.  **Instale as dependências:**
    ```bash
    pip install -r requirements.txt
    ```

### 3. Popular o Banco de Dados MongoDB

1.  **Certifique-se de que o servidor MongoDB está em execução.**
2.  **No terminal (com o ambiente virtual ativado), execute o script de criação do MongoDB:**
    ```bash
    python db_scripts/creation_mongodb.py
    ```
    Você deverá ver a mensagem "Banco de dados MongoDB populado com sucesso!"

### 4. Rodar a API RESTful (Flask)

1.  **Abra um novo terminal** (ou use o terminal atual se a API rodará em segundo plano).
2.  **Navegue até o diretório do projeto e ative o ambiente virtual** (se estiver usando um novo terminal).
    *   **Windows:**
        ```powershell
        cd "C:\Users\gabri\Desktop\BAN II - TF PARTE 2\LocadoraVeiculos_Python-main"
        .\venv\Scripts\activate
        ```
    *   **macOS/Linux:**
        ```bash
        cd "C:\Users\gabri\Desktop\BAN II - TF PARTE 2\LocadoraVeiculos_Python-main"
        source venv/bin/activate
        ```
3.  **Execute o arquivo `app.py`:**
    ```bash
    python app.py
    ```
    A API será iniciada (geralmente em `http://127.0.0.1:8080/`). Mantenha este terminal aberto.

### 5. Rodar a Interface de Linha de Comando (CLI)

1.  **Abra outro terminal** (diferente do que está rodando a API).
2.  **Navegue até o diretório do projeto e ative o ambiente virtual.**
    *   **Windows:**
        ```powershell
        cd "C:\Users\gabri\Desktop\BAN II - TF PARTE 2\LocadoraVeiculos_Python-main"
        .\venv\Scripts\activate
        ```
    *   **macOS/Linux:**
        ```bash
        cd "C:\Users\gabri\Desktop\BAN II - TF PARTE 2\LocadoraVeiculos_Python-main"
        source venv/bin/activate
        ```
3.  **Execute o arquivo `main.py`:**
    ```bash
    python main.py
    ```
    O menu interativo da aplicação será exibido.

## Rotas da API
- `/get_all_tipo_veiculos` - Listar tipos de veículos (GET)
- `/cadastrar_tipo_veiculo` - Cadastrar tipo de veículo (POST)
- `/get_all_veiculos` - Listar veículos (GET)
- `/adicionar_veiculo` - Adicionar veículo (POST)
- `/tirar_veiculo_frota/<placa>` - Tirar veículo da frota (DELETE)
- `/get_all_clientes` - Listar clientes (GET)
- `/cadastrar_cliente` - Cadastrar cliente (POST)
- `/alterar_endereco_cliente/<cpf>` - Alterar endereço de cliente (PUT)
- `/get_all_funcionarios` - Listar funcionários (GET)
- `/cadastrar_funcionario` - Cadastrar funcionário (POST)
- `/promover_funcionario/<cpf>` - Promover funcionário (PUT)
- `/demitir_funcionario/<cpf>` - Demitir funcionário (DELETE)
- `/alterar_endereco_funcionario/<cpf>` - Alterar endereço de funcionário (PUT)
- `/fazer_reserva` - Fazer reserva (POST)
- `/get_all_reservas` - Listar todas as reservas (GET)
- `/get_reservas_by_cliente` - Listar reservas por cliente (POST)
- `/relatorio_veiculos_mais_alugados` - Listar veículos mais alugados (GET)
- `/relatorio_faturamento_por_periodo` - Listar faturamento por período (GET)
- `/relatorio_clientes_mais_reservas` - Listar clientes com mais reservas (GET)
- `/get_available_veiculos` - Listar veículos disponíveis para reserva (GET)
