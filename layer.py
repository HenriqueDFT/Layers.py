import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PIL import Image, ImageTk # Para exibir imagens no Tkinter
from fpdf import FPDF # Para gerar o PDF
import os # Para manipulação de arquivos e caminhos
import numpy as np # Para cálculos numéricos eficientes, como sqrt

# --- Funções de Cálculo Traduzidas do Fortran para Python ---

def calculate_layer_distance_python(file_path):
    """
    Calcula a distância entre camadas a partir de um arquivo .xyz.
    Traduzido do programa Fortran 'distancia_layers'.
    Retorna (distancia_ang, distancia_bohr) ou códigos de erro.
    """
    ang_to_bohr = 1.8897259886 # Constante de conversão

    try:
        with open(file_path, 'r') as f:
            lines = f.readlines()
    except FileNotFoundError:
        # Erro ao abrir o arquivo, similar ao -999.99 do Fortran
        return -999.99, -999.99
    except Exception as e:
        # Outros erros de leitura
        print(f"Erro ao ler arquivo {file_path}: {e}")
        return -999.99, -999.99

    try:
        natoms = int(lines[0].strip())
    except (ValueError, IndexError):
        # Erro ao ler o número de átomos
        return -999.99, -999.99

    if natoms < 4:
        # Número insuficiente de átomos, similar ao -888.88 do Fortran
        return -888.88, -888.88

    z_coords = []
    # Começa a ler os dados dos átomos a partir da terceira linha (índice 2)
    for i in range(2, len(lines)):
        parts = lines[i].strip().split()
        if len(parts) >= 4: # Espera pelo menos tipo, x, y, z
            try:
                z_coords.append(float(parts[3])) # A coordenada Z é a quarta parte
            except ValueError:
                # Ignora linhas mal formatadas, mas pode indicar problema no arquivo
                continue
    
    if len(z_coords) != natoms:
        # Se o número de coordenadas lidas não corresponde ao natoms declarado
        return -999.99, -999.99

    # A lógica Fortran assume que os 2 primeiros são da camada inferior e os 2 últimos da superior.
    # Isso implica que os átomos estão ordenados por camada no arquivo .xyz.
    # Se o arquivo não estiver ordenado, essa lógica pode não ser precisa.
    z_bot_avg = (z_coords[0] + z_coords[1]) / 2.0
    z_top_avg = (z_coords[natoms-1] + z_coords[natoms-2]) / 2.0 # natoms-1 é o último, natoms-2 é o penúltimo

    distancia_ang = z_top_avg - z_bot_avg
    distancia_bohr = distancia_ang * ang_to_bohr

    return distancia_ang, distancia_bohr

def calculate_atom_distances_python(file_path):
    """
    Calcula distâncias entre pares de átomos a partir de um arquivo .xyz.
    Traduzido do programa Fortran 'calcula_distancias'.
    Retorna uma string formatada com os resultados ou uma mensagem de erro.
    """
    ang_to_bohr = 1.8897259886 # Constante de conversão

    try:
        with open(file_path, 'r') as f:
            lines = f.readlines()
    except FileNotFoundError:
        return f"Erro ao abrir o arquivo '{os.path.basename(file_path)}'."
    except Exception as e:
        return f"Erro ao ler arquivo {os.path.basename(file_path)}: {e}"

    try:
        num_atoms = int(lines[0].strip())
    except (ValueError, IndexError):
        return f"Erro: Não foi possível ler o número de átomos do arquivo '{os.path.basename(file_path)}'."

    if num_atoms < 2:
        return "Erro: Número insuficiente de átomos para calcular distâncias (mínimo de 2)."

    atoms_data = []
    # Começa a ler os dados dos átomos a partir da terceira linha (índice 2)
    for i in range(2, len(lines)):
        parts = lines[i].strip().split()
        if len(parts) >= 4: # Espera pelo menos tipo, x, y, z
            try:
                symbol = parts[0]
                x, y, z = float(parts[1]), float(parts[2]), float(parts[3])
                atoms_data.append({'symbol': symbol, 'x': x, 'y': y, 'z': z})
            except ValueError:
                # Ignorar linhas mal formatadas
                continue
    
    if len(atoms_data) != num_atoms:
        return f"Erro: O número de átomos lidos ({len(atoms_data)}) não corresponde ao declarado ({num_atoms})."

    results = ["Distâncias entre pares de átomos (Å e bohr):"]
    for i in range(num_atoms):
        for j in range(i + 1, num_atoms):
            atom1 = atoms_data[i]
            atom2 = atoms_data[j]

            dx = atom2['x'] - atom1['x']
            dy = atom2['y'] - atom1['y']
            dz = atom2['z'] - atom1['z']

            dist_ang = np.sqrt(dx*dx + dy*dy + dz*dz)
            dist_bohr = dist_ang * ang_to_bohr

            results.append(
                f"{i+1:3d} {atom1['symbol']:2s} - {j+1:3d} {atom2['symbol']:2s}: "
                f"{dist_ang:10.4f} Å    {dist_bohr:10.4f} bohr"
            )
    return "\n".join(results)

