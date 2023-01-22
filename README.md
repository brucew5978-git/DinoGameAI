# DinoGameAI

## Introduction

Used image classification to build a pipeline that plays the Google Dinosaur Game 

My project implements ShuffleNet, an a highly efficient CNN model designed for fast image processing in PyTorch. The model utilizes split channel group convolutions to effectively pass images through shuffle unit, then shuffles the order of outputs tensors to reduce overfitting. After training on the automatically generated datasets earlier in the pipeline, the model performs classification depending on the distance of obstacles to the dinosaur. 

To allow the model to fully control the dinosaur, the program also includes interfaces for taking screen shots, and mapping key actions depending on model prediction.
