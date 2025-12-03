import tkinter as tk
from tkinter import messagebox, filedialog
import os
import numpy as np
import importlib.util
import time


def criarTelaCap3(container, voltarTelaInicial):
    """Cria a interface do Capítulo 3 (Sistemas Lineares Ax=b)."""
    frame = tk.Frame(container)

    titulo = tk.Label(frame, text="Capítulo 03 - Sistemas Lineares Ax=b", font=("Arial", 14, "bold"))
    titulo.pack(pady=10)

    # Criar frame principal com dois painéis (entrada e resultados)
    main_container = tk.Frame(frame)
    main_container.pack(fill="both", expand=True, padx=10, pady=5)

    # Painel esquerdo (entrada de dados)
    left_panel = tk.Frame(main_container)
    left_panel.pack(side="left", fill="both", expand=False, padx=(0, 5))

    # 1. Tamanho
    tamanho_frame = tk.LabelFrame(left_panel, text="1. Definir Tamanho da Matriz", padx=10, pady=10)
    tamanho_frame.pack(fill="x", padx=10, pady=5)

    tk.Label(tamanho_frame, text="Ordem da matriz (n x n):").pack(side="left", padx=5)
    tamanho_var = tk.StringVar(value="3")
    tk.Spinbox(tamanho_frame, from_=1, to=20, textvariable=tamanho_var, width=5).pack(side="left", padx=5)
    status_label = tk.Label(tamanho_frame, text="Nenhuma matriz definida", fg="red", font=("Arial", 9))
    status_label.pack(side="left", padx=20)

    # 2. Entrada manual
    entrada_frame = tk.LabelFrame(left_panel, text="2. Inserir Valores da Matriz A e Vetor b", padx=10, pady=10)
    entrada_frame.pack(fill="both", expand=True, padx=10, pady=5)

    canvas = tk.Canvas(entrada_frame, height=200)
    scrollbar_canvas = tk.Scrollbar(entrada_frame, orient="vertical", command=canvas.yview)
    scrollable_frame = tk.Frame(canvas)

    scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar_canvas.set)
    canvas.pack(side="left", fill="both", expand=True)
    scrollbar_canvas.pack(side="right", fill="y")

    entrada_fields = {}

    def criar_campos_entrada():
        for w in scrollable_frame.winfo_children():
            w.destroy()
        entrada_fields.clear()

        try:
            n = int(tamanho_var.get())
            if n < 1 or n > 20:
                messagebox.showerror("Erro", "Ordem deve estar entre 1 e 20.")
                return
        except ValueError:
            messagebox.showerror("Erro", "Digite um número válido.")
            return

        matriz_title = tk.Label(scrollable_frame, text="Matriz A (nxn):", font=("Arial", 10, "bold"))
        matriz_title.pack(anchor="w", pady=(10, 5))

        for i in range(n):
            linha_frame = tk.Frame(scrollable_frame)
            linha_frame.pack(fill="x", pady=2)
            tk.Label(linha_frame, text=f"Linha {i+1}:", width=10).pack(side="left", padx=5)
            entrada_fields[f"A_{i}"] = []
            for j in range(n):
                e = tk.Entry(linha_frame, width=8, font=("Courier", 9))
                e.pack(side="left", padx=2)
                e.insert(0, "0")
                entrada_fields[f"A_{i}"].append(e)

        vetor_title = tk.Label(scrollable_frame, text="Vetor b (nx1):", font=("Arial", 10, "bold"))
        vetor_title.pack(anchor="w", pady=(15, 5))
        entrada_fields["b"] = []
        for i in range(n):
            linha_frame = tk.Frame(scrollable_frame)
            linha_frame.pack(fill="x", pady=2)
            tk.Label(linha_frame, text=f"b[{i+1}]:", width=10).pack(side="left", padx=5)
            e = tk.Entry(linha_frame, width=8, font=("Courier", 9))
            e.pack(side="left", padx=2)
            e.insert(0, "0")
            entrada_fields["b"].append(e)

        status_label.config(text=f"Matriz {n}x{n} criada", fg="blue")

    def preencher_exemplo():
        try:
            n = int(tamanho_var.get())
        except ValueError:
            messagebox.showerror("Erro", "Digite um número válido para tamanho.")
            return

        if not entrada_fields:
            messagebox.showinfo("Aviso", "Crie os campos primeiro (clique em 'Criar Campos').")
            return

        np.random.seed(42)
        A_ex = np.random.rand(n, n) * 2
        for i in range(n):
            A_ex[i, i] += n
        b_ex = np.random.rand(n) * 10

        for i in range(n):
            for j in range(n):
                entrada_fields[f"A_{i}"][j].delete(0, tk.END)
                entrada_fields[f"A_{i}"][j].insert(0, f"{A_ex[i,j]:.2f}")
        for i in range(n):
            entrada_fields["b"][i].delete(0, tk.END)
            entrada_fields["b"][i].insert(0, f"{b_ex[i]:.2f}")

        status_label.config(text="Exemplo carregado", fg="green")

    button_entrada_frame = tk.Frame(entrada_frame)
    button_entrada_frame.pack(fill="x", pady=10)
    tk.Button(button_entrada_frame, text="Criar Campos", command=criar_campos_entrada, width=15).pack(side="left", padx=5)
    tk.Button(button_entrada_frame, text="Preencher Exemplo", command=preencher_exemplo, width=15).pack(side="left", padx=5)

    # 2c. Arquivo
    arquivo_frame = tk.LabelFrame(left_panel, text="2c. Carregar de Arquivo (Alternativa)", padx=10, pady=10)
    arquivo_frame.pack(fill="x", padx=10, pady=5)
    arquivo_status = tk.Label(arquivo_frame, text="Nenhum arquivo carregado", fg="red", font=("Arial", 9))
    arquivo_status.pack(anchor="w", pady=5)

    def carregar_arquivo_estendido():
        filepath = filedialog.askopenfilename(title="Selecionar arquivo (matriz aumentada [A|b])",
                                              filetypes=[("Texto", "*.txt"), ("Todos", "*.*")])
        if not filepath:
            return
        try:
            dados = np.loadtxt(filepath)
            if dados.ndim != 2:
                messagebox.showerror("Erro", "Arquivo deve conter dados 2D.")
                return
            frame._matriz_A = dados[:, :-1].astype(float)
            frame._vetor_b = dados[:, -1].astype(float)
            if frame._matriz_A.shape[0] != frame._matriz_A.shape[1]:
                messagebox.showerror("Erro", "Matriz A deve ser quadrada.")
                del frame._matriz_A
                del frame._vetor_b
                return
            n = frame._matriz_A.shape[0]
            arquivo_status.config(text=f"✓ Arquivo carregado: {n}x{n} [A|b]\n{os.path.basename(filepath)}", fg="green")
            status_label.config(text=f"Arquivo carregado: {n}x{n}", fg="green")
        except Exception as e:
            messagebox.showerror("Erro ao carregar", str(e))

    def carregar_arquivo_separado():
        filepath_A = filedialog.askopenfilename(title="Selecionar arquivo da matriz A",
                                                filetypes=[("Texto", "*.txt"), ("Todos", "*.*")])
        if not filepath_A:
            return
        filepath_b = filedialog.askopenfilename(title="Selecionar arquivo do vetor b",
                                                filetypes=[("Texto", "*.txt"), ("Todos", "*.*")])
        if not filepath_b:
            return
        try:
            frame._matriz_A = np.loadtxt(filepath_A).astype(float)
            frame._vetor_b = np.loadtxt(filepath_b).astype(float)
            if frame._matriz_A.ndim != 2:
                messagebox.showerror("Erro", "Arquivo de A deve conter matriz 2D.")
                del frame._matriz_A
                del frame._vetor_b
                return
            if frame._vetor_b.ndim != 1:
                frame._vetor_b = frame._vetor_b.flatten()
            if frame._matriz_A.shape[0] != frame._vetor_b.shape[0]:
                messagebox.showerror("Erro", "Tamanho de A e b não compatíveis.")
                del frame._matriz_A
                del frame._vetor_b
                return
            n = frame._matriz_A.shape[0]
            arquivo_status.config(text=f"✓ Arquivos carregados: {n}x{n}\nA: {os.path.basename(filepath_A)}\nb: {os.path.basename(filepath_b)}", fg="green")
            status_label.config(text=f"Arquivo carregado: {n}x{n}", fg="green")
        except Exception as e:
            messagebox.showerror("Erro ao carregar", str(e))

    button_arquivo_frame = tk.Frame(arquivo_frame)
    button_arquivo_frame.pack(fill="x", pady=5)
    tk.Button(button_arquivo_frame, text="Carregar [A|b]", command=carregar_arquivo_estendido, width=15).pack(side="left", padx=5)
    tk.Button(button_arquivo_frame, text="Carregar A e b", command=carregar_arquivo_separado, width=15).pack(side="left", padx=5)

    # 3. Métodos
    methods_frame = tk.LabelFrame(left_panel, text="3. Escolher Método", padx=10, pady=10)
    methods_frame.pack(fill="x", padx=10, pady=5)
    metodo_var = tk.StringVar(value="Gauss")
    metodos_diretos = [("Eliminação de Gauss", "Gauss"), ("Gauss + Pivoteamento Parcial", "GaussPP"),
                       ("Gauss + Pivoteamento Completo", "GaussPC"), ("Decomposição LU", "LU"),
                       ("Decomposição de Cholesky", "Cholesky")]
    metodos_iterativos = [("Gauss-Jacobi", "Jacobi"), ("Gauss-Seidel", "Seidel")]

    tk.Label(methods_frame, text="Métodos Diretos:", font=("Arial", 10, "bold")).pack(anchor="w", pady=(10, 5))
    diretos_frame = tk.Frame(methods_frame); diretos_frame.pack(anchor="w", padx=20)
    for label, val in metodos_diretos:
        tk.Radiobutton(diretos_frame, text=label, variable=metodo_var, value=val).pack(anchor="w")

    tk.Label(methods_frame, text="Métodos Iterativos:", font=("Arial", 10, "bold")).pack(anchor="w", pady=(10, 5))
    iterativos_frame = tk.Frame(methods_frame); iterativos_frame.pack(anchor="w", padx=20)
    for label, val in metodos_iterativos:
        tk.Radiobutton(iterativos_frame, text=label, variable=metodo_var, value=val).pack(anchor="w")

    # 4. Parâmetros iterativos
    params_frame = tk.LabelFrame(left_panel, text="4. Parâmetros (Métodos Iterativos)", padx=10, pady=10)
    params_frame.pack(fill="x", padx=10, pady=5)
    tol_var = tk.StringVar(value="1e-6")
    maxiter_var = tk.StringVar(value="100")
    tk.Label(params_frame, text="Tolerância:").pack(side="left", padx=5)
    tk.Entry(params_frame, textvariable=tol_var, width=15).pack(side="left", padx=5)
    tk.Label(params_frame, text="Máximo de iterações:").pack(side="left", padx=5)
    tk.Entry(params_frame, textvariable=maxiter_var, width=8).pack(side="left", padx=5)
    mostrar_hist_var = tk.BooleanVar(value=False)
    tk.Checkbutton(params_frame, text="Mostrar histórico de iterações", variable=mostrar_hist_var).pack(anchor="w", pady=5)

    # Execução
    exec_frame = tk.Frame(left_panel); exec_frame.pack(fill="x", padx=10, pady=5)

    # Painel direito (resultados - muito maior)
    right_panel = tk.Frame(main_container)
    right_panel.pack(side="right", fill="both", expand=True, padx=(5, 0))

    # Área de resultados - MUITO MAIOR E MELHOR FONTE
    result_frame = tk.LabelFrame(right_panel, text="Resultados", padx=10, pady=10)
    result_frame.pack(fill="both", expand=True)
    
    resultado_text = tk.Text(result_frame, height=30, width=100, font=("Courier", 11), wrap=tk.WORD)
    resultado_text.pack(side="left", fill="both", expand=True)
    resultado_text.config(state='disabled')
    scrollbar_res = tk.Scrollbar(result_frame, command=resultado_text.yview)
    scrollbar_res.pack(side="right", fill="y")
    resultado_text.config(yscrollcommand=scrollbar_res.set)

    def _exibir_resultado(txt):
        resultado_text.config(state='normal')
        resultado_text.delete('1.0', 'end')
        resultado_text.insert('1.0', txt)
        resultado_text.config(state='disabled')

    def executar_metodo():
        tem_campos = bool(entrada_fields)
        tem_arquivo = hasattr(frame, '_matriz_A')
        if not tem_campos and not tem_arquivo:
            messagebox.showwarning("Aviso", "Crie os campos OU carregue um arquivo.")
            return

        if tem_arquivo:
            A = frame._matriz_A.copy(); b = frame._vetor_b.copy(); n = A.shape[0]
        else:
            try:
                n = int(tamanho_var.get())
            except ValueError:
                messagebox.showerror("Erro", "Tamanho inválido."); return
            try:
                A = np.zeros((n, n), dtype=float); b = np.zeros(n, dtype=float)
                for i in range(n):
                    for j in range(n):
                        v = entrada_fields[f"A_{i}"][j].get().strip(); A[i, j] = float(v) if v else 0
                for i in range(n):
                    v = entrada_fields["b"][i].get().strip(); b[i] = float(v) if v else 0
            except Exception as e:
                messagebox.showerror("Erro", f"Valor não numérico: {e}"); return

        metodo = metodo_var.get()
        try:
            base_dir = os.path.dirname(os.path.dirname(__file__))
            module_path = os.path.join(base_dir, 'methods', 'methodsCap03.py')
            spec = importlib.util.spec_from_file_location('methodsCap03', module_path)
            mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)

            texto = f"{'='*70}\nMétodo: {metodo}\nSistema: {n}x{n}\n{'='*70}\n\n"
            texto += "Matriz A:\n"
            for row in A: texto += "  " + _formatar_vetor(row) + "\n"
            texto += "\nVetor b:\n  " + _formatar_vetor(b) + "\n\n" + ("-"*70) + "\n\n"

            if metodo == "Gauss":
                try:
                    x, tempo, info = mod.gauss_eliminacao(A, b); texto += f"Solução:\n{_formatar_vetor(x)}\n\n"
                    texto += f"Tempo de execução: {tempo*1000:.4f} ms\nStatus: {info}\n"
                except ValueError as e:
                    texto += f"❌ ERRO: Matriz Singular ou Mal Condicionada\n"
                    texto += f"   Detalhes: {str(e)}\n"
                    texto += f"   Sugestão: Tente usar 'Gauss + Pivoteamento Parcial' ou 'Completo'\n"
            elif metodo == "GaussPP":
                try:
                    x, tempo, info = mod.gauss_pivoteamento_parcial(A, b); texto += f"Solução:\n{_formatar_vetor(x)}\n\n"
                    texto += f"Tempo de execução: {tempo*1000:.4f} ms\nStatus: {info}\n"
                except ValueError as e:
                    texto += f"❌ ERRO: Matriz Singular\n"
                    texto += f"   Detalhes: {str(e)}\n"
                    texto += f"   Sugestão: Verifique se a matriz é invertível ou tente pivoteamento completo\n"
            elif metodo == "GaussPC":
                try:
                    x, tempo, info = mod.gauss_pivoteamento_completo(A, b); texto += f"Solução:\n{_formatar_vetor(x)}\n\n"
                    texto += f"Tempo de execução: {tempo*1000:.4f} ms\nStatus: {info}\n"
                except ValueError as e:
                    texto += f"❌ ERRO: Matriz Singular ou Numericamente Crítica\n"
                    texto += f"   Detalhes: {str(e)}\n"
                    texto += f"   Sugestão: A matriz pode não ter solução única\n"
            elif metodo == "LU":
                try:
                    x, tempo, info = mod.decomposicao_LU(A, b); texto += f"Solução:\n{_formatar_vetor(x)}\n\n"
                    texto += f"Tempo de execução: {tempo*1000:.4f} ms\nStatus: {info}\n"
                except ValueError as e:
                    texto += f"❌ ERRO: Decomposição LU Falhou\n"
                    texto += f"   Detalhes: {str(e)}\n"
                    texto += f"   Sugestão: Matriz pode ser singular ou mal condicionada\n"
            elif metodo == "Cholesky":
                # Validações PRÉ-EXECUÇÃO
                erros_cholesky = []
                if not np.allclose(A, A.T):
                    erros_cholesky.append("Matriz não é simétrica")
                
                if erros_cholesky:
                    texto += "❌ ERRO: Decomposição de Cholesky Não Aplicável\n\n"
                    texto += "Requisitos para Cholesky:\n"
                    texto += "  ✓ Matriz SIMÉTRICA: A = A^T\n"
                    texto += "  ✓ Matriz DEFINIDA POSITIVA: todos os autovalores > 0\n\n"
                    texto += "Problemas encontrados:\n"
                    for erro in erros_cholesky:
                        texto += f"  ❌ {erro}\n"
                    texto += "\nSugestão: Use 'Gauss + Pivoteamento' ou 'Decomposição LU'\n"
                else:
                    try:
                        x, tempo, info = mod.cholesky(A, b); texto += f"Solução:\n{_formatar_vetor(x)}\n\n"
                        texto += f"Tempo de execução: {tempo*1000:.4f} ms\nStatus: {info}\n"
                    except ValueError as e:
                        texto += f"❌ ERRO: Matriz Não é Definida Positiva\n"
                        texto += f"   Detalhes: {str(e)}\n"
                        texto += f"   Sugestão: A matriz é simétrica mas não é definida positiva\n"
            elif metodo == "Jacobi":
                tol = float(tol_var.get()); max_iter = int(maxiter_var.get())
                texto += f"Parâmetros:\n  Tolerância (ε): {tol:.2e}\n  Max iterações: {max_iter}\n\n"
                
                # Validações PRÉ-EXECUÇÃO
                avisos = []
                if not _verificar_diagonal(A): 
                    avisos.append("Alguns elementos diagonais são muito pequenos")
                if not mod.validar_matriz_convergencia(A): 
                    avisos.append("Matriz não é diagonalmente dominante (convergência NÃO garantida)")
                
                if avisos:
                    texto += "⚠️ AVISOS DE CONVERGÊNCIA:\n"
                    for aviso in avisos:
                        texto += f"  ⚠️ {aviso}\n"
                    texto += "\n"
                
                try:
                    x, num_iter, hist, tempo, info, erro_final = mod.gauss_jacobi(A, b, tol=tol, max_iter=max_iter)
                    texto += f"✓ CONVERGÊNCIA ALCANÇADA\n"
                    texto += f"Número de iterações: {num_iter}\n"
                    texto += f"Erro final (||x_k - x_(k-1)||_∞): {erro_final:.2e}\n"
                    texto += f"Critério de parada: erro < {tol:.2e}\n\n"
                    texto += f"Solução:\n{_formatar_vetor(x)}\n\n"
                    texto += f"Tempo de execução: {tempo*1000:.4f} ms\n"
                    if mostrar_hist_var.get():
                        texto += "\nHistórico de iterações:\n"
                        for i, xi in enumerate(hist): texto += f"  Iteração {i+1}: {_formatar_vetor(xi, prec=4)}\n"
                except ValueError as e:
                    texto += f"❌ ERRO NA EXECUÇÃO\n"
                    texto += f"   {str(e)}\n"
            elif metodo == "Seidel":
                tol = float(tol_var.get()); max_iter = int(maxiter_var.get())
                texto += f"Parâmetros:\n  Tolerância (ε): {tol:.2e}\n  Max iterações: {max_iter}\n\n"
                
                # Validações PRÉ-EXECUÇÃO
                avisos = []
                if not _verificar_diagonal(A): 
                    avisos.append("Alguns elementos diagonais são muito pequenos")
                if not mod.validar_matriz_convergencia(A): 
                    avisos.append("Matriz não é diagonalmente dominante (convergência NÃO garantida)")
                
                if avisos:
                    texto += "⚠️ AVISOS DE CONVERGÊNCIA:\n"
                    for aviso in avisos:
                        texto += f"  ⚠️ {aviso}\n"
                    texto += "\n"
                
                try:
                    x, num_iter, hist, tempo, info, erro_final = mod.gauss_seidel(A, b, tol=tol, max_iter=max_iter)
                    texto += f"✓ CONVERGÊNCIA ALCANÇADA\n"
                    texto += f"Número de iterações: {num_iter}\n"
                    texto += f"Erro final (||x_k - x_(k-1)||_∞): {erro_final:.2e}\n"
                    texto += f"Critério de parada: erro < {tol:.2e}\n\n"
                    texto += f"Solução:\n{_formatar_vetor(x)}\n\n"
                    texto += f"Tempo de execução: {tempo*1000:.4f} ms\n"
                    if mostrar_hist_var.get():
                        texto += "\nHistórico de iterações:\n"
                        for i, xi in enumerate(hist): texto += f"  Iteração {i+1}: {_formatar_vetor(xi, prec=4)}\n"
                except ValueError as e:
                    texto += f"❌ ERRO NA EXECUÇÃO\n"
                    texto += f"   {str(e)}\n"

            _exibir_resultado(texto)
        except Exception as e:
            messagebox.showerror("Erro na execução", f"{type(e).__name__}: {e}")

    tk.Button(exec_frame, text="▶ Executar Método", command=executar_metodo, width=20, bg="green", fg="white", font=("Arial", 10, "bold")).pack(side="left", padx=5)

    # Botões inferiores - no painel esquerdo
    bottom_frame = tk.Frame(left_panel); bottom_frame.pack(fill="x", padx=10, pady=10)
    tk.Button(bottom_frame, text="Voltar", command=voltarTelaInicial, width=15).pack(side="left", padx=5)
    tk.Button(bottom_frame, text="Limpar Resultados", command=lambda: _exibir_resultado(""), width=15).pack(side="left", padx=5)

    return frame


def _formatar_vetor(vetor, prec=8):
    return "  [" + ", ".join(f"{v:.{prec}g}" for v in vetor) + "]"


def _verificar_diagonal(A):
    return all(abs(A[i, i]) > 1e-10 for i in range(len(A)))