def calculate_band_gap_python(file_path):
    """
    Calcula o gap de energia a partir de um arquivo .bands.
    Traduzido do programa Fortran 'calcula_gap'.
    Retorna (gap_val, is_metallic) ou códigos de erro.
    """
    try:
        with open(file_path, 'r') as f:
            lines = f.readlines()
    except FileNotFoundError:
        # Erro ao abrir o arquivo, similar ao -999.99 do Fortran
        return -999.99, False
    except Exception as e:
        print(f"Erro ao ler arquivo {file_path}: {e}")
        return -999.99, False

    if not lines:
        return -888.88, False # Arquivo vazio

    try:
        fermi = float(lines[0].strip())
    except (ValueError, IndexError):
        # Erro ao ler o nível de Fermi, similar ao -888.88 do Fortran
        return -888.88, False

    # Leitura das energias
    energies = []
    for i in range(1, len(lines)): # Começa da segunda linha
        line_parts = lines[i].strip().split()
        if not line_parts: # Pula linhas vazias
            continue
        try:
            # Converte todos os valores da linha para float
            energies.extend([float(val) for val in line_parts])
        except ValueError:
            # Ignora linhas com dados não numéricos
            continue
    
    if not energies:
        # Se nenhuma energia foi lida
        return -777.77, False # Similar ao erro de limite excedido ou dados inválidos

    max_val = -float('inf') # Equivalente a um número muito pequeno
    min_cond = float('inf') # Equivalente a um número muito grande

    # Varre os valores para encontrar os extremos
    for energy in energies:
        if energy <= fermi and energy > max_val:
            max_val = energy
        elif energy > fermi and energy < min_cond:
            min_cond = energy

    gap = min_cond - max_val
    is_metallic = False

    if gap <= 0.0: # Material metálico se o gap for zero ou negativo
        is_metallic = True
        # No Fortran, ele imprime o Fermi para metálicos.
        # Aqui, retornamos o Fermi como 'gap_val' e is_metallic=True.
        return fermi, is_metallic
    else:
        return gap, is_metallic

