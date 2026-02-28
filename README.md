# Neural network for predicting satellite failures using the ESA dataset

## Overview

This repository contains the implementation of a neural network model for predicting satellite failures as part of a Master's degree program. The project leverages the ESA (European Space Agency) dataset to train and evaluate the predictive model. For comprehensive details on the project scope, methodology, and objectives, please refer to the [proposal document](./assets/proposal.pdf).

## Setup

This project empowers the use of [nix](https://nixos.org/) and [devenv](https://devenv.sh/) for environment management. To set up the development environment, follow these steps:

1. **Install Nix and devenv**: Follow the instructions on the Getting Started page of the [devenv documentation](https://devenv.sh/docs/getting-started/).
2. **Clone the repository**:

   ```bash
   git clone https://github.com/SamuelHDieterich/neural-network-satellite-failure-prediction
   cd neural-network-satellite-failure-prediction
   ```
3. **[Optional] Install and enable direnv**: This is a tool that automatically loads the environment when you enter the project directory. You can find more information on the [direnv website](https://direnv.net/).
   - If you have direnv installed, run:

     ```bash
     direnv allow
     ```

   - If you don't have direnv, you can skip this step and manually run `devenv` commands.
4. **Start the development environment**: This will set up the virtual environment, install dependencies, and prepare the project for development. If you have direnv enabled, this step will be done automatically when you enter the project directory. Otherwise, run:

   ```bash
   devenv shell
   ```