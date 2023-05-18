# Code Switch Language Modeling for English and Malay
Code-switching refers to the practice of alternating between two or more languages or dialects within a conversation or communication context. It is a common linguistic phenomenon observed in multilingual societies or among bilingual individuals. Code-switching can occur for various reasons, such as cultural identity, social group membership, or convenience.

This repository contains code and resources for code-switched data generation and language modeling for the generated Code-Switched data. 

## Introduction

Code-switched data generation refers to the process of creating or generating text or speech data that exhibits code-switching patterns. This task is often approached in natural language processing (NLP) and computational linguistics research to develop models and systems that can understand, generate, or analyze code-switched language. We use the NSC (National Speech Corpus) dataset to generate code-switched data for English and Malay. The generated data is then used to train and evaluate language models for code-switched data.

## Installation

To use the code and scripts in this repository, please follow these steps:

1. Clone the repository:

   ```bash
   git clone https://github.com/kjgpta/Code-Switch-Language-Modeling-for-English-and-Malay.git
   ```

2. Install the required dependencies. You can use `pip`:

   ```bash
   pip install -r requirements.txt
   ```

3. Setup any additional configuration or environment variables as necessary.

## Usage

This section describes how to use the code and scripts provided in this repository.

1. Data Generation:

   The `Data Generation` directory contains scripts for normalizing, translating, and generating code-switched data. This includes tasks such as data cleaning, normalization, translation, and generation.

2. Language Modeling:

   The `Language Modeling` directory contains code for training and evaluating language models for code-switched data.

Please refer to the individual directories for detailed instructions on how to run each script or module.

## Data

The NSC dataset used in this project is not public and thus is not included in this repository. However, you can request IMDA Singapore to get the same. Once you have obtained the dataset, make sure to follow the preprocessing steps described in the repository to prepare the data for analysis.

## License

This project is licensed under the [CC0-1.0 License](LICENSE).