# --- Classe para o Diálogo de Informações do Usuário ---
class UserInfoDialog(tk.Toplevel):
    def __init__(self, parent, initial_name="", initial_role="", initial_advisor=""):
        super().__init__(parent)
        self.title("Informações do Usuário para o Relatório")
        self.geometry("400x250")
        self.transient(parent) # Faz com que o diálogo fique acima da janela principal
        self.grab_set() # Bloqueia interação com a janela principal
        self.focus_set() # Define o foco para o diálogo
        self.configure(bg="#f0f0f0")

        self.user_name = initial_name
        self.user_role = initial_role
        self.user_advisor = initial_advisor
        self.result = None # Para armazenar o resultado (nome, cargo, orientador)

        self.create_widgets()

        # Configura o comportamento ao fechar a janela (botão X)
        self.protocol("WM_DELETE_WINDOW", self._on_closing)

    def create_widgets(self):
        frame = ttk.Frame(self, padding="15")
        frame.pack(expand=True, fill=tk.BOTH)

        # Nome
        ttk.Label(frame, text="Nome:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        self.entry_name = ttk.Entry(frame, width=40)
        self.entry_name.grid(row=0, column=1, padx=5, pady=5, sticky=tk.EW)
        self.entry_name.insert(0, self.user_name)

        # Cargo
        ttk.Label(frame, text="Cargo (ICB, ICV, Mestrando, Doutorando):").grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        self.entry_role = ttk.Entry(frame, width=40)
        self.entry_role.grid(row=1, column=1, padx=5, pady=5, sticky=tk.EW)
        self.entry_role.insert(0, self.user_role)

        # Orientador
        ttk.Label(frame, text="Orientador:").grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)
        self.entry_advisor = ttk.Entry(frame, width=40)
        self.entry_advisor.grid(row=2, column=1, padx=5, pady=5, sticky=tk.EW)
        self.entry_advisor.insert(0, self.user_advisor)

        # Botão de Confirmação
        ttk.Button(frame, text="Confirmar", command=self._on_confirm,
                   style='TButton').grid(row=3, column=0, columnspan=2, pady=15)
        
        # Estilo para os botões (copiado da classe principal para consistência)
        style = ttk.Style()
        style.configure('TButton', font=('Inter', 10, 'bold'),
                        foreground='white', background='#4CAF50',
                        padding=8, relief='raised', borderwidth=2,
                        focusthickness=3, focuscolor='none')
        style.map('TButton', background=[('active', '#45a049')])

    def _on_confirm(self):
        """
        Salva as informações e fecha o diálogo.
        """
        self.user_name = self.entry_name.get().strip()
        self.user_role = self.entry_role.get().strip()
        self.user_advisor = self.entry_advisor.get().strip()
        self.result = (self.user_name, self.user_role, self.user_advisor)
        self.destroy()

    def _on_closing(self):
        """
        Lida com o fechamento do diálogo pelo botão 'X'.
        Define o resultado como None para indicar cancelamento.
        """
        self.result = None
        self.destroy()

# --- Classe Principal do Aplicativo Tkinter ---

