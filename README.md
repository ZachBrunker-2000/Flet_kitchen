# Flet Kitchen

A mobile kitchen application built with [Flet](https://flet.dev/) - a framework for building beautiful multi-platform apps with Flutter and Python.

## 📱 Overview

MobileKitchen is a cross-platform application developed using the Flet framework, enabling you to build applications for desktop, web, and mobile platforms (iOS and Android) from a single Python codebase.

## 🚀 Getting Started

### Prerequisites

- Python 3.9 or higher
- Either `uv` or `Poetry` for dependency management

### Installation & Running

#### Using `uv`

Install and run as a desktop app:

```bash
uv run flet run
```

Run as a web app:

```bash
uv run flet run --web
```

#### Using Poetry

Install dependencies:

```bash
poetry install
```

Run as a desktop app:

```bash
poetry run flet run
```

Run as a web app:

```bash
poetry run flet run --web
```

For more details, refer to the [Flet Getting Started Guide](https://flet.dev/docs/getting-started/).

## 🔨 Building

### Android

Build an APK package:

```bash
flet build apk -v
```

[Android Packaging Guide](https://flet.dev/docs/publish/android/)

### iOS

Build an IPA package:

```bash
flet build ipa -v
```

[iOS Packaging Guide](https://flet.dev/docs/publish/ios/)

### macOS

Build a macOS package:

```bash
flet build macos -v
```

[macOS Packaging Guide](https://flet.dev/docs/publish/macos/)

### Linux

Build a Linux package:

```bash
flet build linux -v
```

[Linux Packaging Guide](https://flet.dev/docs/publish/linux/)

### Windows

Build a Windows package:

```bash
flet build windows -v
```

[Windows Packaging Guide](https://flet.dev/docs/publish/windows/)

## 📦 Project Structure

```
Flet_kitchen/
├── src/                  # Application source code
├── pyproject.toml       # Project configuration for both uv and Poetry
├── README.md           # This file
└── .gitignore         # Git ignore rules
```

## 🛠 Development

### Project Configuration

The `pyproject.toml` file includes:

- **Language**: Python
- **Flet Version**: 0.28.3
- **Package Managers**: uv and Poetry
- **Organization**: com.mycompany (configurable)
- **App Path**: `src/`

### Customization

To customize your app, edit the `[tool.flet]` section in `pyproject.toml`:

- `org`: Organization name (reverse domain notation)
- `product`: App display name
- `company`: Company name for about dialogs
- `copyright`: Copyright information

## 📝 License

MIT License - See LICENSE file for details

## 🔗 Resources

- [Flet Documentation](https://flet.dev/)
- [Flutter Documentation](https://flutter.dev/)
- [Python Documentation](https://docs.python.org/)

## 👨‍💻 Author

**Flet Developer**

---

**Note**: This is a template project. Update the author information, description, and other details in `pyproject.toml` and this README as needed for your specific project.
