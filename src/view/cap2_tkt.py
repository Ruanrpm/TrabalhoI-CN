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
    tk.Label(frame, text="Capitulo 02").pack(pady=8)

    tk.Label(frame, text="Entrada (cole 5 linhas: função, a, b, tol, max_iter):").pack(anchor="w", padx=10)
    entrada = tk.Text(frame, height=6, width=50)
    entrada.pack(padx=10, pady=6)
  
    exemplo = "exp(x**2) + (x) - 6\n0\n2\n0.000000001\n100"
    entrada.insert("1.0", exemplo)

    resultado_label = tk.Label(frame, text="")
    resultado_label.pack(padx=10, pady=4)

    # Área de saída de resultados (read-only)
    resultados_out = tk.Text(frame, height=8, width=70)
    resultados_out.pack(padx=10, pady=6)
    resultados_out.config(state='disabled')

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

    btn_frame = tk.Frame(frame)
    btn_frame.pack(pady=6)
    tk.Button(btn_frame, text="Confirmar", command=parse_entrada).pack(side="left", padx=6)
    tk.Button(btn_frame, text="Voltar", command=voltarTelaInicial).pack(side="left", padx=6)

    # Frame para botões de métodos (secante, newton, bissecao, MIL, regula falsi)
    methods_frame = tk.LabelFrame(frame, text="Métodos de raiz")
    methods_frame.pack(fill="x", padx=10, pady=8)

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
                mod.newton(a, tol, it)
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
        tk.Button(methods_frame, text=m, width=12, command=lambda nm=m: _call_method(nm)).pack(side='left', padx=6, pady=6)

    return frame
    