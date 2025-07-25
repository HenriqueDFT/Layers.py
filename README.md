# 🧪 LAYER.PY

## ✨ Descrição

O **layer.py** é uma aplicação em Python desenvolvida para analisar estruturas moleculares ou cristalinas obtidas via **cálculos de DFT** (Teoria do Funcional da Densidade), a partir de arquivos no formato `.xyz`.

A ferramenta permite:

- Cálculo automático do **gap de energia (Eg)**;
- Determinação da **distância entre camadas**;
- Cálculo das **distâncias de ligações químicas**;
- Interface gráfica amigável desenvolvida com `Tkinter`;
- Exportação de **relatórios em PDF** com os resultados, incluindo **nome e dados do usuário**.

---

## 🧰 Tecnologias Utilizadas

- Python `>=3.8`
- Tkinter (interface gráfica)
- NumPy
- Matplotlib
- ReportLab (para gerar PDF)

---

## 📥 Instalação

Clone o repositório:


git clone https://github.com/SeuUsuario/layer.py.git
cd layer.py

Crie um ambiente virtual e instale as dependências:

python -m venv venv
source venv/bin/activate  # No Windows: venv\Scripts\activate
pip install -r requirements.txt

# ▶️ Como Usar

    Execute o programa:

#python3 layer.py

    Na interface gráfica, você poderá:

        Selecionar um arquivo .xyz;

        Com base no selecionado visualize o gap de energia e distâncias atômicas;

        Gerar relatório PDF com seu nome e dados personalizados.

# 📄 Exemplo de Relatório Gerado

O relatório inclui:

    Nome do usuário;

    Cargo;
     
    Orientador:

    Gap de energia calculado;

    Lista de distâncias entre átomos;

    Distância média entre camadas;

    Visualização da estrutura (opcional).

# 📸 Imagens da Interface

![](https://github.com/HenriqueDFT/Layers.py/blob/main/interface.png)

# 📁 Estrutura do Projeto

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

## 🧑‍💻 Autor

Desenvolvido por Henrique Lago, bacharel em Física pela Universidade Federal do Piauí (UFPI), membro do grupo de Nanofísica Computacional (GNC/UFPI), com experiência em simulações via DFT utilizando o pacote SIESTA.

GitHub: @HenriqueDFT
# 📜 Licença

Este projeto está licenciado sob a MIT License.
## ☕ Contribua

Contribuições são bem-vindas! Sinta-se à vontade para abrir issues, propor melhorias ou enviar pull requests.

## ⚛️ conheça o nosso grupo GNC

![](https://github.com/HenriqueDFT/Layers.py/blob/main/qr.png)

---

Se quiser que eu gere esse `README.md` como arquivo real, posso criar para você agora. Deseja?
```bash