class NanophysicsApp(tk.Tk): # Renomeado de FortranApp para NanophysicsApp
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("Calculadora de Nanofísica Computacional")
        self.geometry("800x700")
        self.configure(bg="#f0f0f0") # Cor de fundo suave

        # Caminhos para suas imagens
        self.ufpi_logo_path = "ufpi.png"
        self.nanophysics_logo_path = "gnc(1).png"
        self.qrcode_path = "qr(1)(1).png"

        # Variáveis para armazenar as informações do usuário
        self.user_name = ""
        self.user_role = ""
        self.user_advisor = ""

        self.create_widgets()
        self.results = {
            "distancia_layers": "",
            "calcula_distancias": "",
            "calcula_gap": ""
        }

    def load_image_for_tkinter(self, image_path, size, is_logo=False):
        """
        Carrega uma imagem de um caminho de arquivo para uso no Tkinter.
        Se o arquivo não for encontrado, usa um placeholder.
        """
        try:
            img = Image.open(image_path)
            # Manter a proporção da imagem
            img.thumbnail(size, Image.LANCZOS)
            return ImageTk.PhotoImage(img)
        except FileNotFoundError:
            if is_logo:
                # Placeholder para logos se o arquivo não for encontrado
                placeholder_text = "UFPI Logo" if "ufpi" in image_path else "GNC Logo"
                # Cria uma imagem de placeholder em memória
                from PIL import ImageDraw, ImageFont
                img = Image.new('RGB', size, color='lightgray')
                d = ImageDraw.Draw(img)
                try:
                    # Tenta usar uma fonte padrão se disponível
                    font = ImageFont.truetype("arial.ttf", size[0] // 8)
                except IOError:
                    font = ImageFont.load_default()
                text_bbox = d.textbbox((0,0), placeholder_text, font=font)
                text_width = text_bbox[2] - text_bbox[0]
                text_height = text_bbox[3] - text_bbox[1]
                x_pos = (size[0] - text_width) / 2
                y_pos = (size[1] - text_height) / 2
                d.text((x_pos, y_pos), placeholder_text, fill="black", font=font)
                return ImageTk.PhotoImage(img)
            else:
                # Para o QR code, apenas retorna None e a função chamadora lida com isso
                return None
        except Exception as e:
            messagebox.showwarning("Erro de Imagem", f"Não foi possível carregar a imagem {image_path}: {e}")
            return None

    def create_widgets(self):
        # Frame do Cabeçalho
        header_frame = ttk.Frame(self, padding="10 10 10 10")
        header_frame.pack(fill=tk.X, pady=10)
        header_frame.configure(relief="raised", borderwidth=2)

        # Carregar e exibir logotipos
        # UFPI Logo (maior)
        self.ufpi_photo = self.load_image_for_tkinter(self.ufpi_logo_path, (120, 120), is_logo=True)
        if self.ufpi_photo:
            ufpi_label = tk.Label(header_frame, image=self.ufpi_photo)
            ufpi_label.pack(side=tk.LEFT, padx=10)
        else:
            tk.Label(header_frame, text="[UFPI Logo]", font=("Inter", 10)).pack(side=tk.LEFT, padx=10)

        # Título
        title_label = ttk.Label(header_frame, text="Ferramenta de Análise de Estruturas e Bandas",
                                 font=("Inter", 18, "bold"), foreground="#333333")
        title_label.pack(side=tk.LEFT, expand=True)

        # Nanophysics Logo (menor)
        self.nanophysics_photo = self.load_image_for_tkinter(self.nanophysics_logo_path, (70, 70), is_logo=True)
        if self.nanophysics_photo:
            nanophysics_label = tk.Label(header_frame, image=self.nanophysics_photo)
            nanophysics_label.pack(side=tk.RIGHT, padx=10)
        else:
            tk.Label(header_frame, text="[GNC Logo]", font=("Inter", 10)).pack(side=tk.RIGHT, padx=10)

        # Notebook para as abas (cálculos)
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(pady=10, padx=10, expand=True, fill=tk.BOTH)

        # Aba: Distância entre Camadas
        self.tab_dist_layers = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(self.tab_dist_layers, text="Distância entre Camadas")
        self.create_dist_layers_tab()

        # Aba: Distâncias entre Átomos
        self.tab_calc_dist = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(self.tab_calc_dist, text="Distâncias entre Átomos")
        self.create_calc_dist_tab()

        # Aba: Cálculo de Gap
        self.tab_calc_gap = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(self.tab_calc_gap, text="Cálculo de Gap")
        self.create_calc_gap_tab()

        # Frame para os botões de PDF e Sobre
        bottom_buttons_frame = ttk.Frame(self, padding="10 10 10 10")
        bottom_buttons_frame.pack(fill=tk.X, pady=10)
        
        ttk.Button(bottom_buttons_frame, text="Gerar Relatório PDF", command=self.generate_pdf,
                   style='TButton').pack(side=tk.LEFT, padx=5, expand=True)
        
        ttk.Button(bottom_buttons_frame, text="Sobre", command=self.show_about_info,
                   style='TButton').pack(side=tk.RIGHT, padx=5, expand=True)

        # Estilo para os botões
        style = ttk.Style()
        style.configure('TButton', font=('Inter', 10, 'bold'),
                        foreground='white', background='#4CAF50',
                        padding=8, relief='raised', borderwidth=2,
                        focusthickness=3, focuscolor='none')
        style.map('TButton', background=[('active', '#45a049')]) # Cor ao passar o mouse

        # Estilo para os Text widgets de resultado
        style.configure('TText', background='#e0e0e0', foreground='#333333',
                        font=('Inter', 10), padding=5)

    def create_dist_layers_tab(self):
        frame = ttk.LabelFrame(self.tab_dist_layers, text="Calcular Distância entre Camadas", padding="10")
        frame.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

        ttk.Label(frame, text="Arquivo .xyz:").pack(pady=5, anchor=tk.W)
        self.file_dist_layers_entry = ttk.Entry(frame, width=50)
        self.file_dist_layers_entry.pack(pady=5, fill=tk.X)
        ttk.Button(frame, text="Selecionar Arquivo", command=lambda: self.select_file(self.file_dist_layers_entry, ".xyz"),
                   style='TButton').pack(pady=5)

        ttk.Button(frame, text="Calcular Distância", command=self.run_dist_layers,
                   style='TButton').pack(pady=10)

        ttk.Label(frame, text="Resultados:").pack(pady=5, anchor=tk.W)
        self.result_dist_layers_text = tk.Text(frame, height=5, width=60, state='disabled', wrap=tk.WORD)
        self.result_dist_layers_text.pack(pady=5, fill=tk.BOTH, expand=True)
        self.result_dist_layers_text.configure(font=('Inter', 10), bg='#e0e0e0', fg='#333333', relief='flat')


    def create_calc_dist_tab(self):
        frame = ttk.LabelFrame(self.tab_calc_dist, text="Calcular Distâncias entre Átomos", padding="10")
        frame.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

        ttk.Label(frame, text="Arquivo .xyz:").pack(pady=5, anchor=tk.W)
        self.file_calc_dist_entry = ttk.Entry(frame, width=50)
        self.file_calc_dist_entry.pack(pady=5, fill=tk.X)
        ttk.Button(frame, text="Selecionar Arquivo", command=lambda: self.select_file(self.file_calc_dist_entry, ".xyz"),
                   style='TButton').pack(pady=5)

        ttk.Button(frame, text="Calcular Distâncias", command=self.run_calc_dist,
                   style='TButton').pack(pady=10)

        ttk.Label(frame, text="Resultados:").pack(pady=5, anchor=tk.W)
        self.result_calc_dist_text = tk.Text(frame, height=10, width=60, state='disabled', wrap=tk.WORD)
        self.result_calc_dist_text.pack(pady=5, fill=tk.BOTH, expand=True)
        self.result_calc_dist_text.configure(font=('Inter', 10), bg='#e0e0e0', fg='#333333', relief='flat')


    def create_calc_gap_tab(self):
        frame = ttk.LabelFrame(self.tab_calc_gap, text="Calcular Gap de Energia", padding="10")
        frame.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

        ttk.Label(frame, text="Arquivo .bands:").pack(pady=5, anchor=tk.W)
        self.file_calc_gap_entry = ttk.Entry(frame, width=50)
        self.file_calc_gap_entry.pack(pady=5, fill=tk.X)
        ttk.Button(frame, text="Selecionar Arquivo", command=lambda: self.select_file(self.file_calc_gap_entry, ".bands"),
                   style='TButton').pack(pady=5)

        ttk.Button(frame, text="Calcular Gap", command=self.run_calc_gap,
                   style='TButton').pack(pady=10)

        ttk.Label(frame, text="Resultados:").pack(pady=5, anchor=tk.W)
        self.result_calc_gap_text = tk.Text(frame, height=5, width=60, state='disabled', wrap=tk.WORD)
        self.result_calc_gap_text.pack(pady=5, fill=tk.BOTH, expand=True)
        self.result_calc_gap_text.configure(font=('Inter', 10), bg='#e0e0e0', fg='#333333', relief='flat')


    def select_file(self, entry_widget, file_extension):
        file_path = filedialog.askopenfilename(
            filetypes=[(f"Arquivos {file_extension}", f"*{file_extension}"), ("Todos os arquivos", "*.*")]
        )
        if file_path:
            entry_widget.delete(0, tk.END)
            entry_widget.insert(0, file_path)

    def update_text_widget(self, text_widget, content):
        text_widget.config(state='normal')
        text_widget.delete(1.0, tk.END)
        text_widget.insert(tk.END, content)
        text_widget.config(state='disabled')

    def run_dist_layers(self):
        file_path = self.file_dist_layers_entry.get()
        if not file_path:
            messagebox.showwarning("Entrada Inválida", "Por favor, selecione um arquivo .xyz.")
            return

        try:
            # Chama a função Python traduzida
            dist_ang, dist_bohr = calculate_layer_distance_python(file_path)

            if dist_ang == -999.99:
                result_str = f"Erro: Não foi possível abrir ou processar o arquivo '{os.path.basename(file_path)}'."
            elif dist_ang == -888.88:
                result_str = "Erro: Número insuficiente de átomos no arquivo para calcular a distância entre camadas (mínimo de 4)."
            else:
                result_str = (f"Distância entre camadas:\n"
                              f" - Em angstroms: {dist_ang:.4f} Å\n"
                              f" - Em bohr: {dist_bohr:.4f} bohr")

            self.update_text_widget(self.result_dist_layers_text, result_str)
            self.results["distancia_layers"] = result_str
        except Exception as e:
            messagebox.showerror("Erro de Execução", f"Ocorreu um erro ao executar o cálculo: {e}")
            self.update_text_widget(self.result_dist_layers_text, f"Erro: {e}")
            self.results["distancia_layers"] = f"Erro no cálculo de distância entre camadas: {e}"


    def run_calc_dist(self):
        file_path = self.file_calc_dist_entry.get()
        if not file_path:
            messagebox.showwarning("Entrada Inválida", "Por favor, selecione um arquivo .xyz.")
            return

        try:
            # Chama a função Python traduzida
            result_str = calculate_atom_distances_python(file_path)

            self.update_text_widget(self.result_calc_dist_text, result_str)
            self.results["calcula_distancias"] = result_str
        except Exception as e:
            messagebox.showerror("Erro de Execução", f"Ocorreu um erro ao executar o cálculo: {e}")
            self.update_text_widget(self.result_calc_dist_text, f"Erro: {e}")
            self.results["calcula_distancias"] = f"Erro no cálculo de distâncias entre átomos: {e}"


    def run_calc_gap(self):
        file_path = self.file_calc_gap_entry.get()
        if not file_path:
            messagebox.showwarning("Entrada Inválida", "Por favor, selecione um arquivo .bands.")
            return

        try:
            # Chama a função Python traduzida
            gap_val, is_metallic = calculate_band_gap_python(file_path)

            if gap_val == -999.99:
                result_str = f"Erro: Não foi possível abrir o arquivo '{os.path.basename(file_path)}'."
            elif gap_val == -888.88:
                result_str = "Erro: Não foi possível ler o nível de Fermi da primeira linha ou o arquivo está vazio."
            elif gap_val == -777.77:
                result_str = "Erro: Não foi possível ler dados de energia válidos no arquivo."
            elif is_metallic:
                # O Fortran imprime o nível de Fermi para metálicos, então mantemos a consistência
                result_str = f"Nível de Fermi lido: {gap_val:.4f} eV\nMaterial metálico (sem gap detectado)."
            else:
                result_str = (f"Gap de energia (eV): {gap_val:.4f}")

            self.update_text_widget(self.result_calc_gap_text, result_str)
            self.results["calcula_gap"] = result_str
        except Exception as e:
            messagebox.showerror("Erro de Execução", f"Ocorreu um erro ao executar o cálculo: {e}")
            self.update_text_widget(self.result_calc_gap_text, f"Erro: {e}")
            self.results["calcula_gap"] = f"Erro no cálculo de gap: {e}"

    def generate_pdf(self):
        # Cria uma instância do diálogo de informações do usuário
        dialog = UserInfoDialog(self, self.user_name, self.user_role, self.user_advisor)
        self.wait_window(dialog) # Espera o diálogo ser fechado

        # Verifica se o usuário confirmou (não fechou com o 'X')
        if dialog.result is not None:
            self.user_name, self.user_role, self.user_advisor = dialog.result
            # Permite a geração do PDF mesmo se os campos estiverem vazios
            self._perform_pdf_generation()
        else:
            messagebox.showinfo("Geração de PDF Cancelada", "A geração do relatório PDF foi cancelada pelo usuário.")


    def _perform_pdf_generation(self):
        """
        Contém a lógica real de geração do PDF, agora com as informações do usuário.
        """
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)

        # Adicionar logotipos ao PDF
        try:
            # Tenta adicionar o logo da UFPI
            if os.path.exists(self.ufpi_logo_path):
                pdf.image(self.ufpi_logo_path, x=10, y=10, w=30)
            else:
                pdf.text(10, 20, "[UFPI Logo Ausente]")
            
            # Tenta adicionar o logo do GNC
            if os.path.exists(self.nanophysics_logo_path):
                pdf.image(self.nanophysics_logo_path, x=170, y=10, w=20)
            else:
                pdf.text(170, 20, "[GNC Logo Ausente]")

        except Exception as e:
            messagebox.showwarning("Erro ao adicionar imagem ao PDF",
                                   f"Não foi possível adicionar os logotipos ao PDF. "
                                   f"Certifique-se de que os caminhos das imagens estão corretos. Erro: {e}")

        pdf.ln(20) # Pula algumas linhas para o conteúdo principal

        pdf.set_font("Arial", 'B', 16)
        pdf.cell(0, 10, "Relatório de Análise de Estruturas e Bandas", 0, 1, 'C')
        pdf.ln(5) # Espaço após o título

        # Adicionar informações do usuário (mesmo que vazias)
        pdf.set_font("Arial", size=10)
        pdf.cell(0, 7, f"Nome: {self.user_name if self.user_name else '[Não Informado]'}", 0, 1, 'C')
        pdf.cell(0, 7, f"Cargo: {self.user_role if self.user_role else '[Não Informado]'}", 0, 1, 'C')
        pdf.cell(0, 7, f"Orientador: {self.user_advisor if self.user_advisor else '[Não Informado]'}", 0, 1, 'C')
        pdf.ln(10) # Espaço após as informações do usuário

        pdf.set_font("Arial", 'B', 14)
        pdf.cell(0, 10, "1. Distância entre Camadas", 0, 1)
        pdf.set_font("Arial", size=12)
        if self.results["distancia_layers"]:
            pdf.multi_cell(0, 10, self.results["distancia_layers"])
        else:
            pdf.multi_cell(0, 10, "Nenhum cálculo de distância entre camadas foi realizado.")
        pdf.ln(5)

        pdf.set_font("Arial", 'B', 14)
        pdf.cell(0, 10, "2. Distâncias entre Pares de Átomos", 0, 1)
        pdf.set_font("Arial", size=12)
        if self.results["calcula_distancias"]:
            pdf.multi_cell(0, 10, self.results["calcula_distancias"])
        else:
            pdf.multi_cell(0, 10, "Nenhum cálculo de distâncias entre átomos foi realizado.")
        pdf.ln(5)

        pdf.set_font("Arial", 'B', 14)
        pdf.cell(0, 10, "3. Cálculo de Gap de Energia", 0, 1)
        pdf.set_font("Arial", size=12)
        if self.results["calcula_gap"]:
            pdf.multi_cell(0, 10, self.results["calcula_gap"])
        else:
            pdf.multi_cell(0, 10, "Nenhum cálculo de gap de energia foi realizado.")
        pdf.ln(5)

        try:
            file_name = filedialog.asksaveasfilename(defaultextension=".pdf",
                                                     filetypes=[("Arquivos PDF", "*.pdf")],
                                                     initialfile="relatorio_nanofisica.pdf")
            if file_name:
                pdf.output(file_name)
                messagebox.showinfo("PDF Gerado", f"Relatório PDF salvo com sucesso em:\n{file_name}")
        except Exception as e:
            messagebox.showerror("Erro ao Salvar PDF", f"Ocorreu um erro ao salvar o PDF: {e}")

    def show_about_info(self):
        about_window = tk.Toplevel(self)
        about_window.title("Sobre o Programa")
        about_window.geometry("600x600")
        about_window.configure(bg="#F0F0F0")

        about_font_text = ("Times New Roman", 10)
        about_font_email = ("Times New Roman", 10, "underline")

        text_content = """Este programa foi desenvolvido em Python com o objetivo de otimizar cálculos e gerar relatórios simples com dados restritos a sistemas 2D. Ele permite calcular diretamente o Gap de energia, a distância entre as camadas (layers), e os comprimentos de ligações químicas, tudo a partir de resultados de cálculos de Teoria do Funcional da Densidade (DFT).

O software foi criado por Henrique Lago, físico formado pela Universidade Federal do Piauí (UFPI), durante sua Iniciação Científica Voluntária, sob orientação do Professor Dr. Ramon Sampaio Ferreira. O desenvolvimento ocorreu no âmbito do Grupo de Nanofísica Computacional (GNC) da UFPI.

Conheça mais sobre o grupo escaneando o QR Code abaixo:
"""
        tk.Label(about_window, text=text_content, font=about_font_text, wraplength=550, justify=tk.LEFT, bg="#F0F0F0").pack(padx=20, pady=10)

        # Carregar e exibir QR Code
        self.qrcode_tk = self.load_image_for_tkinter(self.qrcode_path, (200, 200))
        if self.qrcode_tk:
            tk.Label(about_window, image=self.qrcode_tk, bg="#F0F0F0").pack(pady=5)
        else:
            tk.Label(about_window, text="[Arquivo qr(1)(1).png não encontrado]", font=about_font_text, fg="red", bg="#F0F0F0").pack(pady=5)
            messagebox.showwarning("QR Code Ausente", "O arquivo 'qr(1)(1).png' não foi encontrado na pasta do script.")

        tk.Label(about_window, text="e-mail: henrique.liberato@ufpi.edu.br", font=about_font_email, bg="#F0F0F0").pack(pady=10)

if __name__ == "__main__":
    app = NanophysicsApp()
    app.mainloop()
