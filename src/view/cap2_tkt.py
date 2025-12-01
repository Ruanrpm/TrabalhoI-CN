import os
import tkinter as tk
from tkinter import messagebox
import importlib.util

def criarTelaCap2(container, voltarTelaInicial, on_submit=None):
    """Cria a tela do capítulo 2.

    Parâmetros:
    - container: widget pai onde o frame será empacotado
    - voltarTelaInicial: callback para o botão Voltar
    - on_submit: (opcional) função chamada com os valores parseados: (func_str, a, b, tol, max_iter)
    """
    frame = tk.Frame(container)
    tk.Label(frame, text="Capítulo 02 - Busca de Raízes", font=("Arial", 14, "bold")).pack(pady=10)

    # Container principal com dois painéis
    main_container = tk.Frame(frame)
    main_container.pack(fill="both", expand=True, padx=10, pady=5)

    # Painel esquerdo (entrada)
    left_panel = tk.Frame(main_container)
    left_panel.pack(side="left", fill="both", expand=False, padx=(0, 5))

    tk.Label(left_panel, text="Entrada (cole 5 linhas: função, a, b, tol, max_iter):", font=("Arial", 10)).pack(anchor="w", padx=5)
    entrada = tk.Text(left_panel, height=8, width=45, font=("Courier", 10))
    entrada.pack(padx=5, pady=6)
  
    exemplo = "exp(x**2) + (x) - 6\n0\n2\n0.000000001\n100"
    entrada.insert("1.0", exemplo)

    resultado_label = tk.Label(left_panel, text="", wraplength=350, justify="left", font=("Arial", 9))
    resultado_label.pack(padx=5, pady=4)

    # Área de saída de resultados (read-only) - PAINEL DIREITO
    right_panel = tk.Frame(main_container)
    right_panel.pack(side="right", fill="both", expand=True, padx=(5, 0))

    resultados_label = tk.Label(right_panel, text="Resultados", font=("Arial", 11, "bold"))
    resultados_label.pack(anchor="w", padx=5, pady=(0, 5))

    resultados_out = tk.Text(right_panel, height=30, width=100, font=("Courier", 11), wrap=tk.WORD)
    resultados_out.pack(side="left", fill="both", expand=True)
    resultados_out.config(state='disabled')
    
    scrollbar = tk.Scrollbar(right_panel, command=resultados_out.yview)
    scrollbar.pack(side="right", fill="y")
    resultados_out.config(yscrollcommand=scrollbar.set)

    def parse_entrada():
        raw = entrada.get("1.0", "end").strip()
        if not raw:
            messagebox.showerror("Erro", "Entrada vazia. Cole as 5 linhas (função, a, b, tol, max_iter).")
            return
        lines = [l.strip() for l in raw.splitlines() if l.strip()]
        if len(lines) < 5:
            messagebox.showerror("Erro", f"Foram encontradas {len(lines)} linhas. São necessárias 5 linhas.")
            return
        func_str = lines[0]
        try:
            a = float(lines[1])
            b = float(lines[2])
            tol = float(lines[3])
            max_iter = int(float(lines[4]))
        except ValueError as e:
            messagebox.showerror("Erro de formato", f"Não foi possível converter os valores numéricos: {e}")
            return
 
        resultado_label.config(text=f"Função: {func_str} | a={a}  b={b} | tol={tol} | max_iter={max_iter}")

        # armazenar no frame para acesso externo, se necessário
        frame._last_input = {
            "func": func_str,
            "a": a,
            "b": b,
            "tol": tol,
            "max_iter": max_iter,
        }

        # chamar callback se fornecido
        if on_submit:
            try:
                on_submit(func_str, a, b, tol, max_iter)
            except Exception as ex:
                messagebox.showerror("Erro no callback", str(ex))

    btn_frame = tk.Frame(left_panel)
    btn_frame.pack(pady=6)
    tk.Button(btn_frame, text="Confirmar", command=parse_entrada, width=12).pack(side="left", padx=3)
    tk.Button(btn_frame, text="Voltar", command=voltarTelaInicial, width=12).pack(side="left", padx=3)

    # Frame para botões de métodos (secante, newton, bissecao, MIL, regula falsi)
    methods_frame = tk.LabelFrame(left_panel, text="Métodos de raiz", font=("Arial", 10, "bold"))
    methods_frame.pack(fill="x", padx=5, pady=8)

    def _load_methods_module():
        # Carrega o módulo diretamente do arquivo para garantir que ele leia o arq_leitura.txt atualizado
        base_dir = os.path.dirname(os.path.dirname(__file__))  # src/
        module_path = os.path.join(base_dir, 'methods', 'methodsCap02.py')
        spec = importlib.util.spec_from_file_location('methodsCap02', module_path)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        return mod

    def _call_method(name):
        # Verifica se temos input salvo
        if not hasattr(frame, '_last_input'):
            messagebox.showwarning('Aviso', 'Primeiro clique em Confirmar para salvar a entrada.')
            return
        inp = frame._last_input
        a = inp['a']
        b = inp['b']
        tol = inp['tol']
        it = inp['max_iter']

        try:
            mod = _load_methods_module()
        except Exception as e:
            messagebox.showerror('Erro', f'Falha ao carregar módulo de métodos: {e}')
            return

        try:
            if name == 'Secante':
                mod.secante(a, b, tol, it)
            elif name == 'Newton':
                mod.newton(a, b, tol, it)
            elif name == 'Bissecao':
                mod.bissecao([a, b], tol, it)
            elif name == 'MIL':
                mod.Mil(a, tol, it)
            elif name == 'Regula Falsi':
                mod.r_falsi([a, b], tol, tol, it)
            else:
                messagebox.showerror('Erro', f'Método desconhecido: {name}')
                return
        except Exception as ex:
            messagebox.showerror('Erro na execução', str(ex))
            return

        # após execução, pedir ao módulo escrever resultados (se existir)
        try:
            if hasattr(mod, 'escrever_resultados'):
                mod.escrever_resultados()
        except Exception:
            pass

        # obter último resultado do módulo e mostrar na área de saída (substitui conteúdo anterior)
        try:
            if hasattr(mod, 'resultados') and name in mod.resultados:
                lst = mod.resultados.get(name, [])
                if lst:
                    ultimo = lst[-1]
                    raiz, k = ultimo
                    text = f"{name} -> raiz: {raiz} | iteração: {k}\n"
                else:
                    text = f"{name} -> sem resultados\n"
            else:
                text = f"{name} -> sem resultados\n"

            # atualizar Text (read-only) substituindo o conteúdo anterior
            resultados_out.config(state='normal')
            resultados_out.delete('1.0', 'end')
            resultados_out.insert('1.0', text)
            resultados_out.see('1.0')
            resultados_out.config(state='disabled')
        except Exception as ex:
            # se falhar a leitura dos resultados, apenas substitui com mensagem de erro breve
            resultados_out.config(state='normal')
            resultados_out.delete('1.0', 'end')
            resultados_out.insert('1.0', f"Erro ao obter resultado: {ex}\n")
            resultados_out.config(state='disabled')

    # Criar botões dinamicamente com base nos nomes usados no módulo
    for m in ['Secante', 'Newton', 'Bissecao', 'MIL', 'Regula Falsi']:
        tk.Button(methods_frame, text=m, width=11, command=lambda nm=m: _call_method(nm), font=("Arial", 9)).pack(side='left', padx=3, pady=6)

    return frame
    