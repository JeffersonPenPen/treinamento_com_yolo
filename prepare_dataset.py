import fiftyone as fo
import os
import shutil

# ->-> Configurações do Dataset <-<-
CLASSES_DESEJADAS = ["person", "dog"]
NUMERO_DE_AMOSTRAS = 500
DIRETORIO_EXPORTACAO = "coco-yolo"
ARQUIVO_ZIP_FINAL = "coco-yolo.zip"
# --------------------------------

def main():
    """
    Função principal para baixar, formatar e compactar o dataset.
    """
    print("->-> INICIANDO A PREPARAÇÃO DO DATASET <-<-")

    # Passo 1: Baixar o subconjunto do COCO-2017
    print(f"\n[1/4] Baixando {NUMERO_DE_AMOSTRAS} amostras com as classes: {CLASSES_DESEJADAS}...")
    try:
        dataset = fo.zoo.load_zoo_dataset(
            "coco-2017",
            split="train",
            label_types=["detections"],
            classes=CLASSES_DESEJADAS,
            max_samples=NUMERO_DE_AMOSTRAS,
            only_matching=True,
        )
        print(f"Dataset carregado com {len(dataset)} imagens.")
    except Exception as e:
        print(f"ERRO: Falha ao baixar o dataset. {e}")
        return

    # Passo 2: Exportar para o formato YOLOv5
    print(f"\n[2/4] Exportando o dataset para o formato YOLOv5 em: '{DIRETORIO_EXPORTACAO}'")
    if os.path.exists(DIRETORIO_EXPORTACAO):
        shutil.rmtree(DIRETORIO_EXPORTACAO) # Limpa o diretório se já existir
        
    dataset.export(
        export_dir=DIRETORIO_EXPORTACAO,
        dataset_type=fo.types.YOLOv5Dataset,
        label_field="ground_truth",
        classes=CLASSES_DESEJADAS,
    )
    print("Exportação concluída.")

    # Passo 3: Compactar a pasta para o upload
    print(f"\n[3/4] Compactando o diretório em '{ARQUIVO_ZIP_FINAL}'...")
    try:
        shutil.make_archive(DIRETORIO_EXPORTACAO, 'zip', DIRETORIO_EXPORTACAO)
        print(f"Arquivo '{ARQUIVO_ZIP_FINAL}' criado com sucesso.")
    except Exception as e:
        print(f"ERRO: Falha ao compactar o arquivo. {e}")
        return

    # Passo 4: Limpeza final
    print(f"\n[4/4] Limpando a pasta de exportação temporária...")
    shutil.rmtree(DIRETORIO_EXPORTACAO)
    
    print("\n->-> PROCESSO CONCLUÍDO <-<-")
    print(f"O dataset está pronto no arquivo '{ARQUIVO_ZIP_FINAL}'. Faça o upload dele para o seu Google Drive.")

if __name__ == "__main__":
    main()