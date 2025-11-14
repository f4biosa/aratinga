<h1 align="center">
    <picture>
        <source media="(prefers-color-scheme: light)" srcset=".github/aratinga.svg">
        <source media="(prefers-color-scheme: dark)" srcset=".github/aratinga-inverse.svg">
        <img width="343" src=".github/aratinga.svg" alt="Aratinga">
    </picture>
</h1>

# 🧪 Testes (Desenvolvimento do Pacote Aratinga)

Instruções para configurar o ambiente e rodar os testes do pacote `aratinga`.

### 1\. Configuração do Ambiente de Teste

Antes de rodar os testes pela primeira vez, o ambiente precisa ser preparado.

**1.1. Crie o Projeto "Hospedeiro"**
Os testes do `aratinga` rodam "contra" um projeto Django real. Este projeto deve ser "irmão" da pasta `aratinga`.

```bash
# 1. Navegue para a pasta que contém o repositório 'aratinga' (ex: C:\Repositorios\)
cd ..

# 2. Crie o projeto hospedeiro (ex: 'mysite')
aratinga start mysite

# 3. Volte para a pasta do Aratinga
cd aratinga
```

*(O nome `mysite` é apenas um exemplo. Pode ser qualquer nome de projeto válido, mas lembre-se dele para o próximo passo.)*

**1.2. Crie o `pytest.ini` no Hospedeiro**
O `pytest` precisa saber quais configurações do Django usar. Crie o arquivo `../mysite/pytest.ini` e cole o seguinte conteúdo:

```copy to clipboard
[pytest]
DJANGO_SETTINGS_MODULE = project_template.mysite.settings
python_paths = ../aratinga/src
django_find_project = false
```

*(**Importante:** Se você usou um nome diferente de `mysite` no passo 1.1, ajuste o `DJANGO_SETTINGS_MODULE` para `seunome.settings.dev`.)*

**1.3. Instale as Dependências de Teste**
Os testes requerem `pytest`, `pytest-django`, e `pytest-playwright`.

```bash
  # Estando na pasta 'aratinga/'
  uv pip install pytest pytest-django pytest-playwright
```

**1.4. Instale os Navegadores do Playwright**

```bash
  uv run playwright install
```

**1.5. Crie o Tema de Teste E2E**
O teste de upload (`test_theme_crud.py`) espera um arquivo ZIP com um nome específico (devido à regex no `forms.py`).

1.  Crie uma pasta simples (ex: `test_e2e`) com um `index.html` dentro.
2.  Comprima-a num arquivo chamado `aratinga-theme_test_e2e.zip`.
3.  Coloque este arquivo em `aratinga/src/aratinga/tests/endpoint_to_endpoint/`.

### 2\. Testes Unitários

Testes que verificam a lógica do app `aratinga` de forma isolada (ex: `test_theme.py`).

1.  **Configure o ambiente** (necessário no PowerShell):

    ```bash
    # Diga ao Python onde encontrar o projeto 'mysite' e o 'src' do aratinga
    $env:PYTHONPATH = "../mysite;src"
    ```

2.  **Rode os testes unitários:**

    ```bash
    # Usamos --ds para forçar o uso dos settings corretos
    uv run pytest src/aratinga/tests/test_theme.py --ds=mysite.settings.dev
    ```

### 3\. Testes Endpoint-to-Endpoint (E2E)

Testes que simulam cliques de usuário reais no site (login, upload, etc.) usando o Playwright.

1.  **Configure o ambiente** (necessário no PowerShell):

    ```powershell
    # 1. Configure o PYTHONPATH (igual aos testes unitários)
    $env:PYTHONPATH = "../mysite;src"

    # 2. Permita que o Django (Sync) rode com o Playwright (Async)
    $env:DJANGO_ALLOW_ASYNC_UNSAFE = "1"
    ```

2.  **Rode os testes E2E:**

    Execute para testar **sem** interface gráfica (navegador invisível 🙈):

    ```bash
    uv run pytest src/aratinga/tests/endpoint_to_endpoint/ --ds=mysite.settings.dev
    ```

    Execute para testar **com** interface gráfica (navegador visível 👀):

    ```bash
    uv run pytest src/aratinga/tests/endpoint_to_endpoint/ --ds=mysite.settings.dev --headed
    ```