# CrewAI Test Automation Framework

A unified test automation framework powered by CrewAI, integrating Azure DevOps, Selenium, and Page Object Model. Supports both Python and Java, automatically generates and exports test scenarios to Excel, and enables end-to-end automation for web applications.

## Features
- Fetch requirements from Azure DevOps
- Generate detailed test scenarios using CrewAI
- Export test cases to Excel
- Generate Selenium automation code (Python & Java)
- Page Object Model structure
- Easy integration and extensibility

## Project Structure
```
pom.xml
requirements.txt
setup.py
src/
  main/
    java/
    python/
  test/
    java/
    python/
    resources/
venv_py310/
```

## Getting Started
1. Clone the repository:
   ```bash
   git clone https://github.com/Ruchika-Jha/crewai-test-automation.git
   cd crewai-test-automation
   ```
2. Set up Python virtual environment:
   ```bash
   python3 -m venv venv_py310
   source venv_py310/bin/activate
   pip install -r requirements.txt
   ```
3. Configure your `.env` file with Azure DevOps and OpenAI credentials.
4. Run the main workflow:
   ```bash
   python src/main/python/main.py
   ```

## Contributing
Pull requests are welcome! For major changes, please open an issue first to discuss what you would like to change.

## License
MIT
