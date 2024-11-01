# PartNet-M-Desc

## Project Overview
**PartNet-M-Desc** is a textual supplement to the PartNet-Mobility dataset. For each object in PartNet-Mobility, we used the GPT-4o API to generate a dictionary of descriptions. This dictionary includes key aspects such as a brief base description (covering size, shape, color, and style), details about the quantity, arrangement, and positioning of each part, as well as internal and external interaction descriptions. This dataset provides rich descriptive information to support 3D object recognition, part analysis, and model training, adding greater detail for related research and applications.

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

- **Base Description:** A one-sentence overview with basic information, including size, shape, color, and style.
- **Part Description:** Information on the object's parts, such as quantity, arrangement, size, and position, limited to 50 characters.
- **Internal Interaction Description:** Describes interactions between parts within the object, up to 100 characters.
- **External Interaction Description:** Describes interactions with external elements, such as other objects or people, up to 100 characters.

---

## Description Generation Method

Each description was generated using the GPT-4 API with the following prompt:
```

Please generate a dictionary based on the given object image, containing the following keys and corresponding descriptions. Generate each key step by step to ensure accuracy:

1. "base_description": Provide a brief description in one sentence, including the object's basic information such as size, shape, color, and style.
2. "part_description": Focus on the object's parts information, including quantity, arrangement, size, and position. Keep it within 50 characters.
3. "internal_interaction_description": Describe the interactions specifically between the parts within the object. Limit this to around 100 characters.
4. "external_interaction_description": Explain the interactions of the object with external elements, such as other objects or people. Limit this to around 100 characters.

**IMPORTANT:** ONLY OUTPUT THE DICT

```


---
## Usage
To load and use the data in this dataset, refer to the following example:

```python
```

---
## Use Case

The **PartNet-M-Desc** project is designed for generating 3D shapes based on pure text descriptions. These descriptions are crafted to ensure that models can:

- **Accurately Fit Original Shapes:** The generated shapes align as closely as possible with the original models, providing high fidelity to the intended design.
- **Provide Interaction Cues:** The descriptions include interaction hints to help ensure the generated object functions logically within its intended environment.
- **Maintain Conciseness:** While we strive to restore the object shape through detailed text descriptions, practical application focuses on balancing detail with efficiency, ensuring descriptions are informative but not overly verbose.


---
## Contributors and Acknowledgments
Special thanks to the researchers behind PartNet [PartNet](https://partnet.cs.stanford.edu/) and  [PartNet-Mobility](https://sapien.ucsd.edu/browse) for their foundational work, as well as to [OpenAI](https://openai.com/) for providing the technology that made these descriptions possible.


---
## License
This project is licensed under the MIT License.