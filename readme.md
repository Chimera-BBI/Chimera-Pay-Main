

# Setting Up Python Environment

The tool uses python=3.8

To set up your environment, follow the instructions below:

1. Install Python 3.8
2. Navigate to the root folder of the project.
3. Install the required dependencies using the following command:

```bash
pip3 install -r requirements.txt
```

Note: It is recommended to use a virtual environment to manage your dependencies.


# Setting Up Keys

To set up your keys, follow the instructions below:

1. Navigate to the root folder of the project.
2. Create a new file called `keys.yml`.
3. Open the `keys_template.yml` file located in the root folder.
4. Copy the contents of the `keys_template.yml` file and paste them into the newly created `keys.yml` file.
5. Replace the placeholder values with your own API keys.
6. Save the `keys.yml` file.

Note: The `keys.yml` file contains private information and should not be committed to version control. It has been added to the `.gitignore` file for security reasons.

## Accessing Keys

To access the keys within your application, you can use a YAML parsing library to read the contents of the `keys.yml` file.

Here is an example in Python:

```python
import yaml

with open('keys.yml', 'r') as file:
    keys = yaml.safe_load(file)

# Access individual keys like this
api_key = keys['api_key']
```
Make sure to replace 'api_key' with the actual name of the key you want to access.

