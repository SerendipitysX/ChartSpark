# Let the Chart Spark: Embedding Semantic Context into Chart with Text-to-Image Generative Model

This repository contains the code of *ChartSpark*, a novel system that embeds semantic context into chart based on text-to-image generative model.
*ChartSpark* generates pictorial visualizations conditioned on both semantic context conveyed in textual inputs and data information embedded in plain charts. The method is generic for both foreground and background pictorial generation, satisfying the design practices identified from an empirical research into existing pictorial visualizations.
We further develop an interactive visual interface that integrates a text analyzer, editing module, and evaluation module to enable users to generate, modify, and assess pictorial visualizations.

![teaser.png](asset/teaser.png)

![interface.png](asset/interface.png)

![case.png](asset/case.png)

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

## **Data Corpus**
We collected 689 pictorial visualization in total, which can be find [here](https://drive.google.com/drive/folders/11ELKOwPXb92hXiYgG46_Dcw1cfIHh5p_?usp=share_link)
- Foreground internal single: 395
- Foreground internal multiple: 290
- Foreground external: 121
- Background: 63

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