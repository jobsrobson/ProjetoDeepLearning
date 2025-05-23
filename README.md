# Resistor Classification Model (RCM)

## 🚀 Visão Geral
Este projeto simplifica e acelera a leitura de valores de resistores em ambientes de eletrônica, evitando erros humanos e oferecendo uma experiência prática de ponta a ponta em Deep Learning e desenvolvimento full-stack. 


## 🎯 Motivações
Este projeto foi desenvolvido como trabalho final da disciplina de Inteligência Artificial Aplicada (Deep Learning) do curso de Ciência de Dados e Inteligência Artificial do IESB, a convite do professor José Roberto S. Moura. A proposta consistiu em aplicar Redes Neurais Convolucionais na classificação de resistores por imagem, treinar um modelo capaz de identificar valor e tolerância, e realizar o deploy da aplicação em container. A escolha do tema surgiu a partir de observações em uma matéria anterior, na qual muitos estudantes tiveram dificuldade ao identificar manualmente as faixas de cor dos resistores.
- **Automação e Precisão:** Elimina a necessidade de leitura manual das faixas de cor, reduzindo falhas em aplicações de engenharia, laboratórios e hobbistas.  
- **Aprendizado Aplicado:** Permite vivenciar todas as etapas de um projeto de Visão Computacional — desde o processamento de imagens até o deploy em container.  
- **Ferramenta Auxiliar:** Ideal para estudantes, técnicos e makers que desejam confirmar rapidamente o valor de resistores em protótipos ou painéis de teste.


## 📈 Dados de Treinamento
- [Resistor Dataset](https://www.kaggle.com/datasets/eralpozcan/resistor-dataset), por Raif Bayir, Eralp Özcan e İlker Önalan, disponibilizado através do Kaggle.
- Imagens de 37 classes de resistores, dos tipos mais comuns, disponíveis em formato JPG.


## 🛠️ Tecnologias

| Camada      | Ferramenta / Biblioteca            |
| ----------- | ---------------------------------- |
| **Modelagem**   | pyTorch |
| **Backend** | Python 3.10+, Flask          |
| **Frontend**| Flask, HTML5, CSS3, JavaScript     |
| **Infra**   | Docker, AWS |
| **CI/CD**   | GitHub Actions           |


## 📊 Métricas de Sucesso
- Acurácia no Teste: ≥ XX %
- Tempo de Resposta: ≤ 10 s (upload → resposta)
- Robustez: Manter alta performance em variações de iluminação e ruído de fundo
- Usabilidade: Interface simples e intuitiva para upload e visualização dos resultados

