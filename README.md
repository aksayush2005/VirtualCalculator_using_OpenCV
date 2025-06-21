# Virtual Calculator using OpenCV

A Python-based virtual calculator that leverages OpenCV for real-time hand gesture recognition, enabling touchless interaction. This project integrates computer vision techniques with a trained Artificial Neural Network (ANN) model to interpret hand gestures as numerical inputs, facilitating arithmetic operations without physical contact.

## Features

- **Hand Gesture Recognition**: Utilizes OpenCV to detect and interpret hand gestures in real-time.
- **Digit Classification**: Employs a trained ANN model (`MNIST_ANN.py`) to classify hand-drawn digits accurately.
- **Virtual Interface**: Provides an on-screen calculator interface that responds to recognized gestures.
- **Real-Time Feedback**: Displays inputs and results dynamically, enhancing user interaction.

## Installation

1. **Clone the Repository**:

   ```bash
   git clone https://github.com/aksayush2005/VirtualCalculator_using_OpenCV.git
   cd VirtualCalculator_using_OpenCV
   ```

2. **Set Up a Virtual Environment**:

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**:

   Ensure you have Python 3.x installed. Then, install the required packages:

   ```bash
   pip install opencv-python numpy
   ```

   

## Usage

1. **Train the ANN Model**:

   Before running the calculator, train the digit classification model:

   ```bash
   python CUSTOM_ANN.py
   ```

   This script trains an ANN on a custom dataset(custom_hand_data.zip) and saves the model.Ensure the dataset is present in the working directory.

2. **Run the Virtual Calculator**:

   After training the model, launch the calculator interface:

   ```bash
   python calculator.py
   ```

   A window will open using your webcam. Use hand gestures to input numbers and perform calculations.
### Demo Video:
https://youtu.be/kEPfQGFMVKs

## Project Structure

```
├── CUSTOM_ANN.py         # Script to train the ANN model on the custom dataset
├── calculator.py        # Main application script for the virtual calculator
├── custom_hand_data.zip # Custom Dataset,ensure that it is present in the working directory
```

## Contributing

Contributions are welcome! If you'd like to enhance functionality, fix bugs, or improve documentation, please fork the repository and submit a pull request.

## License

This project is open-source and available under the [MIT License](LICENSE).

## Acknowledgments

- [OpenCV](https://opencv.org/) for providing powerful computer vision tools.
