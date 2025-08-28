# API Locadora de Veículos

# Set up
Primeiro, instale o packet manager do python com o comando
```bash
$ sudo apt install python3-pip
```
Depois instale as dependencias do projeto da seguinte forma
```bash
$ pip install -r requirements.txt
```
Após instalar as dependencias é necessário matar qualquer processo que esteja presente na porta 8080 do seu computador para poder rodar o servidor localmente
```bash
$ sudo lsof -i :8080
```
Caso após rodar o ```lsof -i :8080``` não listar nenhuma porta, signifca que nenhum processo está ocupando essa porta. 

Caso contrário, pegar o numero do processo e executar o comando abaixo com o número do processo. 
```bash
$ sudo kill -9 998244353
```
ou caso esteja em um ambiente windows
```bash
$ netstat -ano | findstr :8080
$ taskkill /PID 998244353 /F
```

então execute ```python3 app.py``` para rodar o servidor localmente e ter acesso às rotas http no seu navegador no endereço ```http://127.0.0.1:8080```
depois disso, em outro terminal, execute o comando ```python3 main.py```