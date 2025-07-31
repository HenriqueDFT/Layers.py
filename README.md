# 🧪 LAYER.PY

---

## ✨ Descrição

O **layer.py** é uma aplicação em Python desenvolvida para analisar estruturas moleculares ou cristalinas obtidas via **cálculos de DFT** (Teoria do Funcional da Densidade), a partir de arquivos no formato `.xyz`.

A ferramenta permite:

* Cálculo automático do **gap de energia (Eg)**;
* Determinação da **distância entre camadas**;
* Cálculo das **distâncias de ligações químicas**;
* Interface gráfica amigável desenvolvida com `Tkinter`;
* Exportação de **relatórios em PDF** com os resultados, incluindo **nome e dados do usuário**.

---

## 🧰 Tecnologias Utilizadas

* Python `>=3.8`
* Tkinter (interface gráfica)
* NumPy
* Matplotlib
* ReportLab (para gerar PDF)

---

## 📥 Instalação e Uso

Para começar a usar o Layer.py, siga estes passos simples:

1.  **Baixe o Projeto:**
    Baixe o arquivo `layers.zip` do repositório.

2.  **Extraia o Conteúdo:**
    Descompacte o arquivo `layers.zip` em uma pasta de sua preferência.

3.  **Instale as Dependências (se necessário):**
    Abra o terminal ou prompt de comando, navegue até a pasta onde você extraiu o projeto (a mesma onde está o arquivo `requirements.txt`) e execute o seguinte comando para instalar todas as bibliotecas necessárias:

    ```bash
    pip install -r requirements.txt
    ```
    *Dica: Se você tiver problemas com a versão do Python, pode tentar usar `pip3 install -r requirements.txt`.*

4.  **Execute o Programa:**
    Com as dependências instaladas, você já pode iniciar a aplicação. No mesmo terminal ou prompt de comando, execute:

    ```bash
    python3 layer.py
    ```

### ▶️ Como Usar na Interface Gráfica:

Ao abrir o programa, você poderá:

* **Selecionar arquivos** `.xyz` ou `.bands` para seus cálculos.
* **Visualizar** o gap de energia, distâncias atômicas e distâncias entre camadas.
* **Gerar um relatório PDF** com seus resultados, personalizando com seu nome e dados.

---

## 📄 Exemplo de Relatório Gerado

O relatório inclui:

* Nome do usuário;
* Cargo;
* Orientador;
* Gap de energia calculado;
* Lista de distâncias entre átomos;
* Distância média entre camadas;
* Visualização da estrutura (opcional).

---

## 📸 Imagens da Interface

![](https://github.com/HenriqueDFT/Layers.py/blob/main/interface.png)

---

## 📁 Estrutura do Projeto
```text

layer.py/
├── layer.py
├── analisador.py
├── pdf_exporter.py
├── ui/
│   └── interface.py
├── imagens/
│   └── interface.png
├── exemplos/
│   └── estrutura.xyz
├── README.md
└── requirements.txt
``` 

---

## 🧑‍💻 Autor

Desenvolvido por Henrique Lago, bacharel em Física pela Universidade Federal do Piauí (UFPI), membro do grupo de Nanofísica Computacional (GNC/UFPI), com experiência em simulações via DFT utilizando o pacote SIESTA.

GitHub: @HenriqueDFT

---

## 📜 Licença

Este projeto está licenciado sob a [MIT License](LICENSE).

---

## ☕ Contribua

Contribuições são bem-vindas! Sinta-se à vontade para abrir issues, propor melhorias ou enviar pull requests.

---

## ⚛️ Conheça o Nosso Grupo GNC

![](https://github.com/HenriqueDFT/Layers.py/blob/main/qr.png)
