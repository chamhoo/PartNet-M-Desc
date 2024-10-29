# PartNet-M-Desc

## Project Overview
**PartNet-M-Desc** is a textual supplement to the PartNet-Mobility dataset. For each object in PartNet-Mobility, we used the GPT-4o API to generate a description of approximately 100 words, detailing the object’s color, shape, size, and other characteristics, as well as the position and connection method of each part. This dataset provides rich descriptive information, facilitating enhanced detail for 3D object recognition, part analysis, and model training, supporting related research and applications.

---

## Dataset Structure

The dataset is structured as follows:
```
PartNet-M-Desc/
├── objects/
│   ├── 1.json
│   ├── 2.json
│   └── ...
└── README.md

```
Each `.json` file contains:

- **Object ID:** A unique identifier
- **Description:** Textual description with detailed characteristics (color, shape, size, etc.)

---

## Description Generation Method

Each description was generated using the GPT-4 API with the following prompt:
```
```


---
## Usage
To load and use the data in this dataset, refer to the following example:

```python
```

---
## Contributors and Acknowledgments
Special thanks to the researchers behind PartNet [PartNet](https://partnet.cs.stanford.edu/) and  [PartNet-Mobility](https://sapien.ucsd.edu/browse) for their foundational work, as well as to [OpenAI](https://openai.com/) for providing the technology that made these descriptions possible.


---
## License
This project is licensed under the MIT License.