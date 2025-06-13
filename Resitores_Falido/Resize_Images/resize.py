# Redimensiona imagens organizadas em subpastas por classe para 299x299 pixels,
# mantendo a estrutura de pastas na pasta de destino.

from PIL import Image
import os

def redimensionar_imagens_com_subpastas(pasta_raiz_origem, pasta_raiz_destino, novo_tamanho=(299, 299)):
    """
    Redimensiona imagens organizadas em subpastas por classe, mantendo
    a estrutura de pastas na pasta de destino.

    Args:
        pasta_raiz_origem (str): Caminho para a pasta raiz que contém as subpastas das classes.
        pasta_raiz_destino (str): Caminho para a pasta raiz onde as imagens redimensionadas
                                   e as subpastas serão salvas.
        novo_tamanho (tuple): Uma tupla (largura, altura) para o novo tamanho da imagem.
    """
    if not os.path.exists(pasta_raiz_destino):
        os.makedirs(pasta_raiz_destino)
        print(f"Criada pasta de destino principal: {pasta_raiz_destino}")

    # Percorre os itens (subpastas de classes) dentro da pasta raiz de origem
    for class_name in os.listdir(pasta_raiz_origem):
        class_origem_path = os.path.join(pasta_raiz_origem, class_name)
        class_destino_path = os.path.join(pasta_raiz_destino, class_name)

        # Verifica se o item é um diretório (ou seja, uma pasta de classe de resistor)
        if os.path.isdir(class_origem_path):
            # Cria a subpasta correspondente no diretório de destino, se ela não existir
            if not os.path.exists(class_destino_path):
                os.makedirs(class_destino_path)
                print(f"  Criada subpasta de destino para classe: {class_name}")

            print(f"Processando imagens na classe: {class_name}")

            # Agora, percorre os arquivos dentro desta subpasta de classe
            for filename in os.listdir(class_origem_path):
                # Verifica se o arquivo é uma imagem
                if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
                    filepath_origem = os.path.join(class_origem_path, filename)
                    filepath_destino = os.path.join(class_destino_path, filename)

                    try:
                        with Image.open(filepath_origem) as img:
                            # Redimensiona a imagem usando o algoritmo Lanczos para alta qualidade
                            img_redimensionada = img.resize(novo_tamanho, Image.Resampling.LANCZOS)
                            img_redimensionada.save(filepath_destino)
                    except Exception as e:
                        print(f"    Erro ao processar {filename} na classe {class_name}: {e}")

    print("\nProcessamento concluído!")

pasta_raiz_origem = '/home/jobsr/Resistores'
pasta_raiz_destino = '/home/jobsr/Resistores_299'

redimensionar_imagens_com_subpastas(pasta_raiz_origem, pasta_raiz_destino)