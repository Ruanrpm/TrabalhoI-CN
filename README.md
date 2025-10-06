# 🔢 Métodos Numéricos para Aproximação de Raízes  

Este projeto implementa em **Python** quatro métodos numéricos clássicos utilizados para **encontrar raízes de funções** reais. Ele permite calcular aproximações sucessivas até atingir uma precisão definida, salvando os resultados em um arquivo `.txt` em formato tabular.  

---

## 📘 Métodos Implementados

1. **Método da Bisseção**  
   Baseia-se na divisão sucessiva de um intervalo onde ocorre mudança de sinal da função até que o tamanho do intervalo seja suficientemente pequeno.  
   - Garantia de convergência.  
   - Mais lento, mas estável.  

2. **Método da Falsa Posição (Regula Falsi)**  
   Combina as ideias da bisseção com uma aproximação linear da função.  
   - Mais rápido que a bisseção.  
   - Pode convergir lentamente em alguns casos.  

3. **Método da Secante**  
   Usa duas aproximações iniciais e constrói uma reta secante entre os pontos para estimar a raiz.  
   - Não requer derivada.  
   - Convergência mais rápida, mas depende de boas aproximações iniciais.  

4. **Método de Newton-Raphson**  
   Utiliza a derivada da função para encontrar a raiz de forma iterativa.  
   - Convergência quadrática.  
   - Requer cálculo da derivada e uma boa aproximação inicial.  

---


## ⚙️ Estrutura do Projeto

├── main.py # Arquivo principal de execução

├── arq_leitura.txt # Arquivo de entrada

├── arq_escrita.txt # Arquivo de saída com resultados formatados em colunas



---

## 🧩 Como Funciona

1. O usuário fornece:  
   - A função `f(x)`  
   - (Opcional) `p(x)`  
   - O intervalo `[a, b]`  
   - A precisão desejada  
   - O número máximo de iterações  

2. O programa aplica os métodos e salva os resultados no arquivo `arq_escrita.txt`



---

## 🧮 Exemplo de Uso

Entrada:
```python
f(x) = exp(-x**2) - cos(x)
Intervalo:
1
3
Precisão: 0.0000001
Iterações máximas: 100


Método          Raiz Aproximada      Iterações
-----------------------------------------------
Bisseção        1.436758             20
Regula Falsi    1.436756             10
Secante         1.436757             5
Newton          1.436756             4

```


---
## 🧠 Conceitos Utilizados

  - Aproximações sucessivas de raízes reais.

  - Critérios de parada por erro absoluto.

  - Recursão e controle de iterações.

  - Escrita e formatação de arquivos em Python.
  
---

## 🧰 Tecnologias Utilizadas

  - Python 

  - Bibliotecas padrão: math, sympy


---

## 📄 Licença

  - Este projeto é de uso livre para fins educacionais e acadêmicos.


---

## 👨‍💻 Autor

Desenvolvido por Ruan Pablo — estudante de Ciência da Computação.
Sinta-se à vontade para contribuir ou deixar sugestões! 🚀
