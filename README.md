# Let the Chart Spark: Embedding Semantic Context into Chart with Text-to-Image Generative Model

This repository contains the code of *ChartSpark*, a novel system that embeds semantic context into chart based on text-to-image generative model.
*ChartSpark* generates pictorial visualizations conditioned on both semantic context conveyed in textual inputs and data information embedded in plain charts. The method is generic for both foreground and background pictorial generation, satisfying the design practices identified from an empirical research into existing pictorial visualizations.
We further develop an interactive visual interface that integrates a text analyzer, editing module, and evaluation module to enable users to generate, modify, and assess pictorial visualizations.

![tmpBE81.png](https://s3-us-west-2.amazonaws.com/secure.notion-static.com/14dfee7a-6888-4a9b-8cc1-b571ef25e1b6/tmpBE81.png)

![tmpD5E1.png](https://s3-us-west-2.amazonaws.com/secure.notion-static.com/59a09f1e-12f1-456a-96c6-a7f58e9e2e64/tmpD5E1.png)

## Code release progress:

**Todo:**

- Affine transformation
- Refinement
- Replication
- Instruction for Backend Setup
- Instruction for Frontend Setup

Done:

- Environment
- Pretrained model
- mask of chart
- Interface
- Semantic context exrtaction
- Attention map extraction
- Unconditional & conditional generation

## **Dependencies and Installation**

```bash
gitclone https://github.com/SerendipitysX/ChartSpark.git
cd ChartSpark
****conda create --name <environment_name> --file requirements.txt
```

## Pretrained Model

In this work, we benefit from some excellent pretrained models, including [WebVectors](http://vectors.nlpl.eu/explore/embeddings/en/models/) for seeking the relevant words,  [DIS](https://github.com/xuebinqin/DIS) for background removal, and [diffusers](https://github.com/huggingface/diffusers) for generating the image containing semantic context.

To use these models, please follow the steps below:

1. Download the removal pretrained models from [here](https://drive.google.com/drive/folders/1o-VFpRX7wmBgeVXQ75lAOOoj5bLh8s5Y?usp=share_link),  unzip the folder and save it to `mask/`.
2. Select one of corpus from [WebVectors](http://vectors.nlpl.eu/explore/embeddings/en/models/) and save it to theme_extract `theme_extract/`.

## **Contact**

We are glad to hear from you. If you have any questions, please feel free to contact [xrakexss@gmail.com](mailto:xrakexss@gmail.com) or open issues on this repository.